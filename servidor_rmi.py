import Pyro4
import pika
from pyrabbit.api import Client
from typing import List, Set, Dict


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ServidorRMI(object):
    def __init__(self):
        self.canais_de_comunicacao: Dict[str, List] = {"usuarios": []}
        self.nomes_usuarios_conectados: Set[str] = set()

    def pegar_canais_de_comunicacao(self) -> List[str]:
        return list(self.canais_de_comunicacao.keys())

    def pegar_nomes_dos_usuarios(self) -> List[str]:
        return list(self.nomes_usuarios_conectados)

    def registrar(self, nome_usuario: str, objeto_usuario: object) -> List[str]:
        if not nome_usuario:
            raise ValueError("Nome de usuário inválido!!!")

        self.criar_fila(nome_usuario)
        self.atualizar_listas_usuarios_nas_interfaces()
        self.canais_de_comunicacao["usuarios"].append((nome_usuario, objeto_usuario))
        self.nomes_usuarios_conectados.add(nome_usuario)
        print(f"Usuário {nome_usuario} se conectou!")

        return [
            nome_usuario for (nome_usuario, c) in self.canais_de_comunicacao["usuarios"]
        ]

    def publicar(
        self, nome_remetente: str, nome_destinatario: str, mensagem: str
    ) -> None:
        if nome_destinatario not in self.nomes_usuarios_conectados:
            print(f"{nome_destinatario} não existe!")
            return

        conexao = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        canal = conexao.channel()
        canal.queue_declare(queue=nome_destinatario)
        canal.basic_publish(exchange="", routing_key=nome_destinatario, body=mensagem)
        print(
            f" [x] Mensagem de {nome_remetente} enviada para {nome_destinatario}: {mensagem}"
        )
        conexao.close()

    def criar_fila(self, nome_da_fila: str) -> None:
        conexao = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        canal = conexao.channel()
        canal.queue_declare(queue=nome_da_fila)
        conexao.close()

        self.nomes_usuarios_conectados.add(nome_da_fila)
        self.atualizar_listas_usuarios_nas_interfaces()

    def listar_filas(self) -> List[str]:
        cl = Client("localhost:8080", "guest", "guest")
        queues = []
        for q in cl.get_queues():
            if "amq." not in q["name"]:
                queues.append(q["name"])

        print(f"filas existentes: {queues}")
        return queues

    def remover_fila(self, nome_da_fila: str) -> None:
        cl = Client("localhost:8080", "guest", "guest")
        cl.delete_queue(vhost="/", qname=nome_da_fila)
        self.atualizar_listas_usuarios_nas_interfaces()

    def listar_quantidade_mensagens_nas_filas(self) -> int:
        # todo: o número de mensagens nas filas não correspondem ao valor adquirido pela função
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

        return quantidade

    def criar_topico(self, nome_do_topico: str) -> None:
        cl = Client("localhost:8080", "guest", "guest")
        result = cl.create_exchange("/", nome_do_topico, "fanout")
        if result:
            print("tópico criado com sucesso")
            self.atualizar_listas_topicos_nas_interfaces()

    def listar_topicos(self) -> List[str]:
        cl = Client("localhost:8080", "guest", "guest")
        exchanges = cl.get_exchanges()
        topicos = []
        for e in exchanges:
            if e["type"] == "fanout" and "amq." not in e["name"]:
                topicos.append(e["name"])

        print(f"tópicos: {topicos}")
        return topicos

    def remover_topico(self, nome_do_topico: str) -> None:
        cl = Client("localhost:8080", "guest", "guest")
        cl.delete_exchange(vhost="/", name=nome_do_topico)
        self.atualizar_listas_topicos_nas_interfaces()

    def atualizar_listas_usuarios_nas_interfaces(self) -> None:
        usuarios = self.canais_de_comunicacao["usuarios"]
        for nome_usuario, objeto_usuario in usuarios:
            objeto_usuario.atualizar_listas_usuarios()

    def atualizar_listas_topicos_nas_interfaces(self) -> None:
        usuarios = self.canais_de_comunicacao["usuarios"]
        for nome_usuario, objeto_usuario in usuarios:
            objeto_usuario.atualizar_listas_topicos()

    @Pyro4.oneway
    def enviar_mensagem_para_topico(self, nome_topico: str, mensagem: str) -> None:
        conexao = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        canal = conexao.channel()

        canal.exchange_declare(exchange=nome_topico, exchange_type="fanout")

        canal.basic_publish(exchange=nome_topico, routing_key="", body=mensagem)
        print(f" [x] enviando '{mensagem}' para o tópico {nome_topico}")
        conexao.close()


Pyro4.Daemon.serveSimple({ServidorRMI: "servidor.rmi"})
