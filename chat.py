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

    def atualizar_listas_usuarios(self):
        usuarios: List[str] = api.listar_filas()
        self.root.get_screen("tela_principal").ids.lista_usuarios.clear_widgets()
        for usuario in usuarios:
            self.root.get_screen("tela_principal").ids.lista_usuarios.add_widget(
                Usuario(nome_usuario=usuario)
            )

    def atualizar_listas_topicos(self):
        topicos: List[str] = api.listar_topicos()
        self.root.get_screen("tela_principal").ids.lista_topicos.clear_widgets()
        for topico in topicos:
            self.root.get_screen("tela_principal").ids.lista_topicos.add_widget(
                Topico(nome_topico=topico)
            )

    def enviar_mensagem_usuario(self, mensagem: str, destinatario: str):
        self.root.get_screen("historico_usuario").ids.mensagem_usuario.text = ""
        self.referencia_usuario.enviar_mensagem_para_algum_usuario(
            mensagem=mensagem, destinatario=destinatario
        )
        self.mostrar_historico_usuario(nome_usuario=destinatario, tipo="usuarios")

    def mostrar_historico_usuario(self, nome_usuario: str, tipo: str):
        historico = self.referencia_usuario.pegar_historico(
            nome=nome_usuario, tipo=tipo
        )
        self.root.get_screen("historico_usuario").ids.nome_usuario.title = nome_usuario
        self.root.get_screen(
            "historico_usuario"
        ).ids.historico_do_usuario.text = historico
        self.root.current = "historico_usuario"
