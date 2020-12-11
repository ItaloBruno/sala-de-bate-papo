import Pyro4
import pika
import time
from pyrabbit.api import Client


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ServidorRMI(object):
    def __init__(self):
        self.canais_de_comunicacao = (
            {}
        )  # registered channels { channel --> (nick, client callback) list }
        self.nomes_usuarios_conectados = []  # all registered nicks on this server

    def pegar_canais_de_comunicacao(self):
        return list(self.canais_de_comunicacao.keys())

    def pegar_nomes_dos_usuarios(self):
        return self.nomes_usuarios_conectados

    def registrar(self, nome_canal, nome_usuario, objeto_usuario):
        if not nome_canal or not nome_usuario:
            raise ValueError("Nome de canal/jogador inválido!!!")

        if nome_usuario in self.nomes_usuarios_conectados:
            raise ValueError("Esse nome de jogador já está sendo usado!!!")

        if nome_canal not in self.canais_de_comunicacao:
            print(f"Criando novo canal {nome_canal}")
            self.canais_de_comunicacao[nome_canal] = []

        self.canais_de_comunicacao[nome_canal].append((nome_usuario, objeto_usuario))
        self.nomes_usuarios_conectados.append(nome_usuario)
        print(f"Usuário {nome_usuario} se conectou!")

        return [
            nome_usuario for (nome_usuario, c) in self.canais_de_comunicacao[nome_canal]
        ]

    def publicar(self, nome_canal, nome_usuario, mensagem):
        if nome_canal not in self.canais_de_comunicacao:
            print(f"CANAL DESCONHECIDO IGNORADO {nome_canal}")
            return
        for (n, c) in self.canais_de_comunicacao[nome_canal][:]:
            try:
                c.receber_mensagem(nome_usuario, mensagem)
            except Pyro4.errors.ConnectionClosedError:
                if (n, c) in self.canais_de_comunicacao[nome_canal]:
                    self.canais_de_comunicacao[nome_canal].remove((n, c))
                    print(f"Ouvinte morto removido {n} - {c} ")

    def desconectar_usuario(self, nome_canal, nome_usuario):
        if nome_canal not in self.canais_de_comunicacao:
            print(f"CANAL DESCONHECIDO IGNORADO {nome_canal}")
            return

        for (n, c) in self.canais_de_comunicacao[nome_canal]:
            if n == nome_usuario:
                self.canais_de_comunicacao[nome_canal].remove((n, c))
                break

        if len(self.canais_de_comunicacao[nome_canal]) < 1:
            del self.canais_de_comunicacao[nome_canal]
            print(f"Canal {nome_canal} removido")

        self.nomes_usuarios_conectados.remove(nome_usuario)
        print(f"O usuário {nome_usuario} deixou o canal {nome_canal}")

    def criar_fila(self, nome_da_fila):
        conexao = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        canal = conexao.channel()
        canal.queue_declare(queue=nome_da_fila)
        conexao.close()

    def enviar_mensagem_para_fila(self, canal, conexao, nome_da_fila, mensagem):
        canal.basic_publish(exchange="", routing_key=nome_da_fila, body=mensagem)
        print(" [x] Enviada '" + mensagem + "'")
        time.sleep(0.5)
        # conexao.close()

    def listar_filas(self):
        cl = Client("localhost:8080", "guest", "guest")
        queues = [q["name"] for q in cl.get_queues()]
        print(f"filas existentes: {queues}")
        return queues

    def remover_fila(self, nome_da_fila):
        cl = Client("localhost:8080", "guest", "guest")
        cl.delete_queue(vhost="/", qname=nome_da_fila)

    def criar_topico(self, nome_do_topico):
        cl = Client("localhost:8080", "guest", "guest")
        result = cl.create_exchange("/", nome_do_topico, "topic")
        if result:
            print("tópico criado com sucesso")

    def remover_topico(self, nome_do_topico):
        cl = Client("localhost:8080", "guest", "guest")
        cl.delete_exchange(vhost="/", name=nome_do_topico)

    def listar_topicos(self):
        cl = Client("localhost:8080", "guest", "guest")
        exchanges = cl.get_exchanges()
        topicos = []
        for e in exchanges:
            if e["type"] == "topic" and "amq." not in e["name"]:
                topicos.append(e["name"])

        print(f"tópicos: {topicos}")
        return topicos

    def listar_host(self):
        cl = Client("localhost:8080", "guest", "guest")
        hosts = cl.get_vhost_names()
        print(f"hosts: {hosts}")

    def listar_quantidade_mensagens_nas_filas(self):
        cl = Client("localhost:8080", "guest", "guest")
        quantidade = 0
        filas = cl.get_queues()
        for q in filas:
            print(
                "nome da fila: {} - quantidade de mensagens: {}".format(
                    q["name"], q["messages"]
                )
            )
            quantidade += q["messages"]

        print(f"quantidade total de mensagens: {quantidade}")
        # msg = cl.get_messages("/", "hoje")
        # print(msg)

        return quantidade


Pyro4.Daemon.serveSimple({ServidorRMI: "servidor.rmi"})
