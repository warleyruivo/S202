import tkinter as tk
from tkinter import ttk, messagebox
from usuario import *
from livro import *
from resenha import *
from usuario import Usuario
from livro import Livro
from resenha import Resenha
from neo4j_amizades import Neo4jRedeAmizades

neo4j = Neo4jRedeAmizades("bolt://54.147.84.236:7687", "neo4j", "minority-major-towns")

class App(tk.Tk):
    def __init__(self, neo4j_driver):
        super().__init__()
        self.neo4j = neo4j_driver
        self.title("Rede Social para Leitores")
        self.geometry("900x600")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both")

        # Instanciando caminhos das abas, repassando neo4j quando necessário
        self.usuarios_tab = UsuariosTab(self.notebook)
        self.notebook.add(self.usuarios_tab, text="Usuários")

        self.livros_tab = LivrosTab(self.notebook)
        self.notebook.add(self.livros_tab, text="Livros")

        self.resenhas_tab = ResenhasTab(self.notebook)
        self.notebook.add(self.resenhas_tab, text="Resenhas")

        # Abas que usam Neo4j recebem o driver
        self.amigos_tab = AmigosTab(self.notebook, self.neo4j)
        self.notebook.add(self.amigos_tab, text="Amigos")

        self.recomendacoes_tab = RecomendacoesTab(self.notebook, self.neo4j)
        self.notebook.add(self.recomendacoes_tab, text="Recomendações")

    def close(self):
        self.neo4j.close()
        self.destroy()

class UsuariosTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Frames para organização
        frm_form = ttk.Frame(self)
        frm_form.pack(padx=10, pady=10, fill='x')

        frm_list = ttk.Frame(self)
        frm_list.pack(padx=10, pady=10, fill='both', expand=True)

        # Formulario para criar/editar usuário
        ttk.Label(frm_form, text="Nome:").grid(row=0, column=0, sticky='w', pady=2)
        self.entry_nome = ttk.Entry(frm_form, width=30)
        self.entry_nome.grid(row=0, column=1, pady=2)

        ttk.Label(frm_form, text="Email:").grid(row=1, column=0, sticky='w', pady=2)
        self.entry_email = ttk.Entry(frm_form, width=30)
        self.entry_email.grid(row=1, column=1, pady=2)

        self.btn_criar = ttk.Button(frm_form, text="Criar Usuário", command=self.criar_usuario)
        self.btn_criar.grid(row=2, column=0, pady=10)

        self.btn_editar = ttk.Button(frm_form, text="Editar Usuário", command=self.editar_usuario)
        self.btn_editar.grid(row=2, column=1, pady=10)

        self.btn_remover = ttk.Button(frm_form, text="Remover Usuário", command=self.remover_usuario)
        self.btn_remover.grid(row=2, column=2, pady=10)

        # Área para listar usuários
        self.text_usuarios = tk.Text(frm_list, height=20, wrap='word')
        self.text_usuarios.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frm_list, command=self.text_usuarios.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_usuarios.config(yscrollcommand=scrollbar.set)

        self.listar_usuarios()

    def criar_usuario(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        if not nome or not email:
            messagebox.showwarning("Aviso", "Nome e Email são obrigatórios.")
            return
        usuario = Usuario(nome, email)
        create_usuario(usuario)
        neo4j.criar_usuario(email, nome)
        messagebox.showinfo("Sucesso", f"Usuário {nome} criado.")
        self.limpar_campos()
        self.listar_usuarios()

    def editar_usuario(self):
        email = self.entry_email.get().strip()
        novo_nome = self.entry_nome.get().strip()
        if not email or not novo_nome:
            messagebox.showwarning("Aviso", "Email e Novo Nome são obrigatórios para editar.")
            return
        update_usuario(email, {"nome": novo_nome})
        messagebox.showinfo("Sucesso", "Usuário atualizado.")
        self.limpar_campos()
        self.listar_usuarios()

    def remover_usuario(self):
        email = self.entry_email.get().strip()
        if not email:
            messagebox.showwarning("Aviso", "Email é obrigatório para remover.")
            return
        delete_usuario(email)
        messagebox.showinfo("Sucesso", "Usuário removido.")
        self.limpar_campos()
        self.listar_usuarios()

    def listar_usuarios(self):
        usuarios = read_usuarios()
        self.text_usuarios.delete('1.0', tk.END)
        if usuarios:
            for u in usuarios:
                self.text_usuarios.insert(tk.END, f"{u}\n")
        else:
            self.text_usuarios.insert(tk.END, "Nenhum usuário encontrado.")

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

class LivrosTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        frm_form = ttk.Frame(self)
        frm_form.pack(padx=10, pady=10, fill='x')

        frm_list = ttk.Frame(self)
        frm_list.pack(padx=10, pady=10, fill='both', expand=True)

        ttk.Label(frm_form, text="Título:").grid(row=0, column=0, sticky='w', pady=2)
        self.entry_titulo = ttk.Entry(frm_form, width=40)
        self.entry_titulo.grid(row=0, column=1, pady=2)

        ttk.Label(frm_form, text="Autor:").grid(row=1, column=0, sticky='w', pady=2)
        self.entry_autor = ttk.Entry(frm_form, width=40)
        self.entry_autor.grid(row=1, column=1, pady=2)

        ttk.Label(frm_form, text="Gênero:").grid(row=2, column=0, sticky='w', pady=2)
        self.entry_genero = ttk.Entry(frm_form, width=40)
        self.entry_genero.grid(row=2, column=1, pady=2)

        ttk.Label(frm_form, text="Sinopse:").grid(row=3, column=0, sticky='nw', pady=2)
        self.text_sinopse = tk.Text(frm_form, width=40, height=5)
        self.text_sinopse.grid(row=3, column=1, pady=2)

        self.btn_criar = ttk.Button(frm_form, text="Criar Livro", command=self.criar_livro)
        self.btn_criar.grid(row=4, column=0, pady=10)

        self.btn_editar = ttk.Button(frm_form, text="Editar Livro", command=self.editar_livro)
        self.btn_editar.grid(row=4, column=1, pady=10)

        self.btn_remover = ttk.Button(frm_form, text="Remover Livro", command=self.remover_livro)
        self.btn_remover.grid(row=4, column=2, pady=10)

        # Área para listar livros
        self.text_livros = tk.Text(frm_list, height=20, wrap='word')
        self.text_livros.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frm_list, command=self.text_livros.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_livros.config(yscrollcommand=scrollbar.set)

        self.listar_livros()

    def criar_livro(self):
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        genero = self.entry_genero.get().strip()
        sinopse = self.text_sinopse.get("1.0", tk.END).strip()

        if not titulo or not autor:
            messagebox.showwarning("Aviso", "Título e Autor são obrigatórios.")
            return

        livro = Livro(titulo, autor, genero, sinopse)
        create_livro(livro)
        messagebox.showinfo("Sucesso", f"Livro '{titulo}' criado.")
        self.limpar_campos()
        self.listar_livros()

    def editar_livro(self):
        titulo = self.entry_titulo.get().strip()
        novo_autor = self.entry_autor.get().strip()
        novo_genero = self.entry_genero.get().strip()
        nova_sinopse = self.text_sinopse.get("1.0", tk.END).strip()

        if not titulo:
            messagebox.showwarning("Aviso", "Título do livro é obrigatório para editar.")
            return

        novos_dados = {}
        if novo_autor:
            novos_dados["autor"] = novo_autor
        if novo_genero:
            novos_dados["genero"] = novo_genero
        if nova_sinopse:
            novos_dados["sinopse"] = nova_sinopse

        if not novos_dados:
            messagebox.showwarning("Aviso", "Pelo menos um campo deve ser preenchido para atualizar.")
            return

        update_livro(titulo, novos_dados)
        messagebox.showinfo("Sucesso", f"Livro '{titulo}' atualizado.")
        self.limpar_campos()
        self.listar_livros()

    def remover_livro(self):
        titulo = self.entry_titulo.get().strip()
        if not titulo:
            messagebox.showwarning("Aviso", "Título do livro é obrigatório para remover.")
            return
        delete_livro(titulo)
        messagebox.showinfo("Sucesso", f"Livro '{titulo}' removido.")
        self.limpar_campos()
        self.listar_livros()

    def listar_livros(self):
        livros = read_livros()
        self.text_livros.delete('1.0', tk.END)
        if livros:
            for l in livros:
                self.text_livros.insert(tk.END, f"Título: {l['titulo']}\nAutor: {l['autor']}\nGênero: {l.get('genero','')}\nSinopse: {l.get('sinopse','')}\n{'-'*40}\n")
        else:
            self.text_livros.insert(tk.END, "Nenhum livro encontrado.")

    def limpar_campos(self):
        self.entry_titulo.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_genero.delete(0, tk.END)
        self.text_sinopse.delete("1.0", tk.END)

class ResenhasTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        frm_form = ttk.Frame(self)
        frm_form.pack(padx=10, pady=10, fill='x')

        frm_list = ttk.Frame(self)
        frm_list.pack(padx=10, pady=10, fill='both', expand=True)

        ttk.Label(frm_form, text="Email do usuário:").grid(row=0, column=0, sticky='w', pady=2)
        self.entry_email = ttk.Entry(frm_form, width=40)
        self.entry_email.grid(row=0, column=1, pady=2)

        ttk.Label(frm_form, text="Título do livro:").grid(row=1, column=0, sticky='w', pady=2)
        self.entry_titulo = ttk.Entry(frm_form, width=40)
        self.entry_titulo.grid(row=1, column=1, pady=2)

        ttk.Label(frm_form, text="Nota (0 a 10):").grid(row=2, column=0, sticky='w', pady=2)
        self.entry_nota = ttk.Entry(frm_form, width=10)
        self.entry_nota.grid(row=2, column=1, pady=2, sticky='w')

        ttk.Label(frm_form, text="Comentário:").grid(row=3, column=0, sticky='nw', pady=2)
        self.text_comentario = tk.Text(frm_form, width=40, height=5)
        self.text_comentario.grid(row=3, column=1, pady=2)

        self.btn_criar = ttk.Button(frm_form, text="Criar Resenha", command=self.criar_resenha)
        self.btn_criar.grid(row=4, column=0, columnspan=2, pady=10)

        # Área para listar resenhas
        self.text_resenhas = tk.Text(frm_list, height=20, wrap='word')
        self.text_resenhas.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frm_list, command=self.text_resenhas.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_resenhas.config(yscrollcommand=scrollbar.set)

        self.listar_resenhas()

    def criar_resenha(self):
        email = self.entry_email.get().strip()
        titulo = self.entry_titulo.get().strip()
        nota_str = self.entry_nota.get().strip()
        comentario = self.text_comentario.get("1.0", tk.END).strip()

        if not email or not titulo or not nota_str:
            messagebox.showwarning("Aviso", "Email, título do livro e nota são obrigatórios.")
            return

        try:
            nota = float(nota_str)
            if nota < 0 or nota > 10:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Aviso", "Nota deve ser um número entre 0 e 10.")
            return

        resenha = Resenha(email, titulo, nota, comentario)
        create_resenha(resenha)
        messagebox.showinfo("Sucesso", f"Resenha para '{titulo}' criada.")
        self.limpar_campos()
        self.listar_resenhas()

    def listar_resenhas(self):
        resenhas = read_resenhas()
        self.text_resenhas.delete('1.0', tk.END)
        if resenhas:
            for r in resenhas:
                self.text_resenhas.insert(
                    tk.END,
                    f"Livro: {r['livro_titulo']}\nUsuário: {r['usuario_email']}\nNota: {r['nota']}\nComentário: {r['comentario']}\nData: {r['data']}\n{'-'*40}\n"
                )
        else:
            self.text_resenhas.insert(tk.END, "Nenhuma resenha encontrada.")

    def limpar_campos(self):
        self.entry_email.delete(0, tk.END)
        self.entry_titulo.delete(0, tk.END)
        self.entry_nota.delete(0, tk.END)
        self.text_comentario.delete("1.0", tk.END)

class AmigosTab(ttk.Frame):
    def __init__(self, parent, neo4j):
        super().__init__(parent)
        self.neo4j = neo4j

        frm_form = ttk.Frame(self)
        frm_form.pack(padx=10, pady=10, fill='x')

        frm_list = ttk.Frame(self)
        frm_list.pack(padx=10, pady=10, fill='both', expand=True)

        # Formulário para criar amizade
        ttk.Label(frm_form, text="Email do Usuário 1:").grid(row=0, column=0, sticky='w', pady=2)
        self.entry_email1 = ttk.Entry(frm_form, width=40)
        self.entry_email1.grid(row=0, column=1, pady=2)

        ttk.Label(frm_form, text="Email do Usuário 2:").grid(row=1, column=0, sticky='w', pady=2)
        self.entry_email2 = ttk.Entry(frm_form, width=40)
        self.entry_email2.grid(row=1, column=1, pady=2)

        self.btn_adicionar = ttk.Button(frm_form, text="Adicionar Amizade", command=self.adicionar_amizade)
        self.btn_adicionar.grid(row=2, column=0, columnspan=2, pady=10)

        # Formulário para listar amigos
        ttk.Label(frm_form, text="Email para listar amigos:").grid(row=3, column=0, sticky='w', pady=2)
        self.entry_email_listar = ttk.Entry(frm_form, width=40)
        self.entry_email_listar.grid(row=3, column=1, pady=2)

        self.btn_listar = ttk.Button(frm_form, text="Listar Amigos", command=self.listar_amigos)
        self.btn_listar.grid(row=4, column=0, columnspan=2, pady=10)

        # Área para mostrar lista de amigos e mensagens
        self.text_resultado = tk.Text(frm_list, height=15, wrap='word')
        self.text_resultado.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frm_list, command=self.text_resultado.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_resultado.config(yscrollcommand=scrollbar.set)

    def adicionar_amizade(self):
        email1 = self.entry_email1.get().strip()
        email2 = self.entry_email2.get().strip()
        if not email1 or not email2:
            messagebox.showwarning("Aviso", "Por favor, preencha ambos os emails.")
            return
        if email1 == email2:
            messagebox.showwarning("Aviso", "Os emails devem ser diferentes.")
            return

        try:
            self.neo4j.adicionar_amizade(email1, email2)
            messagebox.showinfo("Sucesso", f"Amizade criada entre {email1} e {email2}.")
            self.limpar_campos_amistade()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar amizade:\n{e}")

    def listar_amigos(self):
        email = self.entry_email_listar.get().strip()
        if not email:
            messagebox.showwarning("Aviso", "Por favor, insira o email para listar amigos.")
            return

        try:
            amigos = self.neo4j.listar_amigos(email)
            self.text_resultado.delete('1.0', tk.END)
            if amigos:
                self.text_resultado.insert(tk.END, f"Amigos de {email}:\n\n")
                for amigo in amigos:
                    self.text_resultado.insert(tk.END, f"- {amigo['nome']} ({amigo['email']})\n")
            else:
                self.text_resultado.insert(tk.END, f"O usuário {email} não possui amigos cadastrados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar amigos:\n{e}")

    def limpar_campos_amistade(self):
        self.entry_email1.delete(0, tk.END)
        self.entry_email2.delete(0, tk.END)
        self.entry_email_listar.delete(0, tk.END)
        self.text_resultado.delete('1.0', tk.END)

class RecomendacoesTab(ttk.Frame):
    def __init__(self, parent, neo4j):
        super().__init__(parent)
        self.neo4j = neo4j

        frm_form = ttk.Frame(self)
        frm_form.pack(padx=10, pady=10, fill='x')

        frm_result = ttk.Frame(self)
        frm_result.pack(padx=10, pady=10, fill='both', expand=True)

        ttk.Label(frm_form, text="Email do usuário:").grid(row=0, column=0, sticky='w', pady=2)
        self.entry_email = ttk.Entry(frm_form, width=40)
        self.entry_email.grid(row=0, column=1, pady=2)

        self.btn_recomendar_historico = ttk.Button(frm_form, text="Recomendar com base no histórico", command=self.recomendar_historico)
        self.btn_recomendar_historico.grid(row=1, column=0, columnspan=2, pady=5)

        self.btn_recomendar_amigos = ttk.Button(frm_form, text="Recomendar com base nos amigos", command=self.recomendar_amigos)
        self.btn_recomendar_amigos.grid(row=2, column=0, columnspan=2, pady=5)

        self.text_resultado = tk.Text(frm_result, height=15, wrap='word')
        self.text_resultado.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frm_result, command=self.text_resultado.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_resultado.config(yscrollcommand=scrollbar.set)

    def recomendar_historico(self):
        email = self.entry_email.get().strip()
        if not email:
            messagebox.showwarning("Aviso", "Por favor, insira o email do usuário.")
            return

        self.text_resultado.delete('1.0', tk.END)
        usuario = db.usuarios.find_one({"email": email})
        if not usuario:
            self.text_resultado.insert(tk.END, "Usuário não encontrado.")
            return

        livros_lidos = usuario.get("livros_lidos", [])
        if not livros_lidos:
            self.text_resultado.insert(tk.END, "Usuário ainda não leu nenhum livro.")
            return

        livros = list(db.livros.find({"titulo": {"$in": livros_lidos}}))
        generos_lidos = list(set([livro["genero"] for livro in livros]))

        recomendados = list(db.livros.find({
            "genero": {"$in": generos_lidos},
            "titulo": {"$nin": livros_lidos}
        }))

        if not recomendados:
            self.text_resultado.insert(tk.END, "Nenhum livro para recomendar no momento.")
            return

        self.text_resultado.insert(tk.END, f"📚 Recomendações para {usuario['nome']} com base no histórico:\n\n")
        for livro in recomendados:
            self.text_resultado.insert(tk.END, f"- {livro['titulo']} ({livro['autor']}) — Gênero: {livro['genero']}\n")

    def recomendar_amigos(self):
        email = self.entry_email.get().strip()
        if not email:
            messagebox.showwarning("Aviso", "Por favor, insira o email do usuário.")
            return

        self.text_resultado.delete('1.0', tk.END)

        usuario = db.usuarios.find_one({"email": email})
        if not usuario:
            self.text_resultado.insert(tk.END, "Usuário não encontrado no MongoDB.")
            return

        livros_lidos_usuario = usuario.get("livros_lidos", [])
        amigos = self.neo4j.listar_amigos(email)
        if not amigos:
            self.text_resultado.insert(tk.END, "O usuário não possui amigos cadastrados no grafo.")
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
            self.text_resultado.insert(tk.END, f"📚 Livros lidos pelos amigos de {email}, que ele ainda não leu:\n\n")
            for titulo in livros_recomendados:
                livro = db.livros.find_one({"titulo": titulo})
                if livro:
                    self.text_resultado.insert(tk.END, f"- {livro['titulo']} ({livro['autor']}) — Gênero: {livro['genero']}\n")
        else:
            self.text_resultado.insert(tk.END, "Nenhum livro novo encontrado entre os amigos.")

if __name__ == "__main__":
    app = App(neo4j)
    app.protocol("WM_DELETE_WINDOW", app.close)
    app.mainloop()