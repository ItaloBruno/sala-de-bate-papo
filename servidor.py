from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class InterfaceServidor(BoxLayout):
    # TODO: Quando inicializar essa tela, inicializar os elementos nas listas de usuários e tópicos
    #  fazer isso de forma dinâmica e atualizar telas quando adicionar/remover algum usuário/tópico
    ...


class Servidor(App):
    def build(self):
        return InterfaceServidor()


Servidor().run()
