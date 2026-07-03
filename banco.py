import mysql.connector


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="senai",
        database="saep_estoque",
    )


def cadastrar_produto(nome, categoria, quantidade, preco):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = """
        INSERT INTO produtos (nome, categoria, quantidade, preco)
        VALUES (%s, %s, %s, %s)
        """
        valores = (nome, categoria, quantidade, preco)
        cursor.execute(sql, valores)
        conexao.commit()
    except mysql.connector.Error as erro:
        raise RuntimeError(f"Erro de banco de dados: {erro}") from erro
    finally:
        if cursor is not None:
            cursor.close()
        if conexao is not None:
            conexao.close()


def atualizar_produto(id_produto, nome, categoria, quantidade, preco):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = """
        UPDATE produtos
        SET nome = %s, categoria = %s, quantidade = %s, preco = %s
        WHERE id = %s
        """
        cursor.execute(sql, (nome, categoria, quantidade, preco, id_produto))
        conexao.commit()
    except mysql.connector.Error as erro:
        raise RuntimeError(f"Erro de banco de dados: {erro}") from erro
    finally:
        if cursor is not None:
            cursor.close()
        if conexao is not None:
            conexao.close()


def listar_produtos():
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, categoria, quantidade, preco FROM produtos")
        return cursor.fetchall()
    except mysql.connector.Error as erro:
        raise RuntimeError(f"Erro de banco de dados: {erro}") from erro
    finally:
        if cursor is not None:
            cursor.close()
        if conexao is not None:
            conexao.close()


def excluir_produto(id_produto):
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "DELETE FROM produtos WHERE id = %s"
        cursor.execute(sql, (id_produto,))
        conexao.commit()
    except mysql.connector.Error as erro:
        raise RuntimeError(f"Erro de banco de dados: {erro}") from erro
    finally:
        if cursor is not None:
            cursor.close()
        if conexao is not None:
            conexao.close()