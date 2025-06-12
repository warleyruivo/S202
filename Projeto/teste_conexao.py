from database import db

try:
    # Tentativa de listar coleções existentes
    colecoes = db.list_collection_names()
    print("Conexão bem-sucedida!")
    print("Coleções disponíveis:", colecoes)
except Exception as e:
    print("Erro ao conectar ao MongoDB:", e)
