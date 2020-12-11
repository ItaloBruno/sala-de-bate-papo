from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from typing import List

from gerenciador import (
    criar_topico,
    criar_fila,
    criar_canal_de_conexao,
    remover_fila,
    remover_topico,
    listar_filas,
    listar_topicos,
)


class InterfaceServidor(BoxLayout):
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
    def build(self):
        usuarios: List[str] = listar_filas()
        topicos: List[str] = listar_topicos()

        return InterfaceServidor(usuarios=usuarios, topicos=topicos)

    @staticmethod
    def adicionar_novo_usuario(referencia: BoxLayout, nome_usuario: str):
        usuarios_existentes = listar_filas()
        nome_usuario = nome_usuario.strip()
        if nome_usuario not in usuarios_existentes:
            referencia.add_widget(Usuario(nome_usuario=nome_usuario))
            conexao, canal = criar_canal_de_conexao()
            criar_fila(canal, nome_usuario)
            conexao.close()

    @staticmethod
    def adicionar_novo_topico(referencia: BoxLayout, nome_topico: str):
        topicos_existentes = listar_topicos()
        nome_topico = nome_topico.strip()
        if nome_topico not in topicos_existentes:
            referencia.add_widget(Topico(nome_topico=nome_topico))
            criar_topico(nome_topico)

    @staticmethod
    def remover_usuario(referencia: BoxLayout, item):
        nome_usuario = item.ids.usuario.text
        referencia.remove_widget(item)
        remover_fila(nome_usuario)

    @staticmethod
    def remover_topico(referencia: BoxLayout, item):
        referencia.remove_widget(item)
        nome_topico = item.ids.topico.text
        referencia.remove_widget(item)
        remover_topico(nome_topico)


Servidor().run()
