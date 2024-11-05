<h1>SGE - Sistema de Gerenciamento Empresarial</h1>

<p align="center">
  <img src="https://img.shields.io/static/v1?label=Python&message=3.10&color=blue&style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/static/v1?label=Flask&message=2.1&color=green&style=for-the-badge&logo=flask"/>
  <img src="https://img.shields.io/static/v1?label=PostgreSQL&message=13&color=4169E1&style=for-the-badge&logo=postgresql"/>
  <img src="https://img.shields.io/static/v1?label=SQLAlchemy&message=1.4&color=orange&style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/static/v1?label=JWT&message=2.0&color=black&style=for-the-badge&logo=jsonwebtokens"/>
  <img src="http://img.shields.io/static/v1?label=STATUS&message=CONCLUIDO&color=green&style=for-the-badge"/>
  <img src="https://img.shields.io/static/v1?label=License&message=MIT&color=blue&style=for-the-badge"/>
</p>

> Status do Projeto: :heavy_check_mark: (concluido) | :warning: (em desenvolvimento) | :x: (não iniciada)

### Tópicos

:small_blue_diamond: [Descrição do Projeto](#descrição-do-projeto-writing_hand) :heavy_check_mark:  

:small_blue_diamond: [Objetivos do Projeto](#objetivos-do-projeto-dart) :heavy_check_mark:  

:small_blue_diamond: [Funcionalidades](#funcionalidades-video_game) :heavy_check_mark:  

:small_blue_diamond: [Arquitetura](#arquitetura-triangular_ruler-straight_ruler) :heavy_check_mark:

:small_blue_diamond: [Rotas - Endpoints](#rotas---endpoints-arrows_clockwise) :heavy_check_mark:  

:small_blue_diamond: [Criar e ativar ambiente virtual](#criar-e-ativar-ambiente-virtual-white_check_mark)

:small_blue_diamond: [Instalação das depedências](#instalação-das-depedências-arrow_down_small)

:small_blue_diamond: [Executar Migrações](#executar-migrações-arrow_forward)

:small_blue_diamond: [Executar App](#executar-app-arrow_forward)

:small_blue_diamond: [Linguagens, Tecnologias e Bibliotecas Utilizadas](#linguagens-tecnologias-dependências-e-libs-utilizadas-hammer_and_wrench-gear-books)  

---


## Descrição do Projeto :writing_hand:

O **Sistema de Gerenciamento Empresarial (SGE)** é uma solução para simplificar e centralizar o gerenciamento de operações de uma empresa, incluindo o controle de clientes, produtos, categorias, pedidos e detalhes dos pedidos. Utilizando uma arquitetura de camadas e uma API RESTful, o SGE oferece uma plataforma escalável e segura para o gerenciamento empresarial.

---

## Objetivos do Projeto :dart:

**1. Centralizar o Gerenciamento**  
- Centralizar e otimizar a gestão de clientes, produtos e pedidos.

**2. Automação de Processos**  
- Automatizar processos como cadastro de pedidos e atualização de estoque.

**3. Facilitar a consulta e gerenciamento** 
- Facilitar a consulta e gerenciamento de dados relacionados a clientes, produtos e pedidos.

**4. Segurança e Autenticação**  
- Utilizar JWT para proteger os dados e assegurar operações seguras.

**5. Facilidade de Integração**  
- Proporcionar uma API RESTful robusta que permita integração com outros sistemas.

---

## Funcionalidades :video_game:

- **Cadastro e Gerenciamento de Clientes:** Cadastro, consulta, atualização e exclusão de clientes.
- **Cadastro e Gerenciamento de Produtos:** Cadastro, consulta, atualização e exclusão de produtos, associando-os a categorias.
- **Cadastro e Gerenciamento de Categorias:** Cadastro, consulta, atualização e exclusão de categorias.
- **Criação e Atualização de Pedidos:** Criação de pedidos vinculados a clientes, com detalhes específicos para cada produto.
- **Autenticação e Autorização com JWT:** Segurança para acesso e operações sensíveis.
- **Criptografia de Dados Sensíveis:** Utilização de `Fernet` para criptografar informações sensíveis.

---
## Arquitetura :triangular_ruler: :straight_ruler:

O sistema é estruturado em uma arquitetura de camadas que separa responsabilidades e facilita a manutenção e escalabilidade. A aplicação usa o framework Flask para o backend e é desenvolvida com PostgreSQL como banco de dados relacional.

### Descrição da Arquitetura

- **Configuração**: Configurações de ambiente e variáveis sensíveis são carregadas de um arquivo `.env`.
- **Banco de Dados**: PostgreSQL, gerenciado pelo SQLAlchemy.
- **Autenticação**: Implementação de autenticação JWT para proteger endpoints e operações sensíveis.
- **Camadas da Aplicação**:
  - **Models**: Define a estrutura das tabelas e relacionamentos no banco de dados.
  - **Controllers**: Implementa a lógica de cada endpoint e orquestra as operações.
  - **Services**: Contém a lógica de negócios.
  - **Middlewares**: Configuração de CORS e autenticação.
  - **Rotas**: Gerencia as rotas da API e define os endpoints.

---

## Rotas - Endpoints :arrows_clockwise:

### Autenticação

#### Login
- **POST** `/login`
  - **Descrição**: Autentica o usuário e retorna um token JWT.
  - **Body**:
    ```json
    {
      "email": "string",
      "senha": "string"
    }
    ```
  - **Resposta**:
    ```json
    {
      "token": "string"
    }
    ```

---

### Clientes

#### Criar Cliente
- **POST** `/clientes`
  - **Descrição**: Cadastra um novo cliente.
  - **Body**:
    ```json
    {
      "nome": "string",
      "email": "string"
    }
    ```

#### Listar Clientes
- **GET** `/clientes`
  - **Descrição**: Lista todos os clientes.

#### Buscar Cliente por ID
- **GET** `/clientes/{id}`
  - **Descrição**: Busca um cliente específico pelo ID.

#### Atualizar Cliente
- **PUT** `/clientes/{id}`
  - **Descrição**: Atualiza as informações de um cliente.

#### Excluir Cliente
- **DELETE** `/clientes/{id}`
  - **Descrição**: Exclui um cliente específico.

---

### Produtos

#### Criar Produto
- **POST** `/produtos`
  - **Descrição**: Cadastra um novo produto.
  - **Body**:
    ```json
    {
      "nome": "string",
      "id_categoria": "string"
    }
    ```

#### Listar Produtos
- **GET** `/produtos`
  - **Descrição**: Lista todos os produtos.

#### Buscar Produto por ID
- **GET** `/produtos/{id}`
  - **Descrição**: Busca um produto específico pelo ID.

#### Atualizar Produto
- **PUT** `/produtos/{id}`
  - **Descrição**: Atualiza as informações de um produto.

#### Excluir Produto
- **DELETE** `/produtos/{id}`
  - **Descrição**: Exclui um produto específico.

---

### Categorias

#### Criar Categoria
- **POST** `/categorias`
  - **Descrição**: Cadastra uma nova categoria.

#### Listar Categorias
- **GET** `/categorias`
  - **Descrição**: Lista todas as categorias.

#### Buscar Categoria por ID
- **GET** `/categorias/{id}`
  - **Descrição**: Busca uma categoria específica pelo ID.

#### Atualizar Categoria
- **PUT** `/categorias/{id}`
  - **Descrição**: Atualiza as informações de uma categoria.

#### Excluir Categoria
- **DELETE** `/categorias/{id}`
  - **Descrição**: Exclui uma categoria específica.

---

### Pedidos

#### Criar Pedido
- **POST** `/pedidos`
  - **Descrição**: Cria um novo pedido para um cliente específico.
  - **Body**:
    ```json
    {
      "id_cliente": "string"
    }
    ```

#### Listar Pedidos
- **GET** `/pedidos`
  - **Descrição**: Lista todos os pedidos.

#### Buscar Pedido por ID
- **GET** `/pedidos/{id}`
  - **Descrição**: Busca um pedido específico pelo ID.

#### Atualizar Pedido
- **PUT** `/pedidos/{id}`
  - **Descrição**: Atualiza as informações de um pedido.

#### Excluir Pedido
- **DELETE** `/pedidos/{id}`
  - **Descrição**: Exclui um pedido específico.

---

### Detalhes do Pedido

#### Criar Detalhe do Pedido
- **POST** `/detalhe_pedidos`
  - **Descrição**: Adiciona um detalhe a um pedido específico.
  - **Body**:
    ```json
    {
      "id_pedido": "string",
      "id_produto": "string",
      "valor": "decimal",
      "desconto": "decimal"
    }
    ```

#### Listar Detalhes do Pedido
- **GET** `/detalhe_pedidos`
  - **Descrição**: Lista todos os detalhes dos pedidos.

#### Buscar Detalhe do Pedido por ID
- **GET** `/detalhe_pedidos/{id}`
  - **Descrição**: Busca um detalhe de pedido específico pelo ID.

#### Atualizar Detalhe do Pedido
- **PUT** `/detalhe_pedidos/{id}`
  - **Descrição**: Atualiza as informações de um detalhe do pedido.

#### Excluir Detalhe do Pedido
- **DELETE** `/detalhe_pedidos/{id}`
  - **Descrição**: Exclui um detalhe específico do pedido.

---

## Configuração e Instalação :gear:

### Criar e ativar ambiente virtual :white_check_mark:

```bash
$ python -m venv venv
```

**MacOS/Linux:**
```bash
$ source venv/bin/activate
```

**Windows:**
```bash
$ venv\Scripts\activate 
```

### Instalação das depedências :arrow_down_small:

```bash
$ pip install -r requirements.txt
```

### Executar migrações :arrow_forward:

```bash
$ flask db upgrade
```

### Executar app :arrow_forward:

**development:**
```bash
$ flask run
```

```bash
Running on http://127.0.0.1:5000/
```

## Linguagens, tecnologias, dependências e libs utilizadas :hammer_and_wrench: :gear: :books:

- [Python](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/installation/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Draw.io](https://www.drawio.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/s)
- [Marshmallow](https://marshmallow.readthedocs.io/en/stable/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/latest/)
- [Fernet - symmetric encryption](https://cryptography.io/en/latest/fernet/)
- [Postman](https://www.postman.com/downloads/)
- [Git](https://git-scm.com/downloads)
- [GitHub](https://github.com/)

...

