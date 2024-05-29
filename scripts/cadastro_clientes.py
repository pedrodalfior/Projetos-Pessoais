import tkinter as tk
import sqlite3
import customtkinter

janela_principal = tk.Tk()
janela_principal.title("Cadastro de Clientes")
janela_principal.geometry("600x400")

customtkinter.set_appearance_mode("dark")

def janela_da_pesquisa(resultado_pesquisa):
    nova_janela = tk.Toplevel()
    nova_janela.geometry("600x400")
    nova_janela.title("Pesquisa por CPF")
    label_pesquisa = tk.Label(nova_janela, text=resultado_pesquisa)
    label_pesquisa.pack()

def janela_da_exclusao(resultado_exclusao):
    janela_exclusao = tk.Toplevel()
    janela_exclusao.geometry("600x300")
    janela_exclusao.title("Cliente Excluído")
    label_pesquisa = tk.Label(janela_exclusao, text=resultado_exclusao)
    label_pesquisa.pack()

def janela_da_edicao(resultado_edicao):
    janela_edicao = tk.Toplevel()
    janela_edicao.geometry("600x400")
    janela_edicao.title("Cliente Editado")
    label_edicao = tk.Label(janela_edicao, text=resultado_edicao)
    label_edicao.pack()

def criar_tabela():
    conexao = sqlite3.connect('clientes.db')
    c = conexao.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS clientes (
              nome TEXT,
              cpf TEXT PRIMARY KEY,
              email TEXT,
              telefone TEXT
              )''')

    conexao.commit()
    conexao.close()

criar_tabela()

def pesquisar_dados():
    cpf = entry_cpf.get()
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    email = entry_email.get()

    conexao = sqlite3.connect('clientes.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes WHERE cpf=? OR nome=? OR telefone=? OR email=?", (cpf, nome, telefone, email))
    resultado_pesquisa = cursor.fetchall()

    conexao.close()

    janela_da_pesquisa(resultado_pesquisa)

def excluir_clientes():
    cpf = entry_cpf.get()
    conexao = sqlite3.connect('clientes.db')
    c = conexao.cursor()

    c.execute("DELETE FROM clientes WHERE cpf = ?",(cpf,))
    conexao.commit()
    conexao.close()

    janela_da_exclusao("Cliente excluído com sucesso!")

def editar_clientes():
    cpf = entry_cpf.get()
    telefone = entry_telefone.get()

    conexao = sqlite3.connect('clientes.db')
    c = conexao.cursor()

    c.execute('UPDATE clientes SET telefone = ? WHERE cpf = ?', (telefone, cpf))
    conexao.commit()
    conexao.close()

    janela_da_edicao("Telefone atualizado com sucesso!")

def cadastrar_cliente():
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    email = entry_email.get()
    telefone = entry_telefone.get()

    conexao = sqlite3.connect("clientes.db")
    c = conexao.cursor()

    c.execute("INSERT INTO clientes VALUES (?, ?, ?, ?)",(nome, cpf, email, telefone))
    conexao.commit()
    conexao.close()

    entry_nome.delete(0, "end")
    entry_cpf.delete(0, "end")
    entry_email.delete(0, "end")
    entry_telefone.delete(0, "end")

def exporta_clientes():
    conexao = sqlite3.connect("clientes.db")
    c = conexao.cursor()

    c.execute("SELECT * FROM clientes")
    clientes_cadastrados = c.fetchall()

    conexao.close()

    with open("clientes.csv", "w") as f:
        for cliente in clientes_cadastrados:
            f.write(','.join(cliente) + '\n')

def interacoes():
    global entry_nome, entry_cpf, entry_email, entry_telefone

    label_nome = tk.Label(janela_principal, text="NOME COMPLETO")
    label_nome.grid(row=0, column=0, padx=10, pady=10)

    label_cpf = tk.Label(janela_principal, text="CPF")
    label_cpf.grid(row=1, column=0, padx=10, pady=10)

    label_email = tk.Label(janela_principal, text="EMAIL")
    label_email.grid(row=2, column=0, padx=10, pady=10)

    label_telefone = tk.Label(janela_principal, text="TELEFONE")
    label_telefone.grid(row=3, column=0, padx=10, pady=10)

    entry_nome = tk.Entry(janela_principal, width=50)
    entry_nome.grid(row=0, column=1, padx=10, pady=10)

    entry_cpf = tk.Entry(janela_principal, width=50)
    entry_cpf.grid(row=1, column=1, padx=10, pady=10)

    entry_email = tk.Entry(janela_principal, width=50)
    entry_email.grid(row=2, column=1, padx=10, pady=10)

    entry_telefone = tk.Entry(janela_principal, width=50)
    entry_telefone.grid(row=3, column=1, padx=10, pady=10)

    botao_cadastrar = tk.Button(text='Cadastrar Cliente', command=cadastrar_cliente)
    botao_cadastrar.grid(row=4, column=1, columnspan=2, padx=40, pady=10, ipadx=80)

    botao_exportar = tk.Button(text="Exportar p/ Excel", command=exporta_clientes)
    botao_exportar.grid(row=5, column=1, columnspan=2, padx=40, pady=10, ipadx=80)

    botao_pesquisa = tk.Button(text='Pesquisar Dados', command=pesquisar_dados)
    botao_pesquisa.grid(row=6, column=1, columnspan=2, padx=40, pady=10, ipadx=80)

    botao_excluir = tk.Button(text='Excluir Cliente', command=excluir_clientes)
    botao_excluir.grid(row=7, column=1, columnspan=2, padx=40, pady=10, ipadx=80)
    
    
    janela_principal.mainloop()

