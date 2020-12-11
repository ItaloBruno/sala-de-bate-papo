from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from typing import List


class InterfaceServidor(BoxLayout):
    def __init__(self, usuarios: List[str], topicos: List[str], **kwargs):
        super().__init__(**kwargs)
        for usuario in usuarios:
            self.ids.lista_usuarios.add_widget(
                Usuario(texto=usuario)
            )

        for topico in topicos:
            self.ids.lista_topicos.add_widget(
                Topico(texto=topico)
            )


class Usuario(BoxLayout):
    def __init__(self, texto: str = "", **kwargs):
        super().__init__(**kwargs)
        self.ids.usuario.text = texto


class Topico(BoxLayout):
    def __init__(self, texto: str = "", **kwargs):
        super().__init__(**kwargs)
        self.ids.topico.text = texto


class Servidor(App):
    def build(self):
        # TODO: pegar as listas de usuários e tópicos direto do broker
        usuarios: List[str] = ["maradona", "foginho", "batistuta", "yoda", "esteban"]
        topicos: List[str] = ["nba", "nfl", "mbl", "nhl", "nbb"]

        return InterfaceServidor(
            usuarios=usuarios,
            topicos=topicos
        )

    @staticmethod
    def adicionar_novo_usuario(referencia: BoxLayout, novo_texto: str):
        referencia.add_widget(
            Usuario(texto=novo_texto)
        )
        # TODO: adcionar esse novo usuário no broker

    @staticmethod
    def adicionar_novo_topico(referencia: BoxLayout, novo_texto: str):
        referencia.add_widget(
            Topico(texto=novo_texto)
        )
        # TODO: adcionar esse novo tópico no broker

    @staticmethod
    def remover_usuario(referencia: BoxLayout, item):
        referencia.remove_widget(item)
        # TODO: remover esse usuário no broker

    @staticmethod
    def remover_topico(referencia: BoxLayout, item):
        referencia.remove_widget(item)
        # TODO: remover esse tópico no broker


Servidor().run()
