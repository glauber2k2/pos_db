# Projeto Final – Pós-Graduação em Desenvolvimento Web (2025)

API RESTful desenvolvida em **Flask** para gerenciar clientes, produtos e vendas, utilizando uma arquitetura híbrida com bancos de dados **SQL (MySQL)** e **NoSQL (MongoDB)**. Trabalho final da disciplina de **Banco de Dados**.

---

## Autores
- Diego Altenkirch Kabbaz  
- Glauber de Oliveira Monteiro  

---

## Funcionalidades

### 1. Banco de Dados Relacional – MySQL
MySQL é usado como fonte primária de dados para as operações transacionais:
- CRUD de **Clientes** – GET, POST, PUT, DELETE  
- CRUD de **Produtos** – GET, POST, PUT, DELETE  
- CRUD de **Vendas/Pedidos** – GET, POST, PUT, DELETE  

### 2. Banco de Dados NoSQL – MongoDB
MongoDB armazena dados consolidados para dashboards:
- **Total de Clientes** – contagem atualizada em tempo real  
- **Total de Produtos** – contagem atualizada em tempo real  
- **Total de Vendas** – contagem atualizada em tempo real  
- **Produto Mais Vendido** – identificação do item com maior número de vendas  

---

## Como Executar o Projeto

### Pré-requisitos
- Python 3.8+  
- Servidor MySQL (XAMPP, WAMP, Docker etc.)  
- Servidor MongoDB  
- Git

### Passos
1. **Clonar o repositório**
   ```bash
   git clone https://github.com/glauber2k2/pos_db.git
   cd pos_db
   ```

2. **Criar e ativar ambiente virtual**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar os bancos**
   - Criar no MySQL um BD vazio chamado `bdpos`.
   - Ajustar `config.py` se suas credenciais forem diferentes.

5. **Criar tabelas no MySQL**
   ```python
   from main import app, db
   with app.app_context():
       db.create_all()
   exit()
   ```

6. **Iniciar a aplicação**
   ```bash
   python main.py
   ```
   O servidor estará em: **http://127.0.0.1:5000**

---

## Endpoints da API

### Clientes
| Método | Rota          | Descrição   |
|--------|---------------|-------------|
| GET    | /clientes      | Lista todos |
| GET    | /clientes/<id> | Detalhe     |
| POST   | /clientes      | Cria novo   |
| PUT    | /clientes/<id> | Atualiza    |
| DELETE | /clientes/<id> | Remove      |

### Produtos
| Método | Rota          | Descrição   |
|--------|---------------|-------------|
| GET    | /produtos      | Lista todos |
| GET    | /produtos/<id> | Detalhe     |
| POST   | /produtos      | Cria novo   |
| PUT    | /produtos/<id> | Atualiza    |
| DELETE | /produtos/<id> | Remove      |

### Vendas
| Método | Rota       | Descrição   |
|--------|------------|-------------|
| GET    | /vendas     | Lista todas |
| POST   | /vendas     | Cria nova   |
| PUT    | /vendas/<id>| Atualiza    |
| DELETE | /vendas/<id>| Remove      |

### Dashboard (MongoDB)
- **GET /dashboard/total_clientes**  
- **GET /dashboard/total_produtos**  
- **GET /dashboard/total_vendas**  
- **GET /dashboard/produto_mais_vendido**
