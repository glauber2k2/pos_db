from pymongo import MongoClient
from config import MONGO_URL, MONGO_DB

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=2000)
    client.server_info()
    mongo_db = client[MONGO_DB]
    dashboard_collection = mongo_db["dashboard"]
    vendas_produto_collection = mongo_db["vendas_por_produto"] # Nova coleção
    mongo_connected = True
    print("[MongoDB] Conectado com sucesso!")
except Exception as e:
    print(f"[MongoDB] Aviso: não foi possível conectar: {e}")
    mongo_db = None
    dashboard_collection = None
    vendas_produto_collection = None
    mongo_connected = False

def obter_documento(collection_name, filtro):
    if mongo_connected:
        collection = mongo_db[collection_name]
        return collection.find_one(filtro)
    return None

def registrar_dashboard_total(total_clientes):
    if mongo_connected:
        dashboard_collection.update_one(
            {"_id": "total_clientes"},
            {"$set": {"total": total_clientes}},
            upsert=True
        )

def obter_dashboard_total():
    if mongo_connected:
        doc = dashboard_collection.find_one({"_id": "total_clientes"})
        return doc["total"] if doc else 0
    return 0

def registrar_dashboard_produtos(total_produtos):
    if mongo_connected:
        dashboard_collection.update_one(
            {"_id": "total_produtos"},
            {"$set": {"total": total_produtos}},
            upsert=True
        )

def registrar_dashboard_vendas(total_vendas):
    if mongo_connected:
        dashboard_collection.update_one(
            {"_id": "total_vendas"},
            {"$set": {"total": total_vendas}},
            upsert=True
        )


def registrar_venda_por_produto(id_produto, nome_produto):
    if mongo_connected:
        
        vendas_produto_collection.update_one(
            {"_id": id_produto},
            {
                "$inc": {"total_vendas": 1},
                "$set": {"nome_produto": nome_produto}
            },
            upsert=True
        )


def obter_produto_mais_vendido():
    if mongo_connected:
        
        produto = vendas_produto_collection.find().sort("total_vendas", -1).limit(1)
        try:
            return list(produto)[0]
        except IndexError:
            return None 
    return None