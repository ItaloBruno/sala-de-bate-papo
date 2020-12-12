from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from typing import List

import Pyro4


class Interface(BoxLayout):
    def __init__(self, usuarios: List[str], topicos: List[str], **kwargs):
        super().__init__(**kwargs)
        for usuario in usuarios:
            self.ids.lista_usuarios.add_widget(Usuario(nome_usuario=usuario))

        for topico in topicos:
            self.ids.lista_topicos.add_widget(Topico(nome_topico=topico))


class Usuario(BoxLayout):
    def __init__(self, nome_usuario: str = "", **kwargs):
        super().__init__(**kwargs)
        self.ids.usuario.text = nome_usuario


class Topico(BoxLayout):
    def __init__(self, nome_topico: str = "", **kwargs):
        super().__init__(**kwargs)
        self.ids.topico.text = nome_topico


class Servidor(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = Pyro4.core.Proxy("PYRONAME:servidor.rmi")

    def build(self):
        usuarios: List[str] = self.api.listar_filas()
        topicos: List[str] = self.api.listar_topicos()

        return Interface(usuarios=usuarios, topicos=topicos)

    def adicionar_novo_usuario(self, box: BoxLayout, nome_usuario: str):
        usuarios_existentes = self.api.listar_filas()
        nome_usuario = nome_usuario.strip()
        if nome_usuario not in usuarios_existentes:
            box.add_widget(Usuario(nome_usuario=nome_usuario))
            self.api.criar_fila(nome_da_fila=nome_usuario)

    def adicionar_novo_topico(self, box: BoxLayout, nome_topico: str):
        topicos_existentes = self.api.listar_topicos()
        nome_topico = nome_topico.strip()
        if nome_topico not in topicos_existentes:
            box.add_widget(Topico(nome_topico=nome_topico))
            self.api.criar_topico(nome_topico)

    def remover_usuario(self, box: BoxLayout, usuario: BoxLayout):
        nome_usuario = usuario.ids.usuario.text
        box.remove_widget(usuario)
        self.api.remover_fila(nome_usuario)
        self.api.atualizar_listas_usuarios_nas_interfaces()

    def remover_topico(self, box: BoxLayout, topico: BoxLayout):
        nome_topico = topico.ids.topico.text
        box.remove_widget(topico)
        self.api.remover_topico(nome_topico)

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


Servidor().run()
