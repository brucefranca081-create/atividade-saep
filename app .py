import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
# Importando as funções corretas do seu arquivo banco.py
from banco import cadastrar_produto, listar_produtos, excluir_produto 

# 1. Configuração da Janela Principal
janela = tk.Tk()
janela.title("SAEP Estoque Fácil")
janela.geometry("550x650")  # Aumentado para caber o formulário e a tabela
janela.configure(bg="#f4f6f8")

# 2. Título
titulo = tk.Label(
    janela,
    text="SAEP Estoque Fácil",
    font=("Arial", 20, "bold"),
    bg="#f4f6f8",
    fg="#164193"
)
titulo.pack(pady=15)

# Função auxiliar para criar labels
def criar_label(texto):
    label = tk.Label(
        janela,
        text=texto,
        bg="#f4f6f8",
        fg="#172033",
        font=("Arial", 10, "bold")
    )
    label.pack()

# 3. Campos de Entrada (Formulário)
criar_label("Nome do produto:")
entrada_nome = tk.Entry(janela, width=42)
entrada_nome.pack(pady=3)

criar_label("Categoria:")
entrada_categoria = tk.Entry(janela, width=42)
entrada_categoria.pack(pady=3)

criar_label("Quantidade:")
entrada_quantidade = tk.Entry(janela, width=42)
entrada_quantidade.pack(pady=3)

criar_label("Preço:")
entrada_preco = tk.Entry(janela, width=42)
entrada_preco.pack(pady=3)

# 4. Funções de Lógica do Sistema
def atualizar_tabela():
    # Limpa os dados atuais da tabela
    for item in tabela.get_children():
        tabela.delete(item)

    # Busca os produtos atualizados do banco.py
    produtos = listar_produtos()

    # Preenche a tabela novamente
    if produtos:
        for produto in produtos:
            tabela.insert("", tk.END, values=produto)

def salvar():
    nome = entrada_nome.get()
    categoria = entrada_categoria.get()
    quantidade = entrada_quantidade.get()
    preco = entrada_preco.get()

    if nome == "" or categoria == "" or quantidade == "" or preco == "":
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    try:
        # Tenta cadastrar no banco convertendo os tipos corretamente
        cadastrar_produto(nome, categoria, int(quantidade), float(preco))
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        
        # Limpa os campos após salvar
        entrada_nome.delete(0, tk.END)
        entrada_categoria.delete(0, tk.END)
        entrada_quantidade.delete(0, tk.END)
        entrada_preco.delete(0, tk.END)
        
        # Atualiza a tabela automaticamente para mostrar o novo produto
        atualizar_tabela()
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número inteiro e Preço deve ser um número decimal.")

def excluir():
    item_selecionado = tabela.selection()

    if not item_selecionado:
        messagebox.showwarning("Atenção", "Selecione um produto na tabela para excluir.")
        return
    
    
    item = tabela.item(item_selecionado)
    id_produto = item["values"][0] # O ID é a primeira coluna (índice 0)
    
    
    confirmar = messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o produto ID {id_produto}?")
    
    if confirmar:
        # Supondo que sua função banco.excluir_produto espere o ID do produto
        excluir_produto(id_produto) 
        messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
        atualizar_tabela()

# 5. Botões de Ação
botao_salvar = tk.Button(
    janela,
    text="Cadastrar Produto",
    command=salvar,
    width=25,
    bg="#E7490F",
    fg="white",
    font=("Arial", 10, "bold")
)
botao_salvar.pack(pady=15)

botao_excluir = tk.Button(
    janela,
    text="Excluir Produto Selecionado",
    command=excluir,
    width=25,
    bg="#d9534f", # Cor avermelhada para exclusão
    fg="white",
    font=("Arial", 10, "bold")
)
botao_excluir.pack(pady=5)

# 6. Tabela (Treeview) para mostrar os produtos
tabela = ttk.Treeview(
    janela,
    columns=("id", "nome", "categoria", "quantidade", "preco"),
    show="headings"
)

# Cabeçalhos da Tabela
tabela.heading("id", text="ID")
tabela.heading("nome", text="Nome")
tabela.heading("categoria", text="Categoria")
tabela.heading("quantidade", text="Qtd")
tabela.heading("preco", text="Preço")

# Colunas da Tabela
tabela.column("id", width=40, anchor="center")
tabela.column("nome", width=150)
tabela.column("categoria", width=100)
tabela.column("quantidade", width=60, anchor="center")
tabela.column("preco", width=80, anchor="center")

tabela.pack(pady=15, fill="x", padx=15)


atualizar_tabela()


janela.mainloop()
