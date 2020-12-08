import pika
import time
from pyrabbit.api import Client
from pprint import pprint


def criar_canal_de_conexao():
    conexao = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    canal = conexao.channel()
    return conexao, canal


def criar_fila(canal, nome_da_fila):
    canal.queue_declare(queue=nome_da_fila)


def enviar_mensagem_para_fila(canal, conexao, nome_da_fila, mensagem):
    canal.basic_publish(exchange="", routing_key=nome_da_fila, body=mensagem)
    print(" [x] Enviada '" + mensagem + "'")
    time.sleep(0.5)
    # conexao.close()


def listar_filas():
    cl = Client('localhost:8080', 'guest', 'guest')
    queues = [q['name'] for q in cl.get_queues()]
    print(f"filas existentes: {queues}")
    return queues


def remover_fila(nome_da_fila):
    cl = Client('localhost:8080', 'guest', 'guest')
    cl.delete_queue(vhost="/", qname=nome_da_fila)


def criar_topico(nome_do_topico):
    cl = Client('localhost:8080', 'guest', 'guest')
    result = cl.create_exchange('/', nome_do_topico, "topic")
    if result:
        print("tópico criado com sucesso")


def remover_topico(nome_do_topico):
    cl = Client('localhost:8080', 'guest', 'guest')
    cl.delete_exchange(vhost="/", name=nome_do_topico)


def listar_topicos():
    cl = Client('localhost:8080', 'guest', 'guest')
    exchanges = cl.get_exchanges()
    topicos = []
    for e in exchanges:
        if e["type"] == "topic":
            topicos.append(e["name"])

    print(f"tópicos: {topicos}")


def listar_host():
    cl = Client('localhost:8080', 'guest', 'guest')
    hosts = cl.get_vhost_names()
    print(f"hosts: {hosts}")


def listar_quantidade_mensagens_nas_filas():
    cl = Client('localhost:8080', 'guest', 'guest')
    quantidade = 0
    filas = cl.get_queues()
    for q in filas:
        print("nome da fila: {} - quantidade de mensagens: {}".format(q["name"], q["messages"]))
        quantidade += q['messages']

    print(f"quantidade total de mensagens: {quantidade}")
    # msg = cl.get_messages("/", "hoje")
    #
    # print(msg)


if __name__ == '__main__':
    remetente = input("Qual o seu nome? ")
    destinatario = input("Qual o nome do usuário que você quer enviar a mensagem? ")

    conexao, canal = criar_canal_de_conexao()
    criar_fila(canal, remetente)
    criar_fila(canal, destinatario)

    listar_filas()
    listar_topicos()
    listar_host()

    print()
    criar_topico("cumpadis")
    listar_topicos()

    print()
    remover_topico("cumpadis")
    listar_topicos()
    #
    # print()
    # listar_filas()
    # remover_fila(destinatario)
    # listar_filas()

    mensagens = [
        "Primeira mensagem",
        "Segunda mensagem",
        "Terceira mensagem",
        "Quarta mensagem",
        "Quinta mensagem",
    ]

    for msg in mensagens:
        canal.basic_publish(exchange="", routing_key=destinatario, body=msg)
        print(" [x] Enviada '" + msg + "'")
        time.sleep(0.5)

    for msg in mensagens[:3]:
        canal.basic_publish(exchange="", routing_key=remetente, body=msg)
        print(" [x] Enviada '" + msg + "'")
        time.sleep(0.5)

    # time.sleep(5)
    filas = listar_filas()

    listar_quantidade_mensagens_nas_filas()

    conexao.close()
