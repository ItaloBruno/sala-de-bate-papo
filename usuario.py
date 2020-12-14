from chat import Chat
import threading
import Pyro4
import pika


@Pyro4.expose
class Usuario(object):
    def __init__(self):
        self.servidor = Pyro4.core.Proxy("PYRONAME:servidor.rmi")
        self.historico_de_mensagens = {"usuarios": {}, "topicos": {}}
        self.nome = ""
        self.conexao_encerrada = False
        self.interface = Chat()

    @Pyro4.expose
    @Pyro4.oneway
    def receber_mensagem(self, msg: bytes) -> None:
        msg = msg.decode()
        dados_mensagem = msg.split(" > ")
        if not self.historico_de_mensagens["usuarios"].get(dados_mensagem[0], None):
            self.historico_de_mensagens["usuarios"].update({dados_mensagem[0]: ""})

        self.historico_de_mensagens["usuarios"][dados_mensagem[0]] += f"\n{msg}"
        print(f"mensagem recebida: {msg}")
        if self.interface.root.current == "historico_usuario":
            self.interface.mostrar_historico_usuario(dados_mensagem[0])

    @Pyro4.expose
    @Pyro4.oneway
    def receber_mensagem_topico(self, msg: bytes) -> None:
        msg = msg.decode()
        dados_mensagem = msg.split(" > ")
        if not self.historico_de_mensagens["topicos"].get(dados_mensagem[0], None):
            self.historico_de_mensagens["topicos"].update({dados_mensagem[0]: ""})

        self.historico_de_mensagens["topicos"][dados_mensagem[0]] += f"\n{msg}"
        print(f"mensagem recebida: {msg}")
        if self.interface.root.current == "historico_topico":
            self.interface.mostrar_historico_topico(dados_mensagem[0])

    def escutar_minha_fila(self) -> None:
        def callback(ch, method, properties, body) -> None:
            self.receber_mensagem(body)

        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        channel.queue_declare(queue=self.nome)

        channel.basic_consume(
            queue=self.nome, auto_ack=True, on_message_callback=callback
        )

        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()

    def enviar_mensagem_para_algum_usuario(
        self, mensagem: str, destinatario: str
    ) -> None:
        historico = self.historico_de_mensagens["usuarios"].get(destinatario, None)
        if not historico:
            self.historico_de_mensagens["usuarios"].update({destinatario: ""})

        mensagem = f"{self.nome} > {mensagem}"
        self.historico_de_mensagens["usuarios"][destinatario] += f"\n{mensagem}"

        self.servidor.publicar(self.nome, destinatario, mensagem)

    def enviar_mensagem_para_o_topico(self, nome_topico: str, mensagem: str) -> None:
        historico = self.historico_de_mensagens["topicos"].get(nome_topico, None)
        if not historico:
            self.historico_de_mensagens["topicos"].update({nome_topico: ""})

        mensagem = f"{nome_topico} > {mensagem}"
        self.historico_de_mensagens["topicos"][nome_topico] += f"\n{mensagem}"
        self.servidor.enviar_mensagem_para_topico(
            nome_topico=nome_topico, mensagem=mensagem
        )

    def assinar_topico(self, nome_topico: str) -> None:
        thread_topico = threading.Thread(
            target=self.escutar_topico, args=(nome_topico,)
        )
        thread_topico.start()

    def escutar_topico(self, nome_topico: str) -> None:
        # todo: os usuários que estão escutando esse topico não tão recebendo as mensagens
        conexao = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        canal = conexao.channel()

        canal.exchange_declare(
            exchange=nome_topico, exchange_type="fanout", durable=True
        )

        resultado = canal.queue_declare("", exclusive=True)
        nome_fila = resultado.method.queue

        canal.queue_bind(exchange=nome_topico, queue=nome_fila)

        print(" [*] Waiting for logs. To exit press CTRL+C")

        def callback(ch, method, properties, body):
            print(" [x] %r:%r" % (method.routing_key, body))
            self.receber_mensagem_topico(body)

        canal.basic_consume(
            queue=nome_fila, on_message_callback=callback, auto_ack=True
        )

        canal.start_consuming()

    def iniciar_interface_chat(self) -> None:
        self.interface.referencia_usuario = self
        self.interface.run()

    def iniciar_chat(self) -> None:
        nomes_usuarios = self.servidor.pegar_nomes_dos_usuarios()
        if nomes_usuarios:
            print(
                "Os seguintes usuários estão conectados no servidor: {}".format(
                    (", ".join(nomes_usuarios))
                )
            )

        self.nome = input("Escolha seu nome: ").strip()
        _ = self.servidor.registrar(self.nome, self)

        thread_interface = threading.Thread(target=self.iniciar_interface_chat)
        thread_interface.start()

        thread_receber_mensagem = threading.Thread(target=self.escutar_minha_fila)
        thread_receber_mensagem.start()

    @Pyro4.expose
    @Pyro4.oneway
    def atualizar_listas_usuarios(self) -> None:
        self.interface.atualizar_listas_usuarios()

    @Pyro4.expose
    @Pyro4.oneway
    def atualizar_listas_topicos(self) -> None:
        self.interface.atualizar_listas_topicos()

    def pegar_historico(self, nome: str, tipo: str) -> str:
        historico = ""
        if tipo in self.historico_de_mensagens.keys():
            historico = self.historico_de_mensagens[tipo].get(nome, "")

        return historico


class DaemonThread(threading.Thread):
    def __init__(self, usuario):
        threading.Thread.__init__(self)
        self.jogador = usuario
        self.setDaemon(True)

    def run(self):
        with Pyro4.core.Daemon() as daemon:
            daemon.register(self.jogador)
            daemon.requestLoop(lambda: not self.jogador.conexao_encerrada)


usuario = Usuario()
daemonthread = DaemonThread(usuario)
daemonthread.start()
usuario.iniciar_chat()
