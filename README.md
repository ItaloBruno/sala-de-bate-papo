# Sala de bate papo

Implementar um Sistema de Gerenciamento e Utilização de Comunicação
por Mensagens.

Deve ser implementado um servidor (sockets ou RMI/RPC) para gerenciar o
Broker, com as seguintes funcionalidades:

1. Adicionar e remover filas e tópicos :heavy_check_mark:
2. Listas quantidade de mensagens nas filas :hourglass_flowing_sand: :bug: :shipit:	
3. Instanciar novos usuários (verificar duplicidade de nomes) :heavy_check_mark:
4. Criar automaticamente uma fila para cada usuário novo criado :heavy_check_mark:

Os usuários, por sua vez, devem implementar as seguintes funcionalidades:

1. Permitir assinar tópicos :heavy_check_mark:
2. Enviar mensagens entre usuários diretamente online :heavy_check_mark:	
3. Enviar mensagens entre usuários diretamente offline :hourglass_flowing_sand: :bug: :shipit:	
4. Enviar mensagens para tópicos :hourglass_flowing_sand: :bug:


## Tecnologias utilizadas nesse projeto

[Python 3.7.7](https://www.python.org/downloads/)

[RabbitMQ](https://www.rabbitmq.com/)

[Pika](https://pika.readthedocs.io/en/stable/)

[PyRabbit](https://github.com/bkjones/pyrabbit)

[Kivy](https://github.com/kivy/kivy)

[Docker](https://www.docker.com/)

[Pyro4](https://github.com/irmen/Pyro4)


## Executando o projeto

1. Para começar, precisamos subir o serviço do RabbitMQ. Para isso, execute o seguinte comando 
   (caso você tenha o docker instalado em sua máquina):
   
` docker run --rm -p 5672:5672 -p 8080:15672 rabbitmq:3-management `

obs.: caso você não tenho o [Docker](https://www.docker.com/) instalado, instale-o ou siga as instruções do site ofical do [RabbitMQ](https://www.rabbitmq.com/download.html) 

Após subir o serviço, acesse ` http://localhost:8080 ` com usuario e senha `guest` para acessar o gerenciador diretamente do browser.


2.  Você deve subir o servidor de nomes, para que possamos 
    registrar o servidor do chat e possibilitar o seu acesso remoto. 
    Para isso, abra um terminal e execute o comando abaixo:

    ` pyro4-ns `

3. Para registra o servidor no servidor de nomes, abra um outro terminal e execute:

    ` python servidor_rmi.py `

4. Agora para iniciar a interface de gerenciamento do servidor, abra um novo terminal e execute:

    ` python servidor.py `

5. Tamo chegando lá, calma kkk. Para executar a interface do usuário, abra um novo terminal para cada 
   novo usuário que você queira utilizar e execute o comando abaixo:
   
    ` python usuario.py `

Ufa, acho que agora podemos bater um papo em paz. Aproveitem xD

## Dificuldades encontradas

- Na primeira vez que fui executar o hello world do rabbitmq, tive que utilizar o comando abaixo:

` sudo apt-get install rabbitmq-server `
  
Após isso, foi possível enviar a mensagem para o broker.

- Caso dê problema com a porta usada pelo rabbitmq, acesse esse [link](https://stackoverflow.com/questions/40266556/address-already-in-use-error-upon-docker-compose-up/40266908)
  
- Não consegui utilizar uma função no servidor_rmi para escutar as filas. A solução que achei foi deixar essa parte no próprio usuário :pensive:

## Melhorias pendentes

- Deixar as interfaces do servidor e do cliente mais amigáveis/bonitas
- Enviar de forma correta as mensagens para todos que assinam um tópico
- Colocar a informação da quantidade de mensagens em cada fila na interface do servidor (existe uma função que busca essa informação mas não está sendo utilizada na GUI)
- Permitir a comunicação entre usuários que estejam offline

## Materiais de estudo usados como base

- [Primeiros passos com RabbitMQ e python](https://blog.ateliedocodigo.com.br/primeiros-passos-com-rabbitmq-e-python-938fb0957019)
- [RabbitMQ com Python](https://gist.github.com/renatoapcosta/2a4b6c7a5933edf09e9226e11f1ca989)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html)
- [Introdução ao RabbitMQ](https://www.youtube.com/watch?v=1WgrnSDDtVE&feature=emb_logo)
- [Live de Python #145 - Interfaces gráficas com Kivy](https://www.youtube.com/watch?v=5ApbLrcUtlE)
- [Curso de Kivy na prática](https://www.youtube.com/playlist?list=PLsMpSZTgkF5AV1FmALMgW8W-TvrfR3nrs)
