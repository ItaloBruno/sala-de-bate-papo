# Sala de bate papo



## Tecnologias utilizadas nesse projeto

[Python 3.8](https://www.python.org/downloads/)

[RabbitMQ](https://www.rabbitmq.com/)

[Pika](https://pika.readthedocs.io/en/stable/)

[PyRabbit](https://github.com/bkjones/pyrabbit)

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

