from chat import Chat

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
    def receber_mensagem(self, nome_usuario: str, mensagem: dict):
        ...

    def enviar_mensagem_para_algum_usuario(self):
        ...

    def enviar_mensagem_para_o_topico(self):
        ...

    def assinar_topico(self):
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
        thread_interface = threading.Thread(target=self.iniciar_interface_chat)
        thread_interface.start()
        _ = self.servidor.registrar(self.nome, self)
        # self.historico_de_mensagens += (
        #     f"\nConectado como {self.nome}"
        # )
        # self.historico_de_mensagens += f"{self.nome} >"

        thread_para_enviar_mensagem = threading.Thread(
            target=self.enviar_mensagem_para_algum_usuario
        )

        thread_para_enviar_mensagem.start()

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
