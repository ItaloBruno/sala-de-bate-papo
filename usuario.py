from chat import Chat
import pika

import threading
import Pyro4


@Pyro4.expose
class Usuario(object):
    def __init__(self):
        self.servidor = Pyro4.core.Proxy("PYRONAME:servidor.rmi")
        self.historico_de_mensagens = {}
        self.canal_de_comunicacao = ""
        self.conexao_encerrada = False
        self.nome = ""
        self.interface = Chat()

    @Pyro4.expose
    @Pyro4.oneway
    def receber_mensagem(self, msg):
        # todo: redirecionar mensagem para um usuário em específico
        print(f"Mensagem recebida: {msg}")

    def escutar_minha_fila(self):
        # todo: tentar executar essa função usando o servidor
        # self.servidor.consumir_fila(self.nome, self)
        def callback(ch, method, properties, body):
            print(f"Mensagem recebida: {body.decode()}")

        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()

        channel.queue_declare(queue=self.nome)

        channel.basic_consume(
            queue=self.nome, auto_ack=True, on_message_callback=callback
        )

        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()

    def enviar_mensagem_para_algum_usuario(self):
        try:
            try:
                while not self.conexao_encerrada:
                    destinatario = input(
                        f"para quem você quer enviar uma mensagem? "
                    ).strip()
                    msg = input(f"{self.nome}> ").strip()
                    if msg:
                        msg = f"{self.nome} > {msg}"
                        self.servidor.publicar(self.nome, destinatario, msg)
            except EOFError:
                pass
        finally:
            pass

    def enviar_mensagem_para_o_topico(self):
        # todo: enviar mensagem par aum determinado tópico
        ...

    def assinar_topico(self):
        # todo: assinar um tópico já existente
        ...

    def iniciar_interface_chat(self):
        self.interface.run()

    def iniciar_chat(self):
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

        thread_para_enviar_mensagem = threading.Thread(
            target=self.enviar_mensagem_para_algum_usuario
        )
        thread_para_enviar_mensagem.start()

        thread_receber_mensagem = threading.Thread(target=self.escutar_minha_fila)
        thread_receber_mensagem.start()

    @Pyro4.expose
    @Pyro4.oneway
    def atualizar_listas_usuarios(self):
        self.interface.atualizar_listas_usuarios()

    @Pyro4.expose
    @Pyro4.oneway
    def atualizar_listas_topicos(self):
        self.interface.atualizar_listas_topicos()


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
