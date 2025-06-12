from database import db
from neo4j_amizades import Neo4jRedeAmizades

neo4j = Neo4jRedeAmizades("bolt://54.147.84.236:7687", "neo4j", "minority-major-towns")

# Classe Usuario e funções CRUD ficam iguais
class Usuario:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
        self.livros_lidos = []

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "livros_lidos": self.livros_lidos
        }

def adicionar_livro_ao_historico(email, titulo_livro):
    livro = db.livros.find_one({"titulo": titulo_livro})
    if not livro:
        print("Livro não encontrado.")
        return

    # Adiciona no MongoDB
    db.usuarios.update_one(
        {"email": email},
        {"$addToSet": {"livros_lidos": titulo_livro}}
    )

    # Adiciona no Neo4j
    genero = livro.get("genero", "Desconhecido")
    autor = livro.get("autor", "Desconhecido")
    neo4j.registrar_leitura(email, titulo_livro, genero, autor)

    print("Livro adicionado ao histórico (MongoDB e Neo4j)!")


def listar_historico_leitura(email):
    usuario = db.usuarios.find_one({"email": email})
    if not usuario:
        print("Usuário não encontrado.")
        return

    print(f"\nHistórico de leitura de {usuario['nome']}:")
    for livro in usuario.get("livros_lidos", []):
        print(f"- {livro}")

def recomendar_livros(email):
    usuario = db.usuarios.find_one({"email": email})
    if not usuario:
        print("Usuário não encontrado.")
        return

    livros_lidos = usuario.get("livros_lidos", [])
    if not livros_lidos:
        print("Usuário ainda não leu nenhum livro.")
        return

    livros = list(db.livros.find({"titulo": {"$in": livros_lidos}}))
    generos_lidos = list(set([livro["genero"] for livro in livros]))

    recomendados = list(db.livros.find({
        "genero": {"$in": generos_lidos},
        "titulo": {"$nin": livros_lidos}
    }))

    if not recomendados:
        print("Nenhum livro para recomendar no momento.")
        return

    print(f"\n📚 Recomendações para {usuario['nome']}:")
    for livro in recomendados:
        print(f"- {livro['titulo']} ({livro['autor']}) — Gênero: {livro['genero']}")

# Ajuste importante: a função receberá a instância neo4j por parâmetro
def recomendar_livros_amigos(email_usuario, neo4j):
    usuario = db.usuarios.find_one({"email": email_usuario})
    if not usuario:
        print("Usuário não encontrado no MongoDB.")
        return

    livros_lidos_usuario = usuario.get("livros_lidos", [])

    amigos = neo4j.listar_amigos(email_usuario)
    if not amigos:
        print("O usuário não possui amigos cadastrados no grafo.")
        return

    livros_recomendados = set()

    for amigo in amigos:
        amigo_email = amigo["email"]
        amigo_data = db.usuarios.find_one({"email": amigo_email})
        if amigo_data:
            for livro in amigo_data.get("livros_lidos", []):
                if livro not in livros_lidos_usuario:
                    livros_recomendados.add(livro)

    if livros_recomendados:
        print(f"\n📚 Livros lidos pelos amigos de {email_usuario}, que ele ainda não leu:")
        for titulo in livros_recomendados:
            livro = db.livros.find_one({"titulo": titulo})
            if livro:
                print(f"- {livro['titulo']} ({livro['autor']}) — Gênero: {livro['genero']}")
    else:
        print("Nenhum livro novo encontrado entre os amigos.")

# CRUD do usuário
def create_usuario(usuario):
    db.usuarios.insert_one(usuario.to_dict())

def read_usuarios():
    return list(db.usuarios.find())

def update_usuario(email, novos_dados):
    db.usuarios.update_one({"email": email}, {"$set": novos_dados})

def delete_usuario(email):
    db.usuarios.delete_one({"email": email})