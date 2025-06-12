from neo4j import GraphDatabase
from database import db 

class Neo4jRedeAmizades:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def criar_usuario(self, email, nome=None):
        with self.driver.session() as session:
            session.run(
                """
                MERGE (u:Usuario {email: $email})
                ON CREATE SET u.nome = $nome
                """,
                email=email,
                nome=nome
            )

    def adicionar_amizade(self, email1, email2):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (a:Usuario {email: $email1}), (b:Usuario {email: $email2})
                MERGE (a)-[:AMIGO]->(b)
                MERGE (b)-[:AMIGO]->(a)
                """,
                email1=email1,
                email2=email2
            )
            print(f"Amizade criada entre '{email1}' e '{email2}'.")
            
    def listar_amigos(self, email):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:Usuario {email: $email})-[:AMIGO]->(amigo)
                RETURN amigo.nome AS nome, amigo.email AS email
                """,
                email=email
            )
            amigos = result.data()
            return amigos
        
    def exibir_amigos_do_usuario(self, email):
        amigos = self.listar_amigos(email)
        if not amigos:
            print(f"O usuário '{email}' não possui amigos cadastrados.")
        else:
            print(f"Amigos de '{email}':")
            for a in amigos:
                print(f" - {a['nome']} ({a['email']})")
                
    def registrar_leitura(self, email_usuario, titulo_livro, genero, autor):
        with self.driver.session() as session:
            session.run(
                """
                MERGE (u:Usuario {email: $email})
                MERGE (l:Livro {titulo: $titulo})
                MERGE (g:Genero {nome: $genero})
                MERGE (a:Autor {nome: $autor})
                MERGE (u)-[:LEU]->(l)
                MERGE (l)-[:PERTENCE_A]->(g)
                MERGE (l)-[:ESCRITO_POR]->(a)
                """,
                email=email_usuario,
                titulo=titulo_livro,
                genero=genero,
                autor=autor
        )
    def mapear_gosto_usuario(self, email_usuario, genero, autor):
        with self.driver.session() as session:
            session.run("""
                MERGE (u:Usuario {email: $email})
                MERGE (g:Genero {nome: $genero})
                MERGE (a:Autor {nome: $autor})
                MERGE (u)-[:GOSTA_DE]->(g)
                MERGE (u)-[:GOSTA_DE_AUTOR]->(a)
            """, email=email_usuario, genero=genero, autor=autor)
        
            
    
