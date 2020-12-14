from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from typing import List
import Pyro4


api = Pyro4.core.Proxy("PYRONAME:servidor.rmi")


class Gerenciador(ScreenManager):
    ...


class HistoricoUsuario(Screen):
    ...


class HistoricoTopico(Screen):
    ...


class Usuario(Button):
    def __init__(self, nome_usuario: str = "", **kwargs):
        super().__init__(**kwargs)
        self.text = nome_usuario


class Topico(Button):
    def __init__(self, nome_topico: str = "", **kwargs):
        super().__init__(**kwargs)
        self.text = nome_topico


class InterfaceUsuario(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def criar_listas(self):
        usuarios: List[str] = api.listar_filas()
        topicos: List[str] = api.listar_topicos()

        for usuario in usuarios:
            self.ids.lista_usuarios.add_widget(Usuario(nome_usuario=usuario))

        for topico in topicos:
            self.ids.lista_topicos.add_widget(Topico(nome_topico=topico))


class Chat(App):
    def __init__(self):
        super(Chat, self).__init__()
        self.referencia_usuario = None

    def build(self):
        gerenciador = Gerenciador()
        gerenciador.get_screen("tela_principal").criar_listas()
        gerenciador.get_screen(
            "tela_principal"
        ).ids.menu_tela_principal.title = self.referencia_usuario.nome
        return gerenciador

    def atualizar_listas_usuarios(self) -> None:
        usuarios: List[str] = api.listar_filas()
        self.root.get_screen("tela_principal").ids.lista_usuarios.clear_widgets()
        for usuario in usuarios:
            self.root.get_screen("tela_principal").ids.lista_usuarios.add_widget(
                Usuario(nome_usuario=usuario)
            )

    def atualizar_listas_topicos(self) -> None:
        topicos: List[str] = api.listar_topicos()
        self.root.get_screen("tela_principal").ids.lista_topicos.clear_widgets()
        for topico in topicos:
            self.root.get_screen("tela_principal").ids.lista_topicos.add_widget(
                Topico(nome_topico=topico)
            )

    def enviar_mensagem_usuario(self, mensagem: str, destinatario: str) -> None:
        self.root.get_screen("historico_usuario").ids.mensagem_usuario.text = ""
        self.referencia_usuario.enviar_mensagem_para_algum_usuario(
            mensagem=mensagem, destinatario=destinatario
        )
        self.mostrar_historico_usuario(nome_usuario=destinatario)

    def mostrar_historico_usuario(self, nome_usuario: str) -> None:
        historico = self.referencia_usuario.pegar_historico(
            nome=nome_usuario, tipo="usuarios"
        )
        self.root.get_screen("historico_usuario").ids.nome_usuario.title = nome_usuario
        self.root.get_screen(
            "historico_usuario"
        ).ids.historico_do_usuario.text = historico
        self.root.current = "historico_usuario"

    def mostrar_historico_topico(self, nome_topico: str) -> None:
        historico = self.referencia_usuario.pegar_historico(
            nome=nome_topico, tipo="topicos"
        )
        historico_topico = self.root.get_screen("historico_topico")
        historico_topico.ids.nome_topico.title = nome_topico
        historico_topico.ids.historico_do_topico.text = historico
        self.root.current = "historico_topico"

    def assinar_topico(self, nome_topico: str) -> None:
        self.referencia_usuario.assinar_topico(nome_topico=nome_topico)

    def enviar_mensagem_topico(self, mensagem: str, nome_topico: str) -> None:
        self.root.get_screen("historico_topico").ids.mensagem_topico.text = ""
        self.referencia_usuario.enviar_mensagem_para_o_topico(
            nome_topico=nome_topico, mensagem=mensagem
        )
        self.mostrar_historico_topico(nome_topico=nome_topico)
