from flask import Flask, jsonify, request
from sqlalchemy.orm import joinedload

import sql_service
import nosql_service


from models import db, Venda
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

@app.route("/")
def index():
    return "Olá, mundo."


@app.route("/clientes", methods=["GET"])
def listar_clientes_route():
    clientes = sql_service.listar_clientes()
    return jsonify([{
        "id_cliente": c.id_cliente, 
        "nome": c.nome, 
        "email": c.email, 
        "cpf": c.cpf, 
        "data_nascimento": c.data_nascimento
    } for c in clientes])

@app.route("/clientes", methods=["POST"])
def criar_cliente_route():
    data = request.json
    if not all(k in data for k in ("nome", "email")):
        return jsonify({"erro": "Campos obrigatórios: nome, email"}), 400
    cliente = sql_service.criar_cliente(
        nome=data["nome"],
        email=data["email"],
        cpf=data.get("cpf"),
        data_nascimento=data["data_nascimento"]
    )
    total_clientes = len(sql_service.listar_clientes())
    nosql_service.registrar_dashboard_total(total_clientes)
    return jsonify({"id": cliente.id_cliente, "mensagem": "Cliente criado com sucesso"}), 201

@app.route("/clientes/<int:cliente_id>", methods=["DELETE"])
def deletar_cliente_route(cliente_id):
    
    cliente = sql_service.deletar_cliente(cliente_id)
    if not cliente: return jsonify({"erro": "Cliente não encontrado"}), 404
    total_clientes = len(sql_service.listar_clientes())
    nosql_service.registrar_dashboard_total(total_clientes)
    return jsonify({"mensagem": "Cliente deletado com sucesso"})

@app.route("/clientes/<int:cliente_id>", methods=["PUT"])
def atualizar_cliente_route(cliente_id):
    data = request.json
    cliente = sql_service.atualizar_cliente(
        cliente_id,
        nome=data.get("nome"),
        email=data.get("email"),
        cpf=data.get("cpf"),
        data_nascimento=data.get("data_nascimento")
    )
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    return jsonify({"mensagem": "Cliente atualizado com sucesso"})

@app.route("/clientes/<int:cliente_id>", methods=["GET"])
def obter_cliente_route(cliente_id):
    cliente = sql_service.obter_cliente(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    return jsonify({
        "id": cliente.id_cliente,
        "nome": cliente.nome,
        "email": cliente.email,
        "cpf": cliente.cpf,
        "data_nascimento": cliente.data_nascimento.strftime("%d-%m-%Y")
    })

@app.route("/produtos", methods=["GET"])
def get_produtos():
    produtos = sql_service.listar_produtos()
    return jsonify([{"id": p.id_produto, "nome": p.nome, "preco": p.preco, "descricao": p.descricao, "categoria": p.categoria} for p in produtos])

@app.route("/produtos", methods=["POST"])
def post_produto():
    data = request.json
    produto = sql_service.criar_produto(data["nome"], data["preco"], data["descricao"], data["categoria"])
    total_produtos = len(sql_service.listar_produtos())
    nosql_service.registrar_dashboard_produtos(total_produtos)
    return jsonify({"id": produto.id_produto}), 201

@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def deletar_produto_route(produto_id):
    produto = sql_service.deletar_produto(produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    total_produtos = len(sql_service.listar_produtos())
    nosql_service.registrar_dashboard_produtos(total_produtos)
    return jsonify({"mensagem": "Produto deletado com sucesso"})

@app.route("/produtos/<int:produto_id>", methods=["GET"])
def get_produto(produto_id):
    produto = sql_service.obter_produto(produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({"id": produto.id_produto, "nome": produto.nome, "preco": produto.preco, "descricao": produto.descricao, "categoria": produto.categoria})

@app.route("/produtos/<int:produto_id>", methods=["PUT"])
def put_produto(produto_id):
    data = request.json
    produto = sql_service.atualizar_produto(
        produto_id,
        nome=data.get("nome"),
        preco=data.get("preco"),
        descricao=data.get("descricao"),
        categoria=data.get("categoria")
    )
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({"mensagem": "Produto atualizado com sucesso"})



@app.route("/vendas", methods=["GET"])
def listar_vendas_route():
    pedidos = Venda.query.options(joinedload(Venda.cliente), joinedload(Venda.produto)).all()
    result = []
    for v in pedidos:
        result.append({
            "id": v.id_pedido, "data_pedido": v.data_pedido,
            "cliente": v.cliente.nome if v.cliente else None,
            "produto": v.produto.nome if v.produto else None,
            "valor_total": v.valor_total
        })
    return jsonify(result)

@app.route("/vendas", methods=["POST"])
def post_venda():
    data = request.json
    cliente = sql_service.obter_cliente(data["id_cliente"])
    produto = sql_service.obter_produto(data["id_produto"])
    if not cliente or not produto:
        return jsonify({"erro": "Cliente ou Produto não encontrado"}), 404

    venda = sql_service.criar_venda(data["id_cliente"], data["id_produto"], data["valor_total"])
    if not venda:
        return jsonify({"erro": "Erro ao criar venda"}), 400
    

    total_vendas = len(sql_service.listar_vendas())
    nosql_service.registrar_dashboard_vendas(total_vendas)
    
    nosql_service.registrar_venda_por_produto(produto.id_produto, produto.nome)
   

    return jsonify({"id": venda.id_pedido}), 201


@app.route("/dashboard/total_clientes", methods=["GET"])
def dashboard_total_clientes():
    total = nosql_service.obter_dashboard_total()
    return jsonify({"total_clientes": total})

@app.route("/dashboard/total_produtos", methods=["GET"])
def dashboard_total_produtos():
    doc = nosql_service.obter_documento("dashboard", {"_id": "total_produtos"})
    total = doc["total"] if doc else 0
    return jsonify({"total_produtos": total})

@app.route("/dashboard/total_vendas", methods=["GET"])
def dashboard_total_vendas():
    doc = nosql_service.obter_documento("dashboard", {"_id": "total_vendas"})
    total = doc["total"] if doc else 0
    return jsonify({"total_vendas": total})


@app.route("/dashboard/produto_mais_vendido", methods=["GET"])
def dashboard_produto_mais_vendido():
    produto = nosql_service.obter_produto_mais_vendido()
    if produto:
        
        produto['_id'] = str(produto['_id'])
        return jsonify(produto)
    return jsonify({"mensagem": "Nenhuma venda registrada ainda."})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
