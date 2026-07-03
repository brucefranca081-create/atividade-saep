import tkinter as tk
from tkinter import messagebox, ttk

from banco import atualizar_produto, cadastrar_produto, excluir_produto, listar_produtos


class AplicacaoEstoque(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SAEP Estoque Fácil Pro")
        self.geometry("1140x820")
        self.minsize(1000, 760)
        self.configure(bg="#0f172a")

        self.id_produto_edicao = None
        self.modo_edicao = False
        self.erro_banco_exibido = False

        self._configurar_estilo()
        self._criar_menu()
        self._criar_interface()
        self._set_mode_cadastro()
        self.atualizar_tabela()

    def _configurar_estilo(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Card.TFrame", background="#111827")
        style.configure("Treeview", background="#0f172a", foreground="#f8fafc", fieldbackground="#0f172a", rowheight=28)
        style.map("Treeview", background=[("selected", "#2563eb")], foreground=[("selected", "white")])
        style.configure("Treeview.Heading", background="#334155", foreground="white", font=("Arial", 10, "bold"))

    def _criar_menu(self):
        menu_principal = tk.Menu(self)
        self.config(menu=menu_principal)

        menu_arquivo = tk.Menu(menu_principal, tearoff=0)
        menu_arquivo.add_command(label="Atualizar", command=self.atualizar_tabela)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.destroy)
        menu_principal.add_cascade(label="Arquivo", menu=menu_arquivo)

        menu_ajuda = tk.Menu(menu_principal, tearoff=0)
        menu_ajuda.add_command(label="Sobre", command=lambda: messagebox.showinfo("Sobre", "SAEP Estoque Fácil Pro\nGestão moderna de estoque com foco em produtividade."))
        menu_principal.add_cascade(label="Ajuda", menu=menu_ajuda)

    def _criar_interface(self):
        self._criar_header()
        self._criar_cards_resumo()
        self._criar_formulario()
        self._criar_tabela()
        self._criar_botoes()
        self._criar_status_bar()

        self.bind("<Return>", lambda event: self.salvar())
        self.bind("<Escape>", lambda event: self.limpar_campos())

    def _criar_header(self):
        header = tk.Frame(self, bg="#0f172a")
        header.pack(fill="x", padx=24, pady=(20, 10))

        tk.Label(header, text="📦 SAEP ESTOQUE FÁCIL PRO", font=("Arial", 24, "bold"), bg="#0f172a", fg="#60a5fa").pack(anchor="w")
        tk.Label(header, text="Sistema profissional para cadastro, controle e análise de estoque em tempo real.", font=("Arial", 10), bg="#0f172a", fg="#cbd5e1").pack(anchor="w", pady=(3, 0))

    def _criar_cards_resumo(self):
        cards = tk.Frame(self, bg="#0f172a")
        cards.pack(fill="x", padx=24, pady=(0, 12))

        self._criar_card(cards, "Produtos cadastrados", "0", "#2563eb", 0)
        self._criar_card(cards, "Itens abaixo do mínimo", "0", "#f59e0b", 1)
        self._criar_card(cards, "Valor total em estoque", "R$ 0,00", "#10b981", 2)

    def _criar_card(self, container, titulo, valor, cor, coluna):
        card = tk.Frame(container, bg="#111827", padx=18, pady=16, highlightbackground="#334155", highlightthickness=1)
        card.grid(row=0, column=coluna, padx=8, sticky="nsew")
        container.grid_columnconfigure(coluna, weight=1)

        tk.Label(card, text=titulo, font=("Segoe UI", 10), bg="#111827", fg="#cbd5e1").pack(anchor="w")
        label_valor = tk.Label(card, text=valor, font=("Segoe UI", 16, "bold"), bg="#111827", fg=cor)
        label_valor.pack(anchor="w", pady=(6, 0))

        if coluna == 0:
            self.lbl_total_produtos = label_valor
        elif coluna == 1:
            self.lbl_estoque_baixo = label_valor
        else:
            self.lbl_valor_total = label_valor

    def _criar_formulario(self):
        card = tk.Frame(self, bg="#111827", padx=18, pady=16, highlightbackground="#334155", highlightthickness=1)
        card.pack(fill="x", padx=24, pady=8)

        tk.Label(card, text="Cadastro e edição", font=("Arial", 12, "bold"), bg="#111827", fg="#f8fafc").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        self.entrada_nome = self._criar_campo(card, "Nome do produto:", 1, 0)
        self.entrada_categoria = self._criar_campo(card, "Categoria:", 1, 2)
        self.entrada_quantidade = self._criar_campo(card, "Quantidade:", 2, 0)
        self.entrada_preco = self._criar_campo(card, "Preço unitário (R$):", 2, 2)

        tk.Label(card, text="Buscar produto:", font=("Arial", 10, "bold"), bg="#111827", fg="#cbd5e1").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=(12, 0))
        self.entrada_busca = tk.Entry(card, font=("Arial", 10), width=42, bg="#f8fafc", fg="#0f172a")
        self.entrada_busca.grid(row=3, column=1, sticky="w", pady=(12, 0), padx=(0, 12))
        self.entrada_busca.bind("<KeyRelease>", self._aplicar_filtro)

        card.grid_columnconfigure(1, weight=1)
        card.grid_columnconfigure(3, weight=1)

    def _criar_campo(self, container, label_text, linha, coluna):
        tk.Label(container, text=label_text, font=("Segoe UI", 10, "bold"), bg="#111827", fg="#cbd5e1").grid(row=linha, column=coluna, sticky="w", padx=(0, 8), pady=6)
        entrada = tk.Entry(container, font=("Segoe UI", 10), width=30, bg="#f8fafc", fg="#0f172a")
        entrada.grid(row=linha, column=coluna + 1, sticky="ew", pady=6, padx=(0, 12))
        return entrada

    def _criar_tabela(self):
        container = tk.Frame(self, bg="#0f172a")
        container.pack(fill="both", expand=True, padx=24, pady=(8, 0))

        tk.Label(container, text="Produtos cadastrados", font=("Arial", 12, "bold"), bg="#0f172a", fg="#f8fafc").pack(anchor="w", pady=(0, 8))

        self.tabela = ttk.Treeview(
            container,
            columns=("id", "nome", "categoria", "quantidade", "preco", "total"),
            show="headings",
            selectmode="browse",
        )
        self.tabela.heading("id", text="ID")
        self.tabela.heading("nome", text="Nome do Produto")
        self.tabela.heading("categoria", text="Categoria")
        self.tabela.heading("quantidade", text="Qtd")
        self.tabela.heading("preco", text="Preço Unitário")
        self.tabela.heading("total", text="Total em Estoque")

        self.tabela.column("id", width=55, anchor="center")
        self.tabela.column("nome", width=260)
        self.tabela.column("categoria", width=170)
        self.tabela.column("quantidade", width=80, anchor="center")
        self.tabela.column("preco", width=130, anchor="center")
        self.tabela.column("total", width=150, anchor="center")

        self.tabela.tag_configure("estoque_baixo", foreground="#f59e0b")
        self.tabela.tag_configure("estoque_critico", foreground="#ef4444")
        self.tabela.bind("<<TreeviewSelect>>", lambda event: self._atualizar_estado_botoes())
        self.tabela.bind("<Double-1>", self._carregar_para_edicao)

        barra_rolagem = ttk.Scrollbar(container, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra_rolagem.set)

        self.tabela.pack(side="left", fill="both", expand=True)
        barra_rolagem.pack(side="right", fill="y")

    def _criar_botoes(self):
        frame_botoes = tk.Frame(self, bg="#0f172a")
        frame_botoes.pack(pady=14)

        self.btn_salvar = tk.Button(frame_botoes, text="➕ Cadastrar", command=self.salvar, width=16, font=("Arial", 10, "bold"), bg="#10b981", fg="white", relief="flat", cursor="hand2")
        self.btn_salvar.grid(row=0, column=0, padx=6)

        self.btn_editar = tk.Button(frame_botoes, text="✏️ Editar", command=self._carregar_para_edicao_selecionado, width=14, font=("Arial", 10, "bold"), bg="#3b82f6", fg="white", relief="flat", cursor="hand2")
        self.btn_editar.grid(row=0, column=1, padx=6)

        self.btn_limpar = tk.Button(frame_botoes, text="🧹 Limpar", command=self.limpar_campos, width=14, font=("Arial", 10, "bold"), bg="#f59e0b", fg="white", relief="flat", cursor="hand2")
        self.btn_limpar.grid(row=0, column=2, padx=6)

        self.btn_excluir = tk.Button(frame_botoes, text="🗑️ Excluir", command=self.excluir, width=14, font=("Arial", 10, "bold"), bg="#ef4444", fg="white", relief="flat", cursor="hand2", state="disabled")
        self.btn_excluir.grid(row=0, column=3, padx=6)

        self.btn_cancelar = tk.Button(frame_botoes, text="❌ Cancelar", command=self.limpar_campos, width=14, font=("Arial", 10, "bold"), bg="#64748b", fg="white", relief="flat", cursor="hand2")
        self.btn_cancelar.grid(row=0, column=4, padx=6)

        self.btn_estoque = tk.Button(frame_botoes, text="⚠ Verificar Alertas", command=self.verificar_estoque_baixo, width=18, font=("Arial", 10, "bold"), bg="#8b5cf6", fg="white", relief="flat", cursor="hand2")
        self.btn_estoque.grid(row=0, column=5, padx=6)

    def _criar_status_bar(self):
        self.lbl_total_geral = tk.Label(self, text="Valor Total do Patrimônio: R$ 0,00", font=("Arial", 11, "bold"), bg="#0f172a", fg="#4ade80")
        self.lbl_total_geral.pack(pady=(0, 4))

        self.lbl_status = tk.Label(self, text="Carregando produtos...", font=("Arial", 9), bg="#0f172a", fg="#cbd5e1")
        self.lbl_status.pack(pady=(0, 8))

    def _set_mode_cadastro(self):
        self.modo_edicao = False
        self.btn_salvar.configure(text="➕ Cadastrar")
        self.btn_cancelar.grid_remove()
        self.btn_editar.configure(state="normal")

    def _set_mode_edicao(self):
        self.modo_edicao = True
        self.btn_salvar.configure(text="💾 Salvar alterações")
        self.btn_cancelar.grid()
        self.btn_editar.configure(state="disabled")

    def _aplicar_filtro(self, event=None):
        self.atualizar_tabela(self.entrada_busca.get().strip())

    def _atualizar_estado_botoes(self):
        estado = "normal" if self.tabela.selection() else "disabled"
        self.btn_excluir.configure(state=estado)
        self.btn_editar.configure(state="normal" if self.tabela.selection() else "disabled")

    def _carregar_para_edicao_selecionado(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto na tabela para editar.")
            return
        self._carregar_para_edicao(None)

    def _carregar_para_edicao(self, event=None):
        selecionado = self.tabela.selection()
        if not selecionado:
            return

        item = self.tabela.item(selecionado[0])
        valores = item["values"]
        self.id_produto_edicao = valores[0]

        self.entrada_nome.delete(0, tk.END)
        self.entrada_categoria.delete(0, tk.END)
        self.entrada_quantidade.delete(0, tk.END)
        self.entrada_preco.delete(0, tk.END)

        self.entrada_nome.insert(0, valores[1])
        self.entrada_categoria.insert(0, valores[2])
        self.entrada_quantidade.insert(0, valores[3])
        self.entrada_preco.insert(0, valores[4].replace("R$ ", ""))

        self.entrada_nome.focus_set()
        self._set_mode_edicao()

    def _carregar_produtos(self):
        try:
            return listar_produtos()
        except Exception as erro:
            if not self.erro_banco_exibido:
                messagebox.showerror("Erro de conexão", f"Não foi possível conectar ao banco de dados:\n{erro}")
                self.erro_banco_exibido = True
            self.lbl_status.config(text="Erro ao carregar produtos. Verifique o banco e tente novamente.")
            self.lbl_total_produtos.config(text="0")
            self.lbl_estoque_baixo.config(text="0")
            self.lbl_valor_total.config(text="R$ 0,00")
            self.lbl_total_geral.config(text="Valor Total do Patrimônio: R$ 0,00")
            return []

    def atualizar_tabela(self, filtro=""):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        produtos = self._carregar_produtos()
        if not produtos and self.erro_banco_exibido:
            return

        filtro_texto = filtro.lower().strip()
        valor_patrimonio = 0.0
        produtos_exibidos = []
        estoque_baixo = 0

        for produto in produtos:
            id_p, nome, categoria, quantidade, preco = produto
            if filtro_texto and filtro_texto not in f"{nome} {categoria}".lower():
                continue

            total_produto = quantidade * float(preco)
            valor_patrimonio += total_produto
            produtos_exibidos.append(produto)

            if quantidade < 5:
                estoque_baixo += 1

            tags = ()
            if quantidade == 0:
                tags = ("estoque_critico",)
            elif quantidade < 5:
                tags = ("estoque_baixo",)

            self.tabela.insert(
                "",
                tk.END,
                values=(id_p, nome, categoria, quantidade, f"R$ {float(preco):.2f}", f"R$ {total_produto:.2f}"),
                tags=tags,
            )

        self.erro_banco_exibido = False
        self.lbl_total_produtos.config(text=str(len(produtos_exibidos)))
        self.lbl_estoque_baixo.config(text=str(estoque_baixo))
        self.lbl_valor_total.config(text=f"R$ {valor_patrimonio:,.2f}")
        self.lbl_total_geral.config(text=f"Valor Total do Patrimônio: R$ {valor_patrimonio:,.2f}")
        self.lbl_status.config(text=f"{len(produtos_exibidos)} produto(s) exibido(s) · {estoque_baixo} com estoque baixo")
        self._atualizar_estado_botoes()

    def limpar_campos(self):
        self.entrada_nome.delete(0, tk.END)
        self.entrada_categoria.delete(0, tk.END)
        self.entrada_quantidade.delete(0, tk.END)
        self.entrada_preco.delete(0, tk.END)
        self.id_produto_edicao = None
        self.entrada_nome.focus_set()
        self._set_mode_cadastro()

    def salvar(self):
        nome = self.entrada_nome.get().strip()
        categoria = self.entrada_categoria.get().strip()
        quantidade = self.entrada_quantidade.get().strip()
        preco = self.entrada_preco.get().strip()

        if not nome or not categoria or not quantidade or not preco:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        try:
            quantidade_int = int(quantidade)
            preco_float = float(preco.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro e o preço deve estar em formato válido.")
            return

        if quantidade_int < 0:
            messagebox.showwarning("Atenção", "A quantidade não pode ser negativa.")
            return

        try:
            if self.modo_edicao and self.id_produto_edicao is not None:
                atualizar_produto(self.id_produto_edicao, nome, categoria, quantidade_int, preco_float)
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            else:
                cadastrar_produto(nome, categoria, quantidade_int, preco_float)
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível salvar o produto: {erro}")
            return

        self.limpar_campos()
        self.atualizar_tabela(self.entrada_busca.get().strip())

    def excluir(self):
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto na tabela para excluir.")
            return

        item = self.tabela.item(selecionado[0])
        id_produto = item["values"][0]
        nome_produto = item["values"][1]

        resposta = messagebox.askyesno("Confirmar exclusão", f"Deseja remover o produto '{nome_produto}' do estoque?")
        if not resposta:
            return

        try:
            excluir_produto(id_produto)
        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível remover o produto: {erro}")
            return

        self.atualizar_tabela(self.entrada_busca.get().strip())
        self.limpar_campos()
        messagebox.showinfo("Sucesso", "Produto removido com sucesso!")

    def verificar_estoque_baixo(self):
        try:
            produtos = listar_produtos()
        except Exception as erro:
            messagebox.showerror("Erro de conexão", f"Não foi possível consultar o estoque:\n{erro}")
            return

        alerta = []
        for produto in produtos:
            nome, quantidade = produto[1], produto[3]
            if quantidade < 5:
                alerta.append(f"• {nome} ({quantidade} un.)")

        if alerta:
            mensagem = "Itens abaixo do limite mínimo de 5 unidades:\n\n" + "\n".join(alerta)
            messagebox.showwarning("Alerta de Estoque", mensagem)
        else:
            messagebox.showinfo("Estoque OK", "Todos os produtos possuem níveis seguros de estoque.")


if __name__ == "__main__":
    app = AplicacaoEstoque()
    app.mainloop()