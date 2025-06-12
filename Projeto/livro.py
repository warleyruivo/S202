from database import db

#Class definition for Livro
class Livro:
    def __init__(self, titulo, autor, genero, sinopse):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.sinopse = sinopse

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "genero": self.genero,
            "sinopse": self.sinopse
        }

#CRUD operations for Livro
def create_livro(livro):
    db.livros.insert_one(livro.to_dict())

def read_livros():
    return list(db.livros.find())

def update_livro(titulo, novos_dados):
    db.livros.update_one({"titulo": titulo}, {"$set": novos_dados})

def delete_livro(titulo):
    db.livros.delete_one({"titulo": titulo})
