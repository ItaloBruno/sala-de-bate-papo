from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class InterfaceChat(BoxLayout):
    # TODO: Quando inicializar essa tela, inicializar os elementos nas listas de usuários e tópicos
    #  fazer isso de forma dinâmica eatualizar telas quando adicionar/remover algum usuário/tópico
    ...


class Chat(App):
    def build(self):
        return InterfaceChat()


Chat().run()
