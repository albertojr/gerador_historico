# Gerador de Hístórico
<p align="center"> Pequeno projeto feito para auxiliar a geração de histórico em secretárias de escolas municipais.Meu pai trabalha na secretária de uma escola, onde é necessário anualmente atualizar ou gerar os históricos de cada aluno. Feito de forma manual com um documento do word, muitas vezes o histórico se perde devido a quantidade, sendo necessário criar um novo. Esse projeto foi pensado em ter um banco de dados dos alunos, disciplinas, turmas e notas permitindo a geração do histórico de forma mais rápida e automatizada.</p>

<p align="center">
 <a href="#Gerador">Objetivo</a> •
 <a href="#tecnologias">Tecnologias</a> • 
 <a href="#funcionalidades">Funcionalidades</a> • 
 <a href="#instalação">Instalação</a> • 
 <a href="#tecnologias">Como rodar</a> • 
 <a href="#autor">Autor</a>
</p>

### Tecnologias
* Django 3.0;
* Front-end: Template Admin LTE 3;
* Jquery 3.5;
* Banco de dados postgres.

### Funcionalidades
* CRUD de notas com tabela;
* CRUD de estudos realizados (Aprovação de outras escolas);
* CRUD de alunos;
* Gerar arquivo PDF com histórico pronto;

### Instalação
> LINUX

1. Instale o python com o comando: 

    sudo apt-get install python3

2. Para instalar o gerenciador de pacotes pip, digite em um terminal:

    sudo apt-get install python3-pip

3. Instale o **VirtualEnv** para o ambiente virtual com o seguinte comando:

    pip install virtualenv

4. Após a instalação, crie o ambiente virtual com o comando:

    virtualenv nome_do_ambiente_virtual

5. Depois, basta ativar o ambiente,com esse comando:
    
    source **nome_do_ambiente_virtual**/bin/activate

6. Uma vez instalado e ativado o ambiente, basta instalar as dependecias do projeto:
    
    pip install -r requirements-dev

7. Configure o python decouple com as variáveis ambiente, secret_key e acesso ao banco de dados:

    *Lembrando, que deve criar um banco de dados no postgres e configurar no .env*, segue um exemplo do .env:

    DB_NAME = nome_do_banco
    
    
    DB_USER = nome_usuario
    
    
    DB_PASSWORD = senha_do_psotgres
    
    
    SECRET_KEY = sua_secret_key
    
    
    DEBUG = True

8. Após instalar todas as dependências e configurar as variáveis ambiente, rode o projeto:


    python manage.py runserver

9. Uma vez com o sistema rodando, basta realizar o comando **migrate** para criar o banco de dados:


    python manage.py migrate

10. Pronto, o **ambiente de desenvolvimento do sistema está rodando!**





