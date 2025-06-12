from usuario import *
from livro import *
from usuario import Usuario
from livro import Livro
from resenha import *
from resenha import Resenha
from neo4j_amizades import Neo4jRedeAmizades

neo4j = Neo4jRedeAmizades("bolt://54.147.84.236:7687", "neo4j", "minority-major-towns")

def menu():
    while True:
        print("\n--- MENU ---")
        print("1 - Cadastrar Usuário")
        print("2 - Listar Usuários")
        print("3 - Editar Usuário")
        print("4 - Remover Usuário")
        print("5 - Cadastrar Livro")
        print("6 - Listar Livros")
        print("7 - Editar Livro")
        print("8 - Remover Livro")
        print("9 - Escrever Resenha")
        print("10 - Listar Resenhas")
        print("11 - Adicionar livro ao histórico de leitura")
        print("12 - Ver histórico de leitura de um usuário")
        print("13 - Criar amizade entre usuários")
        print("14 - Listar amigos de um usuário")
        print("15 - Recomendar livros com base no histórico")
        print("16 - Recomendar livros lidos por amigos")
        print("17 - Adicionar gosto literário ao usuário")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            usuario = Usuario(nome, email)
            create_usuario(usuario)
            neo4j.criar_usuario(email, nome)

        elif opcao == "2":
            for u in read_usuarios():
                print(u)

        elif opcao == "3":
            email = input("Email do usuário a editar: ")
            novo_nome = input("Novo nome: ")
            update_usuario(email, {"nome": novo_nome})

        elif opcao == "4":
            email = input("Email do usuário a remover: ")
            delete_usuario(email)

        elif opcao == "5":
            titulo = input("Título: ")
            autor = input("Autor: ")
            genero = input("Gênero: ")
            sinopse = input("Sinopse: ")
            livro = Livro(titulo, autor, genero, sinopse)
            create_livro(livro)

        elif opcao == "6":
            for l in read_livros():
                print(l)

        elif opcao == "7":
            titulo = input("Título do livro a editar: ")
            novo_autor = input("Novo autor: ")
            update_livro(titulo, {"autor": novo_autor})

        elif opcao == "8":
            titulo = input("Título do livro a remover: ")
            delete_livro(titulo)
            
        elif opcao == "9":
            email = input("Email do usuário: ")
            titulo = input("Título do livro: ")
            nota = float(input("Nota (0 a 10): "))
            comentario = input("Comentário: ")
            resenha = Resenha(email, titulo, nota, comentario)
            create_resenha(resenha)

        elif opcao == "10":
            resenhas = read_resenhas()
            for r in resenhas:
                print(f"\nLivro: {r['livro_titulo']}\nUsuário: {r['usuario_email']}\nNota: {r['nota']}\nComentário: {r['comentario']}\nData: {r['data']}")

        elif opcao == "11":
             email = input("Email do usuário: ")
             titulo = input("Título do livro: ")
             adicionar_livro_ao_historico(email, titulo)

        elif opcao == "12":
             email = input("Email do usuário: ")
             listar_historico_leitura(email)
        
        elif opcao == "13":
             email1 = input("Email do primeiro usuário: ")
             email2 = input("Email do segundo usuário: ")
             neo4j.adicionar_amizade(email1, email2)  
             
        elif opcao == "14":
             email = input("Email do usuário: ")
             neo4j.exibir_amigos_do_usuario(email)
            
        elif opcao == "15":
             email = input("Email do usuário: ")
             recomendar_livros(email)

        elif opcao == "16":
             email = input("Email do usuário: ")
             recomendar_livros_amigos(email, neo4j)
             
        elif opcao == "17":
             email = input("Email do usuário: ")
             genero = input("Gênero favorito: ")
             autor = input("Autor favorito: ")
             neo4j.mapear_gosto_usuario(email, genero, autor)

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")

menu()
neo4j.close()
