from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from typing import List

import Pyro4


class InterfaceUsuario(BoxLayout):
    def __init__(self, usuarios: List[str], topicos: List[str], **kwargs):
        super().__init__(**kwargs)
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = Pyro4.core.Proxy("PYRONAME:servidor.rmi")

    def build(self):
        usuarios: List[str] = self.api.listar_filas()
        topicos: List[str] = self.api.listar_topicos()

        return InterfaceUsuario(usuarios=usuarios, topicos=topicos)

    def atualizar_listas_usuarios(self):
        usuarios: List[str] = self.api.listar_filas()
        self.ids.lista_usuarios.clear_widgets()
        for usuario in usuarios:
            self.ids.lista_usuarios.add_widget(Usuario(nome_usuario=usuario))

    def atualizar_listas_topicos(self):
        topicos: List[str] = self.api.listar_topicos()
        self.ids.lista_topicos.clear_widgets()
        for topico in topicos:
            self.ids.lista_topicos.add_widget(Topico(nome_topico=topico))


Chat().run()
