import Pyro4
import pika
import time
from pyrabbit.api import Client


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ServidorRMI(object):
    def __init__(self):
        self.canais_de_comunicacao = {
            "usuarios": [],
            "servidor": [],
        }
        self.nomes_usuarios_conectados = set()

    def pegar_canais_de_comunicacao(self):
        return list(self.canais_de_comunicacao.keys())

    def pegar_nomes_dos_usuarios(self):
        return list(self.nomes_usuarios_conectados)

    def registrar(self, nome_usuario, objeto_usuario):
        if not nome_usuario:
            raise ValueError("Nome de usuário inválido!!!")

        if nome_usuario in self.nomes_usuarios_conectados:
            raise ValueError("Esse nome de usuário já está sendo usado!!!")

        self.criar_fila(nome_usuario)
        self.atualizar_listas_usuarios_nas_interfaces()
        self.canais_de_comunicacao["usuarios"].append((nome_usuario, objeto_usuario))
        self.nomes_usuarios_conectados.add(nome_usuario)
        print(f"Usuário {nome_usuario} se conectou!")

        return [
            nome_usuario for (nome_usuario, c) in self.canais_de_comunicacao["usuarios"]
        ]

    # def selecionar_usuario(self, nome_usuario):
    #     for nome, objeto in self.canais_de_comunicacao["usuarios"]:
    #         if nome == nome_usuario:
    #             return objeto
    #
    #     return None

    def publicar(self, nome_remetente, nome_destinatario, mensagem):
        if nome_destinatario not in self.nomes_usuarios_conectados:
            print(f"{nome_destinatario} não existe!")
            return

        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue=nome_destinatario)
        channel.basic_publish(exchange="", routing_key=nome_destinatario, body=mensagem)
        print(
            f" [x] Mensagem de {nome_remetente} enviada para {nome_destinatario}: {mensagem}"
        )
        connection.close()

    def consumir_fila(self, nome_usuario, objeto_usuario):
        # todo: não está funcionando da forma correta
        def callback(ch, method, properties, body):
            objeto_usuario.receber_mensagem(body)

        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        channel.queue_declare(queue=nome_usuario)

        channel.basic_consume(
            queue=nome_usuario, auto_ack=True, on_message_callback=callback
        )

        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()

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

        self.nomes_usuarios_conectados.add(nome_da_fila)
        self.atualizar_listas_usuarios_nas_interfaces()

    def listar_filas(self):
        cl = Client("localhost:8080", "guest", "guest")
        queues = [q["name"] for q in cl.get_queues()]
        print(f"filas existentes: {queues}")
        return queues

    def remover_fila(self, nome_da_fila):
        cl = Client("localhost:8080", "guest", "guest")
        cl.delete_queue(vhost="/", qname=nome_da_fila)
        self.atualizar_listas_usuarios_nas_interfaces()

    def enviar_mensagem_para_fila(self, canal, conexao, nome_da_fila, mensagem):
        canal.basic_publish(exchange="", routing_key=nome_da_fila, body=mensagem)
        print(" [x] Enviada '" + mensagem + "'")
        time.sleep(0.5)
        # conexao.close()

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

    def criar_topico(self, nome_do_topico):
        cl = Client("localhost:8080", "guest", "guest")
        result = cl.create_exchange("/", nome_do_topico, "topic")
        if result:
            print("tópico criado com sucesso")
            self.atualizar_listas_topicos_nas_interfaces()

    def listar_topicos(self):
        cl = Client("localhost:8080", "guest", "guest")
        exchanges = cl.get_exchanges()
        topicos = []
        for e in exchanges:
            if e["type"] == "topic" and "amq." not in e["name"]:
                topicos.append(e["name"])

        print(f"tópicos: {topicos}")
        return topicos

    def remover_topico(self, nome_do_topico):
        cl = Client("localhost:8080", "guest", "guest")
        cl.delete_exchange(vhost="/", name=nome_do_topico)
        self.atualizar_listas_topicos_nas_interfaces()

    def atualizar_listas_usuarios_nas_interfaces(self):
        usuarios = self.canais_de_comunicacao["usuarios"]
        for nome_usuario, objeto_usuario in usuarios:
            objeto_usuario.atualizar_listas_usuarios()

    def atualizar_listas_topicos_nas_interfaces(self):
        usuarios = self.canais_de_comunicacao["usuarios"]
        for nome_usuario, objeto_usuario in usuarios:
            objeto_usuario.atualizar_listas_topicos()


Pyro4.Daemon.serveSimple({ServidorRMI: "servidor.rmi"})
