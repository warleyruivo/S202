from database import db
from datetime import datetime

class Resenha:
    def __init__(self, usuario_email, livro_titulo, nota, comentario):
        self.usuario_email = usuario_email
        self.livro_titulo = livro_titulo
        self.nota = nota
        self.comentario = comentario
        self.data = datetime.now()

    def to_dict(self):
        return {
            "usuario_email": self.usuario_email,
            "livro_titulo": self.livro_titulo,
            "nota": self.nota,
            "comentario": self.comentario,
            "data": self.data
        }

# CRUD de Resenhas
def create_resenha(resenha):
    # Verifica se o usuário e o livro existem
    usuario = db.usuarios.find_one({"email": resenha.usuario_email})
    livro = db.livros.find_one({"titulo": resenha.livro_titulo})

    if not usuario:
        print("Erro: usuário não encontrado.")
        return

    if not livro:
        print("Erro: livro não encontrado.")
        return

    db.resenhas.insert_one(resenha.to_dict())
    print("Resenha salva com sucesso!")

def read_resenhas():
    return list(db.resenhas.find())
