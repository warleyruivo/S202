from database import Database
from teacher_crud import TeacherCRUD

class CLI:
    def __init__(self):
        self.db = Database("bolt://3.91.47.130:7687", "neo4j", "2")
        self.crud = TeacherCRUD(self.db)

    def menu(self):
        while True:
            print("\n--- MENU PROFESSORES ---")
            print("1. Criar professor")
            print("2. Ler professor")
            print("3. Atualizar CPF")
            print("4. Deletar professor")
            print("0. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                name = input("Nome: ")
                ano = int(input("Ano de nascimento: "))
                cpf = input("CPF: ")
                self.crud.create(name, ano, cpf)

            elif opcao == "2":
                name = input("Nome do professor: ")
                result = self.crud.read(name)
                if result:
                    for r in result:
                        print(f"Nome: {r['nome']}, Ano Nasc: {r['nascimento']}, CPF: {r['cpf']}")
                else:
                    print("Professor não encontrado.")

            elif opcao == "3":
                name = input("Nome do professor: ")
                newCpf = input("Novo CPF: ")
                result = self.crud.update(name, newCpf)
                if result:
                    for r in result:
                        print(f"CPF do professor {r['name']} atualizado para {r['cpf']}")
                else:
                    print("Professor não encontrado para atualização.")

            elif opcao == "4":
                name = input("Nome do professor: ")
                self.crud.delete(name)

            elif opcao == "0":
                print("Encerrando programa...")
                self.db.close()
                break

            else:
                print("Opção inválida.")

if __name__ == "__main__":
    app = CLI()
    app.menu()
