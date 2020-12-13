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


class Topico(Screen):
    ...


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


class Usuario(Button):
    def __init__(self, nome_usuario: str = "", **kwargs):
        super().__init__(**kwargs)
        self.text = nome_usuario


class Topico(Button):
    def __init__(self, nome_topico: str = "", **kwargs):
        super().__init__(**kwargs)
        self.text = nome_topico


class Chat(App):
    def build(self):
        gerenciador = Gerenciador()
        gerenciador.get_screen("tela_principal").criar_listas()
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
