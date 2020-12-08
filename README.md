# Sala de bate papo

Implementar um Sistema de Gerenciamento e Utilização de Comunicação
por Mensagens

Devem ser implementado um servidor (sockets ou RMI/RPC) para gerenciar o
Broker, com as seguintes funcionalidades:

1. Adicionar e remover filas e tópicos :heavy_check_mark:
2. Listas quantidade de mensagens nas filas :hourglass_flowing_sand: :bug: :shipit:	
3. Instanciar novos usuários (verificar duplicidade de nomes) :x:
4. Criar automaticamente uma fila para cada usuário novo criado :hourglass_flowing_sand:

Os usuários, por sua vez, devem implementar as seguintes funcionalidades:

1. Permitir assinar tópicos :x:	
2. Enviar mensagens entre usuários diretamente online :heavy_check_mark:	
3. Enviar mensagens entre usuários diretamente offline :heavy_check_mark:
4. Enviar mensagens para tópicos :x:


## Tecnologias utilizadas nesse projeto

[Python 3.7.7](https://www.python.org/downloads/)

[RabbitMQ](https://www.rabbitmq.com/)

[Pika](https://pika.readthedocs.io/en/stable/)

[PyRabbit](https://github.com/bkjones/pyrabbit)

[Kivy](https://github.com/kivy/kivy)

[Docker](https://www.docker.com/)

[Pyro4](https://github.com/irmen/Pyro4)


## Executando o projeto

` docker run --rm -p 5672:5672 -p 8080:15672 rabbitmq:3-management `
agora acesse ` http://localhost:8080 ` com usuario e senha `guest`

## Dificuldades encontradas

Na primeira vez que fui executar o hello world, tive que utilizar o comando abaixo:
` sudo apt-get install rabbitmq-server `. Após isso, foi possível enviar a mensagem para o broker.

caso dê problema com a porta usada pelo rabbitmq: https://stackoverflow.com/questions/40266556/address-already-in-use-error-upon-docker-compose-up/40266908

## Melhorias pendentes


## Materiais de estudo usados como base

- [Primeiros passos com RabbitMQ e python](https://blog.ateliedocodigo.com.br/primeiros-passos-com-rabbitmq-e-python-938fb0957019)
- [RabbitMQ com Python](https://gist.github.com/renatoapcosta/2a4b6c7a5933edf09e9226e11f1ca989)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html)
- [Introdução ao RabbitMQ](https://www.youtube.com/watch?v=1WgrnSDDtVE&feature=emb_logo)
- [Live de Python #145 - Interfaces gráficas com Kivy](https://www.youtube.com/watch?v=5ApbLrcUtlE)
- [Curso de Kivy na prática](https://www.youtube.com/playlist?list=PLsMpSZTgkF5AV1FmALMgW8W-TvrfR3nrs)
