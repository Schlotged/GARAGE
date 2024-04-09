from tkinter import *
import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from docxtpl import DocxTemplate
import datetime
from datetime import *
from datetime import datetime
from os import *
from docx2pdf import *
import openpyxl
from docx import Document
from tkinter import filedialog
import win32api
import pandas as pd
from datetime import timedelta
import sqlite3
# from PIL import Image, ImageTk
# import os
import random
import os

class Bancodedados():
    def __init__(self):
        super().__init__()
        self.diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        self.conecta_bd()
        self.montatabelas()
        self.monta_tabela_cobrancas()
        self.monta_tabela_produto()
        
    def monta_tabela_cobrancas(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cobrancas (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                sobrenome TEXT,
                telefone TEXT,
                produto CHAR(100) NOT NULL,
                quantidade INTEGER,
                Valor_unitario INTEGER, 
                valor_total REAL,
                data_inicial DATE,
                data_final DATE,
                Dias INTEGER
            )
        """)
        self.conn.commit()
        print("Tabela de cobranças criada")
        self.desconecta_bd() 
         
    def monta_tabela_produto(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produto (
                codigo INTEGER PRIMARY KEY ASC,
                descricao TEXT,
                valor_unitario NUMERIC,
                quantidade INTEGER,
                fornecedor TEXT,
                tipo_produto TEXT
            )
        """)
        self.conn.commit()
        print("Tabela de produto criada")
        self.desconecta_bd()
     
    def conecta_bd(self):
        self.caminho_bd = os.path.join(self.diretorio_atual, 'clientes.bd')

        self.conn = sqlite3.connect(self.caminho_bd)
        self.cursor = self.conn.cursor()
        print("Conectando ao banco de dados")


    def desconecta_bd(self):
        self.conn.close()
        print("Desconectando do banco de dados")

    def montatabelas(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
               cod INTEGER PRIMARY KEY,
               nome_cliente CHAR(40) NOT NULL,
               sobrenome CHAR(40),
               genero CHAR(20),
               cidade CHAR(40),
               bairro CHAR(40),
               telefone INTEGER,
               empresa CHAR(40)
            )""")
        self.conn.commit()
        print("Banco de dados criado")

class funcoes(Bancodedados):
    def __init__(self):
        super().__init__()

        
         
    def buscar_informacoes_cliente(self, nome, sobrenome):
        self.conecta_bd()

        self.cursor.execute("SELECT nome_cliente, sobrenome, telefone FROM clientes WHERE nome_cliente = ? AND sobrenome = ?", (nome, sobrenome))
        
        cliente_info = self.cursor.fetchone()

        if cliente_info:
            # O cliente foi encontrado, você pode acessar as informações aqui
            nome_cliente, sobrenome_cliente, telefone = cliente_info
            self.nome_entry_tab2.delete(0, END)
            self.nome_entry_tab2.insert(0, nome_cliente)
            self.sobrenome_entry_aba_dois.delete(0, END)
            self.sobrenome_entry_aba_dois.insert(0, sobrenome_cliente)
            self.phone_entry_tab2.delete(0, END)
            self.phone_entry_tab2.insert(0, telefone)
        else:
            messagebox.showerror("Cliente não encontrado", "Cliente não encontrado no banco de dados.")
        
        self.desconecta_bd() 
 
    def buscar_info_produto(self, produto):
        self.conecta_bd()

        # Use uma consulta SQL LIKE para buscar produtos que contenham a palavra-chave
        self.cursor.execute("SELECT codigo, descricao, valor_unitario, quantidade, fornecedor, tipo_produto FROM produto WHERE descricao LIKE ?",
                            ('%' + produto + '%',))

        # Recupere todos os resultados da consulta
        lista_produtos = self.cursor.fetchall()

        # Limpe o conteúdo atual da treeview
        self.treeview_produto_top.delete(*self.treeview_produto_top.get_children())

        # Insira os novos dados na treeview
        for produto_info in lista_produtos:
            # Adicione os valores à treeview
            self.treeview_produto_top.insert("", tk.END, values=produto_info)

        self.desconecta_bd()
        print("Resultados da busca:", lista_produtos)
        print("Número de resultados:", len(lista_produtos))
 
    def busca_produto_top(self):
        produto =  self.produto_buscar.get()
        
        if not produto:
            messagebox.showerror("Erro", "Por favor, preencha o campo de busca.")
            return
        
        self.buscar_info_produto(produto)    
   
    def buscar_info_cliente(self, cliente):
        self.conecta_bd()

        # Use uma consulta SQL LIKE para buscar produtos que contenham a palavra-chave
        self.cursor.execute("SELECT cod, nome_cliente, sobrenome, genero, cidade, bairro, telefone, empresa FROM clientes WHERE nome_cliente LIKE ?",
                    ('%' + cliente + '%',))

        # Recupere todos os resultados da consulta
        lista_clientes = self.cursor.fetchall()

        # Limpe o conteúdo atual da treeview
        self.treeview_cliente_top.delete(*self.treeview_cliente_top.get_children())

        # Insira os novos dados na treeview
        for produto_info in lista_clientes:
            # Adicione os valores à treeview
            self.treeview_cliente_top.insert("", tk.END, values=produto_info)

        self.desconecta_bd()
        print("Resultados da busca:", lista_clientes)
        print("Número de resultados:", len(lista_clientes))
        
    def busca_cliente_top(self):
        produto =  self.produto_cliente.get()
        
        if not produto:
            messagebox.showerror("Erro", "Por favor, preencha o campo de busca.")
            return
        
        self.buscar_info_cliente(produto)      
    
    def buscar_cliente(self):
        nome_aba_dois = self.nome_entry_tab2.get()
        sobrenome_aba_dois = self.sobrenome_entry_aba_dois.get()

        if not nome_aba_dois or not sobrenome_aba_dois:
            messagebox.showerror("Erro", "Por favor, preencha os campos de nome e sobrenome.")
            return

        # Chame a função buscar_informacoes_cliente para buscar as informações do cliente
        self.buscar_informacoes_cliente(nome_aba_dois, sobrenome_aba_dois)
     
    def limpar(self):
        self.entry_nome_top_level.delete(0, tkinter.END)
        self.entry_sobrenome_top_level.delete(0, tkinter.END)
        self.entry_cidade_top_level.delete(0, tkinter.END)
        self.entry_bairro_top_level.delete(0, tkinter.END)
        self.entry_telefone_top_level.delete(0, tkinter.END)
        self.combobox_genero_toplevel.delete(0, tkinter.END)
        
    def inserir_cliente_e_lancamento(self):
        nome_aba_dois = self.nome_entry_tab2.get()
        sobrenome_aba_dois = self.sobrenome_entry_aba_dois.get()
        telefone_aba_dois = self.phone_entry_tab2.get()
        produto_aba_dois = self.produto_entry_tab2.get()
        data_inicial_aba_dois = self.entry_data_inicial.get()
        valor_unitario_aba_dois = float(self.entry_unidade_tab2.get())
        quantidade_aba_dois = int(self.entry_quantidade_tab2.get())
        
        if not nome_aba_dois or not sobrenome_aba_dois or not telefone_aba_dois or not data_inicial_aba_dois:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        # Converte a data inicial em um objeto datetime
        data_inicial_aba_dois = datetime.strptime(data_inicial_aba_dois, "%d/%m/%Y")

        # Calcula a data final somando 30 dias
        data_final = data_inicial_aba_dois + timedelta(days=30)

        # Converte a data final de volta para uma string no formato desejado
        data_final_str = data_final.strftime("%d/%m/%Y")
        
        valor_total = quantidade_aba_dois * valor_unitario_aba_dois
        valor_total = round(valor_total, 2) 
         
        self.conecta_bd()
        self.cursor.execute("""
            INSERT INTO cobrancas('produto', 'quantidade', 'valor_total', 'data_inicial', 'data_final', 'nome', 'sobrenome', 'telefone', 'Valor_unitario')
            VALUES (?, ?, ?, ?, ?,?,?,?, ?)""", (produto_aba_dois,quantidade_aba_dois,valor_total,data_inicial_aba_dois,data_final_str,nome_aba_dois, sobrenome_aba_dois,telefone_aba_dois , valor_unitario_aba_dois ))
        
        # Commit e depois desconecta do banco
        self.conn.commit()
        self.desconecta_bd()

        self.limpar_campos_tab2()
        self.listar_cobrancas()
        
        messagebox.showwarning('Sucesso', 'Foi realizado o lançamento com sucesso!')

    def dias(self):
        self.data_final = datetime.now() + datetime.timedelta(days=30)
        # Exemplo de uso
        dias_restantes = self.calcular_dias_restantes(self.data_final)
        print(f"Dias Restantes: {dias_restantes}")
    
    def calcular_dias_restantes(self, data_final):
        
        hoje = datetime.now()  # Obter a data atual

        # Calcular a diferença em dias
        data_final = datetime.strptime(data_final, "%d/%m/%Y")
        
        diferenca = data_final - hoje

        # Extrair o número de dias restantes
        dias_restantes = diferenca.days

        return dias_restantes
     
    def listar_cobrancas(self):
        
        self.treeview.delete(*self.treeview.get_children())
        self.conecta_bd()
        
        lista = self.cursor.execute("""SELECT id, produto, quantidade, valor_total, data_inicial, data_final, nome, sobrenome, telefone, Valor_unitario, Dias FROM cobrancas
            ORDER BY data_final ASC;
        """)

        for item in lista:
            id_cobranca, produto, quantidade, valor_total, data_inicial, data_final, nome, sobrenome, telefone, valor_unitario, _ = item 

            dias_restantes  = self.calcular_dias_restantes(data_final)
            item = item[:-1] + (dias_restantes,)
            
            if dias_restantes <= 5:
                # Se faltar 5 dias ou menos, configure um tag para essa linha
                self.treeview.tag_configure("vermelho", background="red")
                self.treeview.insert("", END, values=item, tags=("vermelho",))
            else :
                self.treeview.insert("", END, values=item)
        
        self.desconecta_bd()
    
    def listar_produto(self):
            self.conecta_bd()

            # Execute a consulta SQL
            self.cursor.execute("""SELECT codigo, descricao, valor_unitario, quantidade, fornecedor, tipo_produto FROM produto
                                ORDER BY descricao ASC;""")
            
            # Recupere todos os resultados da consulta
            lista_produto = self.cursor.fetchall()

            # Limpe o conteúdo atual da treeview
            self.treeview_produto.delete(*self.treeview_produto.get_children())

            # Insira os novos dados na treeview
            for produto in lista_produto:
                self.treeview_produto.insert("", tk.END, values=produto)

            self.desconecta_bd()
    
    def insert_row(self):
            self.selected_items = []
            self.produto = self.produto_entry.get()
            self.valor_unidade = float(self.valor_entry.get()) 
            self.quantidade = int(self.qnt_spinbox.get())
            self.valor_total = self.valor_unidade*self.quantidade
            self.name = self.name_entry.get()
            self.age = int(self.age_spinbox.get())
            self.subscription_status = self.status_combobox.get()
            self.cliente = self.tipo_cliente_combobox.get()
            self.vendedor = self.name_vendedor_entry.get()
        
            self.current_date = datetime.datetime.now().strftime('%d/%m/%Y') 
            self.path = "base de dados_teste.xlsx"
            self.workbook = openpyxl.load_workbook(self.path)
            self.sheet = self.workbook.active
            
            self.row_values = [self.name, self.age, self.subscription_status, self.cliente, self.produto, self.valor_unidade,self.quantidade, self.valor_total, self.vendedor, self.current_date]
            self.sheet.append(self.row_values)
            self.workbook.save(self.path)

            self.treeview.insert('', tk.END, values=self.row_values)

            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, "Nome")
            self.age_spinbox.delete(0, "end")
            self.age_spinbox.insert(0, "Total dias fiado")
            self.status_combobox.set(self.combo_list[0])
            
            
            self.selected_item = {
                "Nome": self.name,
                "Dias": self.age,
                "Pagamento": self.subscription_status,
                "Cliente": self.tipo_cliente_combobox,
                "Produto": self.produto,
                "Valor unitario": self.valor_unidade,
                "Quantidade": self.quantidade,
                "Total": self.valor_total,
            }
            self.selected_items.append(self.selected_item)
    
    def formatar_telefone(self, event):
        # Remove qualquer formatação atual
        texto_atual = self.entry_telefone_top_level.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        
        # Formata o texto no estilo (00) 00000-0000
        if len(texto_atual) > 10:
            telefone_formatado = f"({texto_atual[:2]}) {texto_atual[2:7]}-{texto_atual[7:]}"
            self.entry_telefone_top_level.delete(0, tk.END)
            self.entry_telefone_top_level.insert(0, telefone_formatado)
    
    def formatar_telefone_tab3(self, event):
        # Remove qualquer formatação atual
        texto_atual = self.phone_entry_tab3.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        
        # Formata o texto no estilo (00) 00000-0000
        if len(texto_atual) > 10:
            telefone_formatado = f"({texto_atual[:2]}) {texto_atual[2:7]}-{texto_atual[7:]}"
            self.phone_entry_tab3.delete(0, tk.END)
            self.phone_entry_tab3.insert(0, telefone_formatado)
    
    def formatar_telefone_tab2(self, event):
            # Remove qualquer formatação atual
        texto_atual = self.phone_entry_tab2.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        
        # Formata o texto no estilo (00) 00000-0000
        if len(texto_atual) > 9:
            telefone_formatado_tab2 = f"({texto_atual[:2]}) {texto_atual[2:7]}-{texto_atual[7:]}"
            self.phone_entry_tab2.delete(0, tk.END)
            self.phone_entry_tab2.insert(0, telefone_formatado_tab2)

    def cadastro_cliente(self):
        self.criar_cliente_top_level()
           
    def show_success_message(self):
        messagebox.showinfo("Sucesso", "Documento gerado e salvo com sucesso!")

    def clear_item(self):
        self.entry_codigo.delete(0, tkinter.END) 
        self.quantidade_spinbox.delete(0, tkinter.END)
        self.quantidade_spinbox.insert(0, "1")
        self.descricao_entry.delete(0, tkinter.END)
        self.preco_unitario_spinbox.delete(0, tkinter.END)
        self.preco_unitario_spinbox.insert(0, "0.0")
 
    def add_item(self):
            # Adicionar os itens dos campos na tela
            
            self.qty = int(self.quantidade_spinbox.get()) 
            self.desc = self.descricao_entry.get()
            self.preco = float(self.preco_unitario_spinbox.get())
            self.line_total = self.qty*self.preco
            self.invoice_item = [self.qty, self.desc, self.preco, self.line_total]

            self.tree_tab1.insert("",0, values=self.invoice_item)
            self.clear_item()
            
            self.invoice_list.append(self.invoice_item)
   
    def gerar_documento(self):
        self.janela_top_level()
    
    def buscar_informacoes_e_salvar(self, planilha, data_inicial, data_final, arquivo_saida):
        # Carrega a planilha em um DataFrame
        self.df = pd.read_excel("base de dados_teste.xlsx")  # Use read_csv() se for um arquivo CSV
        # Converte as colunas de datas para o tipo datetime
        self.df['Data'] = pd.to_datetime(self.df['Data'], format='%d/%m/%Y')
        
        # Filtra as linhas que estão dentro do intervalo de datas desejado
        self.df_filtrado = self.df[(self.df['Data'] >= data_inicial) & (self.df['Data'] <= data_final)] 
        
        # Salva as informações filtradas em um novo arquivo Excel
        self.df_filtrado.to_excel(arquivo_saida, index=False)  # Use to_csv() se quiser salvar como arquivo CSV
        
    def gerar_relatorio_mensal(self):
        self.current_datetime = datetime.datetime.now()
        self.date_time_str = self.current_datetime.strftime("%Y-%m-%d") 
        self.data_inicial = pd.to_datetime(self.data_inicial_entry.get(), format="%d/%m/%Y")
        self.data_final = pd.to_datetime(self.data_final_entry.get(), format="%d/%m/%Y")
        self.arquivo_saida = f"Relatorio_mensal_{self.date_time_str}.xlsx"  # You can customize the output file name
        
        # Ensure data_inicial is before data_final
        if self.data_inicial > self.data_final:
            messagebox.showerror("Erro", "A data inicial deve ser anterior à data final.")
            return

        # Call the buscar_informacoes_e_salvar function
        try:
            self.buscar_informacoes_e_salvar("dados.xlsx", self.data_inicial, self.data_final, self.arquivo_saida)
            print("Data saved successfully.")
            messagebox.showinfo("Sucesso", "Relatório gerado e salvo com sucesso!")
            self.janela_dois.destroy()
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar os dados: {str(e)}")
    
    def gerar_documento_tab1(self):
        self.doc = DocxTemplate("Orcamento_direto_caixa_teste.docx")
        self.name = self.first_name_entry.get()+ "_" + self.last_name_entry.get()
        self.phone = self.telefone_entry.get()
        self.subtotal = sum(item[3] for item in self.invoice_list)
        self.salestax = 0.1
        self.total = self.subtotal*(1-self.salestax) 
        
        self.doc.render({"nome": self.name,
                "Telefone": self.phone,
                "invoice_list": self.invoice_list,
                "subtotal": self.subtotal,
                "taxavenda":str(self.salestax*100)+"%",
                "total": self.total})
        
        self.doc_name = "Novo_orçamento" + "_" + self.name + "_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".docx"
        self.doc.save(self.doc_name)
        messagebox.showinfo("Documento gerado com sucesso", "Documento gerado com sucesso")
        self.new_invoice()
        # convert(self.doc_name)
        # messagebox.showinfo("Documento gerado com sucesso", "Documento PDF gerado com sucesso")
    
    def new_invoice(self):
        self.first_name_entry.delete(0, tkinter.END)
        self.last_name_entry.delete(0, tkinter.END)
        self.telefone_entry.delete(0, tkinter.END)
        self.clear_item()
        self.tree_tab1.delete(*self.tree_tab1.get_children())
        
        self.invoice_list.clear()
        
    def habilitar_edicao(self):
        self.codigo.config(state="normal")
        self.nome_entry_tab3.config(state="normal")
        self.sobrenome_entry.config(state="normal")
        self.phone_entry_tab3.config(state="normal")
        self.combobox_genero.config(state="normal")
        self.entry_cidade.config(state="normal")
        self.entry_bairro.config(state="normal")
        self.empresa_combobox.config(state="normal")
        self.editando = True
        
    def habilitar_edicao_tab2(self):
        self.codigo_aba_dois.config(state="normal")
        self.nome_entry_tab2.config(state="normal")
        self.sobrenome_entry_aba_dois.config(state="normal")
        self.phone_entry_tab2.config(state="normal")
        self.produto_entry_tab2.config(state="normal")
        self.entry_data_inicial.config(state="normal")
        self.entry_quantidade_tab2.config(state="normal") 
        self.editando = True
        
    def salvar_edicao(self):
        if self.editando:
            self.codigo = self.codigo.get()
            self.nome = self.nome_entry_tab3.get()
            self.sobrenome = self.sobrenome_entry.get()
            self.phone = self.phone_entry_tab3.get()
            self.genero = self.combobox_genero.get()
            self.cidade = self.entry_cidade.get()
            self.bairro = self.entry_bairro.get()
            # Aqui você pode adicionar lógica para salvar os dados, se necessário
            self.codigo.config(state="disabled")
            self.editando = False
    
    def add_clientes(self): 
        # self.codigo = str(self.codigo.get())
        self.nome = self.entry_nome_top_level.get()
        self.sobrenome = self.entry_sobrenome_top_level.get()
        self.telefone = self.entry_telefone_top_level.get()
        self.genero = self.combobox_genero_toplevel.get()
        self.cidade = self.entry_cidade_top_level.get()
        self.bairro = self.entry_bairro_top_level.get()
        self.tipo_empresa = self.empresa_combobox_toplevel.get()
        self.conecta_bd()
        
        if not self.tipo_empresa or not self.nome or not self.sobrenome:
            messagebox.showerror('Erro', 'Preencha todos os campos!')
            return
             
        self.cursor.execute(""" INSERT INTO clientes(nome_cliente, sobrenome, genero, cidade, bairro, telefone, empresa)
            VALUES (?, ?, ?, ?, ?, ?, ?)""", (self.nome, self.sobrenome, self.genero, self.cidade, self.bairro, self.telefone, self.tipo_empresa))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar()
        
           
 
    def select_lista(self):
        self.treeview_cliente.delete(*self.treeview_cliente.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod,nome_cliente, sobrenome, genero, cidade, bairro, telefone, empresa FROM clientes
            ORDER BY nome_cliente ASC; """)
        
        for i in lista:
            self.treeview_cliente.insert("", END, values=i)
        self.desconecta_bd()
        
    def limpar_campos_tab3(self):
        self.codigo.delete(0, tkinter.END)
        self.nome_entry_tab3.delete(0, tkinter.END)
        self.sobrenome_entry.delete(0, tkinter.END)
        self.phone_entry_tab3.delete(0, tkinter.END)
        self.combobox_genero.delete(0, tkinter.END)
        self.entry_cidade.delete(0, tkinter.END)
        self.entry_bairro.delete(0, tkinter.END)
        
    def limpar_campos_tab2(self):
        self.codigo_aba_dois.delete(0, tkinter.END)
        self.nome_entry_tab2.delete(0, tkinter.END)
        self.sobrenome_entry_aba_dois.delete(0, tkinter.END)
        self.phone_entry_tab2.delete(0, tkinter.END)
        self.produto_entry_tab2.delete(0, tkinter.END)
        self.entry_data_inicial.delete(0, tkinter.END)
        self.entry_quantidade_tab2.delete(0, tkinter.END)

    def limpar_campos_tab4(self):
        self.nome_codigo_entry.delete(0, tkinter.END)  
        self.nome_produto_entry.delete(0, tkinter.END)
        self.fornecedor_entry.delete(0, tkinter.END)
        self.tipo_produto_combobox.delete(0, tkinter.END)
        self.valor_unitario_entry.delete(0, tkinter.END)
        self.quantidade_entry.delete(0, tkinter.END)
    
    def formatar_data(self, data):
        # Obtém o texto atual na Entry
        texto_atual = self.entry_data_inicial.get()
        
        # Remove todos os caracteres não numéricos para permitir a digitação
        texto_numerico = "".join(filter(str.isdigit, texto_atual))
        
        # Formata o texto no estilo dd/mm/yyyy
        if len(texto_numerico) >= 8:
            data_formatada = datetime.strptime(texto_numerico, "%d%m%Y").strftime("%d/%m/%Y")
            self.entry_data_inicial.delete(0, tk.END)
            self.entry_data_inicial.insert(0, data_formatada)
        else:
            # Se a entrada for muito curta, deixe-a como está
            self.entry_data_inicial.delete(0, tk.END)
            self.entry_data_inicial.insert(0, texto_numerico)
    
    def inserir_produto(self):
        
        produto = self.nome_produto_entry.get()
        fornecedor_aba_quatro = self.fornecedor_entry.get()
        tipo_produto = self.tipo_produto_combobox.get()
        valor_unitario_aba_quatro = self.valor_unitario_entry.get()
        quantidade_aba_quatro = self.quantidade_entry.get()
        
        if not produto or not fornecedor_aba_quatro or not quantidade_aba_quatro or not tipo_produto or not valor_unitario_aba_quatro:
            message = messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return message
         
        codigo_produto = self.gerar_codigo_aleatorio()

        self.conecta_bd()
        self.cursor.execute("""
            INSERT INTO produto('codigo', 'descricao', 'Valor_unitario', 'quantidade', 'fornecedor', 'tipo_produto')
            VALUES (?, ?, ?, ?, ?, ?)""", (codigo_produto, produto, valor_unitario_aba_quatro, quantidade_aba_quatro, fornecedor_aba_quatro, tipo_produto))

        # Commit e depois desconecta do banco
        self.conn.commit()
        self.desconecta_bd()
        self.listar_produto()

        messagebox.showinfo('Sucesso', 'Foi realizado o lançamento com sucesso!')
        self.limpar_campos_tab4()
    
    def selecionar_produto_tab4(self, event):
            # Obtém o item selecionado na treeview
        item_selecionado = self.treeview_produto.selection()

        if item_selecionado:
            # Recupera os valores do item selecionado
            valores = self.treeview_produto.item(item_selecionado, 'values')

            # Exibe os valores onde você precisar
            print("Produto selecionado:", valores)

            produto_info = (valores[0],valores[1],valores[2], valores[3], valores[4], valores[5])

            if produto_info:
                # O produto foi encontrado, você pode acessar as informações aqui
                codigo,descricao, valor_unitario, qntd, fornecedor,tipo_produto = produto_info
                
                self.nome_codigo_entry.delete(0, END)
                self.nome_codigo_entry.insert(0, codigo) 
                self.nome_produto_entry.delete(0, END)
                self.nome_produto_entry.insert(0, descricao)
                self.valor_unitario_entry.delete(0, END)
                self.valor_unitario_entry.insert(0, valor_unitario)
                self.quantidade_entry.delete(0, END)
                self.quantidade_entry.insert(0, qntd)
                self.fornecedor_entry.delete(0, END)
                self.fornecedor_entry.insert(0, fornecedor)
                self.tipo_produto_combobox.delete(0, END)
                self.tipo_produto_combobox.insert(0, tipo_produto)
                
            else:
                messagebox.showerror("Produto não encontrado", "Produto não encontrado no banco de dados.")

    def atualizar_produto_no_bd(self):
        # Obtém os valores das Entrys
        codigo = self.nome_codigo_entry.get() 
        descricao = self.nome_produto_entry.get()
        valor_unitario = self.valor_unitario_entry.get()
        quantidade = self.quantidade_entry.get()
        fornecedor = self.fornecedor_entry.get()
        tipo_produto = self.tipo_produto_combobox.get()

        # Atualiza as informações no banco de dados
        
        # Verifica se o código foi fornecido
        if not codigo or not descricao or not valor_unitario or not quantidade or not fornecedor or not tipo_produto:
            messagebox.showwarning("Código Inválido", "Por favor, informe o código do produto a ser excluído.")
            return
        self.conecta_bd()

        try:
            self.cursor.execute("""
                UPDATE produto
                SET descricao = ?,
                    valor_unitario = ?,
                    quantidade = ?,
                    fornecedor = ?,
                    tipo_produto = ?
                WHERE codigo = ?
            """, (descricao, valor_unitario, quantidade, fornecedor, tipo_produto, codigo))

            self.conn.commit()
            messagebox.showinfo("Sucesso", "Produto atualizado no banco de dados.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar produto: {e}")
        finally:
            self.desconecta_bd()
        self.listar_produto()
        self.limpar_campos_tab4()
        
    def excluir_produto_do_bd(self):
        # Obtém o código do produto a ser excluído
        codigo = self.nome_codigo_entry.get()

        # Verifica se o código foi fornecido
        if not codigo:
            messagebox.showwarning("Código Inválido", "Por favor, informe o código do produto a ser excluído.")
            return

        # Conecta ao banco de dados
        self.conecta_bd()

        try:
            # Executa a exclusão do produto com base no código
            self.cursor.execute("""
                DELETE FROM produto
                WHERE codigo = ?
            """, (codigo,))

            # Commit as alterações no banco de dados
            self.conn.commit()

            # Mostra uma mensagem de sucesso
            messagebox.showinfo("Sucesso", "Produto excluído do banco de dados.")
        except sqlite3.Error as e:
            # Mostra uma mensagem de erro se a exclusão falhar
            messagebox.showerror("Erro", f"Erro ao excluir produto: {e}")
        finally:
            # Desconecta do banco de dados
            self.desconecta_bd()

        # Atualiza a lista de produtos na treeview
        self.listar_produto()

        # Limpa os campos na aba 4
        self.limpar_campos_tab4()


class tela(funcoes):
    def __init__(self):
        super().__init__()
        self.janela = Tk() 
        self.tela() 
        self.notebook_abas()
        self.frames_da_tela()
        self.campos_tela_um()
        self.tree_tab1()
        self.treeview_tab2()
        self.campo_tela_aba_dois()
        self.campos_tab3() 
        self.clear_item()
        self.tela_treeview_cliente()
        self.montatabelas()
        self.select_lista()
        self.listar_cobrancas()
        self.campos_tab4()
        self.treeeview_tab4()
        self.listar_produto()
        
        self.pdv()
        self.tree_pdv()
        
        
    def notebook_abas(self):
        self.note = ttk.Notebook(self.janela)
        self.note.pack(fill='both', expand=True)

        try:
            self.image_orc = tk.PhotoImage(file="C:\\Users\\gedson.silva\\Desktop\\backup\\GARAGE\\calculator_line_icon_235355.png")
            self.image_lançamento = tk.PhotoImage(file="C:\\Users\\gedson.silva\\Desktop\\backup\\GARAGE\\marketing_financial_teamwork_management_corporate_finance_business_icon_231873.png")
            self.image_cliente = tk.PhotoImage(file="C:\\Users\\gedson.silva\\Desktop\\backup\\GARAGE\\employee_group_line_icon_235349.png")
            self.image_produto = tk.PhotoImage(file="C:\\Users\\gedson.silva\\Desktop\\backup\\GARAGE\\productapplication_producto_3010.png")
            self.image_caixa = tk.PhotoImage(file="C:\\Users\\gedson.silva\\Desktop\\backup\\GARAGE\\ecommerce_shopping_cart_icon_220374.png")
        except tk.TclError as e:
            print(f"Erro ao carregar a imagem: {e}")

        self.tab1 = ttk.Frame(self.note)
        self.note.add(self.tab1, text='Orçamento', image=self.image_orc, compound="left")

        self.tab2 = ttk.Frame(self.note)
        self.note.add(self.tab2, text="Fiado", image=self.image_lançamento, compound="left")

        self.tab3 = ttk.Frame(self.note)
        self.note.add(self.tab3, text="Cliente", image=self.image_cliente, compound="left")

        self.tab4 = ttk.Frame(self.note)
        self.note.add(self.tab4, text="Produto", image=self.image_produto,  compound="left")

        self.tab5 = ttk.Frame(self.note)
        self.note.add(self.tab5, text="Caixa", image=self.image_caixa,  compound="left")
   
    def tela(self):
        self.janela.title("Gerador de orçamento")
        self.janela.resizable(True, True)
        # self.janela.geometry("1200x700")
        # self.janela.minsize(width=800, height=400)
        
        largura = 1200
        altura = 700
         
        x_geral = (self.janela.winfo_screenwidth() - largura) // 2
        y_geral = (self.janela.winfo_screenheight() - altura) // 2
        self.janela.geometry(f'{largura}x{altura}+{x_geral}+{y_geral}')
        
        caminho_do_icone = r'C:\Users\gedson.silva\Desktop\backup\GARAGE\garage_ico.ico'
        try: 
            self.janela.iconbitmap(caminho_do_icone) 
        except tk.TclError:
            print(f"Não foi possível encontrar o arquivo de ícone: {caminho_do_icone}")
        
    def frames_da_tela(self):
        self.posicao_cima_frame = ttk.Labelframe(self.tab1)
        self.posicao_cima_frame.grid(row=0, column=1, padx=5, pady=10, sticky="news", columnspan=3)

        self.tree_frame = ttk.Labelframe(self.tab1, text="Tela de Dados")
        self.tree_frame.grid(row=1, column=1, padx=5, pady=10, sticky="ew", columnspan=3)
       
        self.gerador_dados_frame = ttk.Labelframe(self.tab1, text="GERADOR")
        self.gerador_dados_frame.grid(row=2, column=1, padx=5, pady=10, sticky="ew",columnspan=3)
        
        self.Widgets_frame = ttk.Labelframe(self.tab2, text="Insira")
        self.Widgets_frame.grid(row=0, column=0, padx=5,pady=10,sticky="ew",columnspan=3)
        
        self.parte_de_baixo_frame = ttk.Labelframe(self.tab2, text="DADOS")
        self.parte_de_baixo_frame.grid(row=2, column=0, sticky='w')
        
        self.treeview_labelframe = ttk.Labelframe(self.tab2, text="Tela")
        self.treeview_labelframe.grid(row=1, column=0, pady=2,sticky="ew",columnspan=3)

        self.treeFrame = ttk.Frame(self.treeview_labelframe)
        self.treeFrame.grid(row=1, column=0, pady=5, sticky="news",columnspan=3)
        
        self.frame_um_tab3 = ttk.Labelframe(self.tab3)
        self.frame_um_tab3.grid(row=0, column=0, padx=5, sticky="news")
        
        self.frame_dois_tab3 = ttk.Labelframe(self.tab3)
        self.frame_dois_tab3.grid(row=1, column=0,sticky="news", padx=5, columnspan=3)
        # Faz a coluna 0 expandir para ocupar todo o espaço disponível
        
        self.tab1.columnconfigure(1, weight=1)
        self.tab2.columnconfigure(0, weight=1)
        self.tab3.columnconfigure(0, weight=1)
        self.tab4.columnconfigure(0, weight=1)
        self.tab5.columnconfigure(0, weight=1)

        self.treeview_labelframe.columnconfigure(0, weight=1) 
         
        self.frame_tres_tab3 = ttk.Labelframe(self.tab3)
        self.frame_tres_tab3.grid(row=2, column=0,sticky="news", padx=5, columnspan=3)
        
        self.frame_um_tab4 = ttk.Labelframe(self.tab4)
        self.frame_um_tab4.grid(row=0, column=0,sticky="news", padx=5, columnspan=3)
        
        self.frame_dois_tab4 = ttk.Labelframe(self.tab4)
        self.frame_dois_tab4.grid(row=1, column=0,sticky="news", padx=5, columnspan=3)
        self.frame_dois_tab4.columnconfigure(0, weight=1)
        
        self.frame_tab4 = ttk.Frame(self.frame_dois_tab4)
        self.frame_tab4.grid(row=0, column=0, pady=5,sticky="news",  columnspan=3)
        
        self.frame_tres_tab4 = ttk.Labelframe(self.tab4)
        self.frame_tres_tab4.grid(row=2, column=0,sticky="news", padx=5, columnspan=3)
         
                #frame tab5
        self.frame_um_tab5 = ttk.Labelframe(self.tab5)
        self.frame_um_tab5.grid(row=0, column=0,sticky="news", padx=5, columnspan=3)
        
        self.frame_dois_tab5 = ttk.Labelframe(self.tab5)
        self.frame_dois_tab5.grid(row=1, column=0,sticky="news", padx=5)
        
        # self.frame_tres_tab5 = ttk.Labelframe(self.tab5)
        # self.frame_tres_tab5.grid(row=1, column=1,sticky="ew", padx=5)
        
        self.frame = ttk.Frame(self.tab5)
        self.frame.grid(row=2, column=1,sticky="news", padx=5)
        
        self.frame_quatro_tab5 = ttk.Labelframe(self.tab5)
        self.frame_quatro_tab5.grid(row=2, column=0,sticky="new", padx=5, columnspan=1)
        
        self.frame_cinco_tab5 = ttk.Labelframe(self.tab5)
        self.frame_cinco_tab5.grid(row=1, column=1, sticky="news", padx=5)

    def campos_tela_um(self):
        self.label_codigo = ttk.Label(self.posicao_cima_frame, text="Código")
        self.label_codigo.grid(row= 0, column=0, pady=10, sticky="w")
       
        self.entry_codigo = ttk.Entry(self.posicao_cima_frame)
        self.entry_codigo.grid(row=0, column=1, pady=10, sticky="ew", columnspan=3) 
        
        self.botao_buscar_tab1 = ttk.Button(self.posicao_cima_frame,text="Busca")
        self.botao_buscar_tab1.grid(row=0, column=4, pady=10, sticky="ew")
         
        self.first_name_frame = ttk.Label(self.posicao_cima_frame, text="Nome")
        self.first_name_frame.grid(row=1, column=0, pady=10, sticky="w")
        
        self.first_name_entry = ttk.Entry(self.posicao_cima_frame)
        self.first_name_entry.grid(row=1, column=1, pady=10,sticky="ew")
        
        self.last_name_frame = ttk.Label(self.posicao_cima_frame, text="Sobrenome")
        self.last_name_frame.grid(row=1, column=2, pady=10)
        
        self.last_name_entry = ttk.Entry(self.posicao_cima_frame)
        self.last_name_entry.grid(row=1, column=3, pady=10)

        # Campo do telefone na tela
        self.telefone_label = ttk.Label(self.posicao_cima_frame, text="Telefone")
        self.telefone_label.grid(row=2, column=0, pady=10, sticky="w")
        self.telefone_entry = ttk.Entry(self.posicao_cima_frame)
        self.telefone_entry.grid(row=2, column=1, pady=10, sticky="ew")

        # Campo da Quantidade na tela
        self.quantidade_label = ttk.Label(self.posicao_cima_frame, text="Quantidade")
        self.quantidade_label.grid(row=2, column=2, padx=5, pady=10)
        self.quantidade_spinbox = ttk.Spinbox(self.posicao_cima_frame, from_=0, to=100)
        self.quantidade_spinbox.grid(row=2, column=3, pady=10, sticky="ew")

        # Campo do Preço Unitario na tela
        self.preco_unitario_label = ttk.Label(self.posicao_cima_frame, text="Preco Unitario")
        self.preco_unitario_label.grid(row=2, column=4, padx=5, pady=10, sticky="w")
        self.preco_unitario_spinbox = ttk.Spinbox(self.posicao_cima_frame, from_=0.0, to=1000, increment=0.1)
        self.preco_unitario_spinbox.grid(row=2, column=5, pady=10, sticky="ew")

        # Campo da Descrição na tela
        self.descricao_label = ttk.Label(self.posicao_cima_frame, text="Descrição")
        self.descricao_label.grid(row=4, column=0, pady=10, sticky="w")
        self.descricao_entry = ttk.Entry(self.posicao_cima_frame)
        self.descricao_entry.grid(row=4, column=1, pady=10, sticky="ew", columnspan=3)

        # Botão de Adicionar item
        self.add_item_button = ttk.Button(self.posicao_cima_frame, text="Adicionar Item", command=self.add_item)
        self.add_item_button.grid(row=6, column=2, padx=10, pady=10,columnspan=3, sticky="ew")
        
        self.save_invoice_button = ttk.Button(self.gerador_dados_frame, text="Gerar Documento", command=self.gerar_documento_tab1)
        self.save_invoice_button.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        
        self.new_invoice_button = ttk.Button(self.gerador_dados_frame, text="Nova Fatura", command=self.new_invoice)
        self.new_invoice_button.grid(row=0, column=1, padx=10, pady=5)
         
    def tree_tab1(self):
        self.invoice_list = []
        self.columns = ("Quantidade", "Descricao", "Preco Unitario", "Total")
        self.tree_tab1 = ttk.Treeview(self.tree_frame, columns= self.columns, show="headings", height=13) 
        self.tree_tab1.heading("Quantidade", text="Quantidade")
        self.tree_tab1.heading("Descricao", text="Descricao")
        self.tree_tab1.heading("Preco Unitario",text="Preco Unitario")
        self.tree_tab1.heading("Total", text="Total")
        self.tree_tab1.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def treeview_tab2(self): 
        
        columns_aba_dois = ('id', 'produto', 'quantidade', 'valor_total', 'data_inicial', 'data_final', 'nome', 'sobrenome', 'telefone', 'Valor_unitario','Dias')
        
        self.treeview = ttk.Treeview(self.treeFrame, show="headings", columns=columns_aba_dois, height=13)
        self.treeview.column("id", width=30)
        self.treeview.column("produto", width=150)
        self.treeview.column("quantidade", width=30) 
        self.treeview.column("valor_total", width=50)
        self.treeview.column("data_inicial", width=50)
        self.treeview.column("data_final", width=50)   
        self.treeview.column("nome", width=180)
        self.treeview.column("sobrenome", width=80)
        self.treeview.column("telefone", width=80)
        self.treeview.column("Valor_unitario", width=50)
        self.treeview.column("Dias", width=50)

        
        self.treeview.heading("id", text="id")
        self.treeview.heading("produto", text="produto")
        self.treeview.heading("quantidade", text="quantidade")       
        self.treeview.heading("valor_total",text="valor_total")
        self.treeview.heading("data_inicial", text="data_inicial")
        self.treeview.heading("data_final", text="data_final")
        self.treeview.heading("nome", text="nome")   
        self.treeview.heading("sobrenome", text="sobrenome")
        self.treeview.heading("telefone", text="telefone")
        self.treeview.heading("Valor_unitario", text="Valor_unitario")
        self.treeview.heading("Dias", text="Dias")
        
        self.treeScroll = ttk.Scrollbar(self.treeFrame)
        self.treeScroll.pack(side="right", fill="y")
         
        self.treeview.pack(fill=tk.BOTH, expand=True)
        self.treeScroll.config(command=self.treeview.yview)

     
    def tela_de_lancamento_fiado(self):
        self.janela_lançar_fiado = Toplevel(self.janela)
        self.janela_lançar_fiado.title("Lançamento de fiado")
        self.janela_lançar_fiado.geometry("810x500")
        self.janela_lançar_fiado.resizable(False, False)
        self.janela_lançar_fiado.transient(self.janela)
        self.janela_lançar_fiado.focus_force()
        self.janela_lançar_fiado.grab_set()
       
        self.janela_lançar_fiado.columnconfigure(0, weight=1)
         
        largura = 810
        altura = 500
        x = (self.janela_lançar_fiado.winfo_screenwidth() - largura) // 2
        y = (self.janela_lançar_fiado.winfo_screenheight() - altura) // 2
        self.janela_lançar_fiado.geometry(f'{largura}x{altura}+{x}+{y}') 
        
        self.button_style = ttk.Style()
        self.button_style.configure("Custom.TButton", padding=(5, 10)) 

        self.list_genero = ["", "Masculino", "Feminino"]

        self.list_empresa_PF = ["", "Pessoa Jurídica", "Pessoa Física"]

        self.frame_fiado_top = ttk.Labelframe(self.janela_lançar_fiado, text="Insira")
        self.frame_fiado_top.grid(row=0, column=0, padx=5,pady=10,sticky="ew",columnspan=3)
        
        self.label_codigo_aba_dois = ttk.Label(self.frame_fiado_top, text="Código:")
        self.label_codigo_aba_dois.grid(row=0, column=0, pady=5, sticky="w")

        self.codigo_aba_dois = ttk.Entry(self.frame_fiado_top)
        self.codigo_aba_dois.grid(row=0, column=1, sticky="ew")

        self.label_nome_aba_dois = ttk.Label(self.frame_fiado_top, text="Nome:")
        self.label_nome_aba_dois.grid(row=1, column=0, pady=10, sticky="w")

        self.nome_entry_tab2 = ttk.Entry(self.frame_fiado_top)
        self.nome_entry_tab2.grid(row=1, column=1, pady=10, columnspan=3, sticky="ew")

        self.sobrenome_label_aba_dois = ttk.Label(self.frame_fiado_top, text="Sobrenome:")
        self.sobrenome_label_aba_dois.grid(row=1, column=4, padx=10, sticky="ew")

        self.sobrenome_entry_aba_dois = ttk.Entry(self.frame_fiado_top)
        self.sobrenome_entry_aba_dois.grid(row=1, column=5, pady=10, sticky="ew")

        self.phone_tab2_top = ttk.Label(self.frame_fiado_top, text="Telefone:")
        self.phone_tab2_top.grid(row=3, column=0, pady=10, sticky="w")

        self.phone_top = ttk.Entry(self.frame_fiado_top)
        self.phone_top.grid(row=3, column=1,pady=5, sticky="ew")
        
        self.produto_tab2 = ttk.Label(self.frame_fiado_top, text="Produto:")
        self.produto_tab2.grid(row=3, column=2, pady=5,padx=10,sticky="w")

        self.produto_entry_tab2 = ttk.Entry(self.frame_fiado_top)
        self.produto_entry_tab2.grid(row=3, column=3, pady=10, sticky="ew")
        
        self.label_unidade_tab2 = ttk.Label(self.frame_fiado_top, text="Valor Unitario:")
        self.label_unidade_tab2.grid(row=3, column=4, pady=5,padx=10,sticky="e")

        self.entry_unidade_tab2 = ttk.Entry(self.frame_fiado_top)
        self.entry_unidade_tab2.grid(row=3, column=5, pady=10, sticky="ew")

        # Adicione os campos para data inicial e data final
        self.label_data_inicial = ttk.Label(self.frame_fiado_top, text="Data Inicial:")
        self.label_data_inicial.grid(row=4, column=0, pady=10, sticky="w")

        self.entry_data_inicial = ttk.Entry(self.frame_fiado_top)
        self.entry_data_inicial.grid(row=4, column=1, pady=10, sticky="ew")
        
        self.label_quantidade_tab2 = ttk.Label(self.frame_fiado_top, text="Quantidade:")
        self.label_quantidade_tab2.grid(row=4, column=2,padx=10, pady=5, sticky="ew")

        self.entry_quantidade_tab2 = ttk.Spinbox(self.frame_fiado_top, from_=0, to=1000, increment=1)
        self.entry_quantidade_tab2.grid(row=4, column=3, pady=5, sticky="ew")
        

        self.botao_limpar_codigo = ttk.Button(self.frame_fiado_top, text="Limpar", style="Custom.TButton", command=self.limpar_campos_tab2)
        self.botao_limpar_codigo.grid(row=5, column=0, padx=5, pady=5, sticky="news")

        self.botao_atualizar_cobrancas = ttk.Button(self.frame_fiado_top, text="Atualizar Cobranças", command=self.listar_cobrancas)
        self.botao_atualizar_cobrancas.grid(row=5, column=1,padx=5, pady=5, sticky="news")
 
        self.botao_buscar_cliente = ttk.Button(self.frame_fiado_top, text="Buscar Cliente", command=self.tela_de_busca_de_cliente_top, style="Custom.TButton")
        self.botao_buscar_cliente.grid(row=5, column=2, padx=5, pady=5)

        self.botao_buscar_produto = ttk.Button(self.frame_fiado_top, text="Buscar Produto", command=self.tela_de_busca_de_produto, style="Custom.TButton")
        self.botao_buscar_produto.grid(row=5, column=3, padx=5, pady=5)
        
        self.botao_inserir = ttk.Button(self.frame_fiado_top, text="Lançar", command=self.inserir_cliente_e_lancamento, style="Custom.TButton")
        self.botao_inserir.grid(row=5, column=4, pady=5)
        
        self.phone_entry_tab2.bind("<KeyRelease>", self.formatar_telefone_tab2) 
        self.editando = False
        self.entry_data_inicial.bind("<KeyRelease>", self.formatar_data)
    
    def campo_tela_aba_dois(self):
        
        # self.button_style = ttk.Style()
        # self.button_style.configure("Custom.TButton", padding=(5, 10)) 

        # self.list_genero = ["", "Masculino", "Feminino"]

        # self.list_empresa_PF = ["", "Pessoa Jurídica", "Pessoa Física"]

        self.label_codigo_aba_dois = ttk.Label(self.Widgets_frame, text="Código:")
        self.label_codigo_aba_dois.grid(row=0, column=0, pady=5, sticky="w")

        self.codigo_aba_dois = ttk.Entry(self.Widgets_frame)
        self.codigo_aba_dois.grid(row=0, column=1, sticky="ew")

        self.label_nome_aba_dois = ttk.Label(self.Widgets_frame, text="Nome:")
        self.label_nome_aba_dois.grid(row=1, column=0, pady=10, sticky="w")

        self.nome_entry_tab2 = ttk.Entry(self.Widgets_frame)
        self.nome_entry_tab2.grid(row=1, column=1, pady=10, columnspan=3, sticky="ew")

        self.sobrenome_label_aba_dois = ttk.Label(self.Widgets_frame, text="Sobrenome:")
        self.sobrenome_label_aba_dois.grid(row=1, column=4, padx=10, sticky="ew")

        self.sobrenome_entry_aba_dois = ttk.Entry(self.Widgets_frame)
        self.sobrenome_entry_aba_dois.grid(row=1, column=5, pady=10, sticky="ew")

        # self.phone_tab2 = ttk.Label(self.Widgets_frame, text="Telefone:")
        # self.phone_tab2.grid(row=3, column=0, pady=10, sticky="w")

        # self.phone_entry_tab2 = ttk.Entry(self.Widgets_frame)
        # self.phone_entry_tab2.grid(row=3, column=1,pady=5, sticky="ew")
        
        # self.produto_tab2 = ttk.Label(self.Widgets_frame, text="Produto:")
        # self.produto_tab2.grid(row=3, column=2, pady=5,padx=10,sticky="e")

        # self.produto_entry_tab2 = ttk.Entry(self.Widgets_frame)
        # self.produto_entry_tab2.grid(row=3, column=3, pady=10, sticky="ew")
        
        # self.label_unidade_tab2 = ttk.Label(self.Widgets_frame, text="Valor Unitario:")
        # self.label_unidade_tab2.grid(row=3, column=4, pady=5,padx=10,sticky="e")

        # self.entry_unidade_tab2 = ttk.Entry(self.Widgets_frame)
        # self.entry_unidade_tab2.grid(row=3, column=5, pady=10, sticky="ew")

        # # Adicione os campos para data inicial e data final
        # self.label_data_inicial = ttk.Label(self.Widgets_frame, text="Data Inicial:")
        # self.label_data_inicial.grid(row=4, column=0, pady=10, sticky="w")

        # self.entry_data_inicial = ttk.Entry(self.Widgets_frame)
        # self.entry_data_inicial.grid(row=4, column=1, pady=10, sticky="ew")
        
        # self.label_quantidade_tab2 = ttk.Label(self.Widgets_frame, text="Quantidade:")
        # self.label_quantidade_tab2.grid(row=4, column=2,padx=5, pady=10, sticky="ew")

        # self.entry_quantidade_tab2 = ttk.Spinbox(self.Widgets_frame, from_=0, to=1000, increment=1)
        # self.entry_quantidade_tab2.grid(row=4, column=3, pady=15, sticky="ew")
        
        self.botao_buscar_cliente = ttk.Button(self.Widgets_frame, text="Buscar Cliente", style="Custom.TButton")
        self.botao_buscar_cliente.grid(row=5, column=0, padx=5, pady=5, sticky="news")
        
        self.botao_lancar_fiado= ttk.Button(self.Widgets_frame, text="Lançar Fiado", style="Custom.TButton", command=self.tela_de_lancamento_fiado)
        self.botao_lancar_fiado.grid(row=5, column=1, padx=5, pady=5, sticky="news")
       

         
        self.botao_relatorio_cliente = ttk.Button(self.parte_de_baixo_frame, text="Relatorio", style="Custom.TButton")
        self.botao_relatorio_cliente.grid(row=0, column=1, padx=20, pady=5, sticky="news")
      
    def campos_tab3(self):
        self.button_style = ttk.Style()
        self.button_style.configure("Custom.TButton", padding=(5, 10)) 
        
        self.list_genero = ["", "Masculino", "Femninino"]
        
        self.list_empresa_PF = ["", "Pessoa Juridica", "Pessoa Fisica"]
         
        self.label_codigo = ttk.Label(self.frame_um_tab3, text="Código:")
        self.label_codigo.grid(row=0, column=0, pady=5, sticky="w")
        
        self.codigo = ttk.Entry(self.frame_um_tab3)
        self.codigo.grid(row=0, column=1, sticky="ew")
        
        self.label_nome = ttk.Label(self.frame_um_tab3, text="Nome:")
        self.label_nome.grid(row=1, column=0, pady=10, sticky="w")
        
        self.nome_entry_tab3 = ttk.Entry(self.frame_um_tab3, state="disabled")
        self.nome_entry_tab3.grid(row=1, column=1,pady=10, columnspan=3, sticky="ew")
        
        self.sobrenome_label = ttk.Label(self.frame_um_tab3, text="Sobrenome:")
        self.sobrenome_label.grid(row=1, column=4, padx=10,sticky="ew")
        
        self.sobrenome_entry = ttk.Entry(self.frame_um_tab3, state="disabled")
        self.sobrenome_entry.grid(row=1, column=5, pady=10, sticky="ew") 
        
        self.phone_tab3 = ttk.Label(self.frame_um_tab3, text="Telefone:")
        self.phone_tab3.grid(row=3, column=0,pady=10, sticky="w")
        
        self.phone_entry_tab3 = ttk.Entry(self.frame_um_tab3, state="disabled")
        self.phone_entry_tab3.grid(row=3, column=1, pady=10, sticky="ew")
        
        self.label_list_genero = ttk.Label(self.frame_um_tab3, text="Genero:")
        self.label_list_genero.grid(row=3, column=2, padx=10, pady=10)
        
        self.combobox_genero = ttk.Combobox(self.frame_um_tab3, value=self.list_genero, state="disabled")
        self.combobox_genero.grid(row=3, column=3, pady=10)
        
        self.label_cidade = ttk.Label(self.frame_um_tab3, text="Cidade:")
        self.label_cidade.grid(row=2, column=0,pady=10, sticky="w")
        
        self.entry_cidade = ttk.Entry(self.frame_um_tab3, state="disabled")
        self.entry_cidade.grid(row=2, column=1, pady=10)
        
        self.label_bairro = ttk.Label(self.frame_um_tab3, text="Bairro:")
        self.label_bairro.grid(row=2, column=2, pady=10)
        
        self.entry_bairro = ttk.Entry(self.frame_um_tab3, state="disabled")
        self.entry_bairro.grid(row=2, column=3, pady=10, sticky="ew")
        
        self.label_empresa = ttk.Label(self.frame_um_tab3, text="Empresa/Pessoa Fisica")
        self.label_empresa.grid(row=2, column=4, padx=5, pady=10)
       
        self.empresa_combobox = ttk.Combobox(self.frame_um_tab3, value=self.list_empresa_PF, state="disabled")
        self.empresa_combobox.grid(row=2, column=5, padx=5, pady=10)
        
        self.botao_buscar_cliente = ttk.Button(self.frame_um_tab3, text="Buscar", style="Custom.TButton")
        self.botao_buscar_cliente.grid(row=5, column=0, padx=5, pady=5, sticky="news")
       
        self.botao_limpar_codigo = ttk.Button(self.frame_um_tab3, text="Limpar", style="Custom.TButton", command=self.limpar_campos_tab3)
        self.botao_limpar_codigo.grid(row=5, column=1, padx=5, pady=5, sticky="news")       
        
        self.botao_criar = ttk.Button(self.frame_um_tab3, text="Criar Cliente", style="Custom.TButton", command=self.criar_cliente_top_level)
        self.botao_criar.grid(row=5, column=2, padx=5, pady=5, sticky="news")
        
        self.botao_alterar = ttk.Button(self.frame_um_tab3, text="Alterar", command=self.habilitar_edicao,style="Custom.TButton")
        self.botao_alterar.grid(row=5, column=5, pady=5)        
        
        self.botao_buscar_cliente = ttk.Button(self.frame_um_tab3, text="Salvar", command=self.salvar_edicao, style="Custom.TButton")
        self.botao_buscar_cliente.grid(row=5, column=6, pady=5)
         
        self.botao_relatorio_cliente = ttk.Button(self.frame_tres_tab3, text="Relatorio", style="Custom.TButton")
        self.botao_relatorio_cliente.grid(row=0, column=1, padx=20, pady=5, sticky="news")
        
        self.phone_entry_tab3.bind("<KeyRelease>", self.formatar_telefone_tab3)
        self.editando = False
 
    def criar_cliente_top_level(self):
        self.janela_criar_cliente = Toplevel(self.janela)
        self.janela_criar_cliente.title("Cadastro de cliente")
        self.janela_criar_cliente.geometry("450x350")
        self.janela_criar_cliente.resizable(False, False)
        self.janela_criar_cliente.transient(self.janela)
        self.janela_criar_cliente.focus_force()
        self.janela_criar_cliente.grab_set()
        
        self.frame_criar_cliente = ttk.Labelframe(self.janela_criar_cliente)
        self.frame_criar_cliente.grid(row=0, column=0, sticky="ew")
        
        self.frame_botoes_criar_cliente = ttk.Labelframe(self.janela_criar_cliente)
        self.frame_botoes_criar_cliente.grid(row=1, column=0, sticky="ew")
         
        self.janela_criar_cliente.columnconfigure(0, weight=1)
        
        # Configura a coluna 0 para expandir no centro
        self.frame_botoes_criar_cliente.columnconfigure(0, weight=1)
        
        self.label_nome_top_level = ttk.Label(self.frame_criar_cliente, text="Nome")
        self.label_nome_top_level.grid(row=0, column=0, pady=5, sticky="w")
        
        self.entry_nome_top_level = ttk.Entry(self.frame_criar_cliente)
        self.entry_nome_top_level.grid(row=0, column=1, pady=5, sticky="ew")
        
        self.label_sobrenome_top_level = ttk.Label(self.frame_criar_cliente, text="Sobrenome")
        self.label_sobrenome_top_level.grid(row=1, column=0, pady=5, sticky="w")
        
        self.entry_sobrenome_top_level = ttk.Entry(self.frame_criar_cliente)
        self.entry_sobrenome_top_level.grid(row=1, column=1, pady=5, sticky="ew")
        
        self.label_cidade_top_level = ttk.Label(self.frame_criar_cliente, text="Cidade")
        self.label_cidade_top_level.grid(row=2, column=0, pady=5, sticky="w")
        
        self.entry_cidade_top_level = ttk.Entry(self.frame_criar_cliente)
        self.entry_cidade_top_level.grid(row=2, column=1, pady=5, sticky="ew")
        
        self.label_bairro_top_level = ttk.Label(self.frame_criar_cliente, text="Bairro")
        self.label_bairro_top_level.grid(row=3, column=0, pady=5, sticky="w")
        
        self.entry_bairro_top_level = ttk.Entry(self.frame_criar_cliente)
        self.entry_bairro_top_level.grid(row=3, column=1, pady=5, sticky="ew")
        
        self.label_telefone_top_level = ttk.Label(self.frame_criar_cliente, text="Telefone")
        self.label_telefone_top_level.grid(row=4, column=0, pady=5, sticky="w")
        
        self.entry_telefone_top_level = ttk.Entry(self.frame_criar_cliente)
        self.entry_telefone_top_level.grid(row=4, column=1, pady=5, sticky="ew")
        
        self.label_genero_toplevel = ttk.Label(self.frame_criar_cliente, text="Genero")
        self.label_genero_toplevel.grid(row=5, column=0, pady=10, sticky="w")
        
        self.combobox_genero_toplevel = ttk.Combobox(self.frame_criar_cliente, value=self.list_genero)
        self.combobox_genero_toplevel.grid(row=5, column=1, pady=5)
      
        self.label_tipo_empresa = ttk.Label(self.frame_criar_cliente, text="Empresa ou Pessoa Fisica")
        self.label_tipo_empresa.grid(row=6, column=0, pady=5)
         
        self.empresa_combobox_toplevel = ttk.Combobox(self.frame_criar_cliente, value=self.list_empresa_PF)
        self.empresa_combobox_toplevel.grid(row=6, column=1, pady=5) 
         
        self.botao_cadastrar = ttk.Button(self.frame_botoes_criar_cliente, text="Cadastrar", command=self.add_clientes)
        self.botao_cadastrar.grid(row=0, column=1, pady=5, sticky="ew")
       
        self.separador_toplevel = ttk.Separator(self.frame_botoes_criar_cliente, orient="vertical")
        self.separador_toplevel.grid(row=0, column=2, padx=20, pady=5, sticky="ns")
        
        self.botao_limpar = ttk.Button(self.frame_botoes_criar_cliente, text="Limpar", command=self.limpar)
        self.botao_limpar.grid(row=0, column=3,padx=5, pady=5, sticky="ew")
        
        # Coluna vazia à esquerda dos botões
        self.frame_botoes_criar_cliente.grid_columnconfigure(0, weight=1)
        # Coluna vazia à direita dos botões
        self.frame_botoes_criar_cliente.grid_columnconfigure(4, weight=1)
        
        # Vincula o evento de digitação para formatar automaticamente o telefone
        self.entry_telefone_top_level.bind("<KeyRelease>", self.formatar_telefone)

    def tela_treeview_cliente(self):
        self.columns_cliente = ("Código","Nome","Sobrenome","Genero","Cidade","Bairro","Telefone" ,"Empresa/PF")
        self.treeview_cliente = ttk.Treeview(self.frame_dois_tab3, show="headings", columns=self.columns_cliente, height=16)
        self.treeview_cliente.column("Código", width=50)
        self.treeview_cliente.column("Nome", width=180)
        self.treeview_cliente.column("Sobrenome", width=100) 
        self.treeview_cliente.column("Genero", width=100)
        self.treeview_cliente.column("Cidade", width=150)
        self.treeview_cliente.column("Bairro", width=100) 
        self.treeview_cliente.column("Telefone", width=80)     
        self.treeview_cliente.column("Empresa/PF", width=200)
        
        self.treeview_cliente.heading("Código", text="Código")
        self.treeview_cliente.heading("Nome", text="Nome")
        self.treeview_cliente.heading("Sobrenome", text="Sobrenome")       
        self.treeview_cliente.heading("Genero",text="Genero")
        self.treeview_cliente.heading("Cidade", text="Cidade")
        self.treeview_cliente.heading("Bairro", text="Bairro")
        self.treeview_cliente.heading("Telefone", text="Telefone")   
        self.treeview_cliente.heading("Empresa/PF", text="Empresa/PF")
        
        # Adicione uma barra de rolagem vertical
        self.scrollbar = ttk.Scrollbar(self.frame_dois_tab3, orient="vertical", command=self.treeview_cliente.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.treeview_cliente.configure(yscrollcommand=self.scrollbar.set) 
        
        self.treeview_cliente.pack(padx=10, pady=10, fill=tk.BOTH, expand=True) 
 
    def campos_tab4(self):
 
        # Widgets no Frame 1
        self.nome_codigo = ttk.Label(self.frame_um_tab4, text='Codigo:')
        self.nome_codigo.grid(row=0, column=0, pady=5, sticky="w") 
        self.nome_codigo_entry = ttk.Entry(self.frame_um_tab4)
        self.nome_codigo_entry.grid(row=0, column=1, pady=5, sticky="ew") 
        # Produto
        self.nome_label = ttk.Label(self.frame_um_tab4, text='Produto:')
        self.nome_label.grid(row=0, column=2, pady=5, sticky="w") 
        self.nome_produto_entry = ttk.Entry(self.frame_um_tab4)
        self.nome_produto_entry.grid(row=0, column=3, pady=5, sticky="ew")
       
        # valor unitario 
        self.valor_unitario_label = ttk.Label(self.frame_um_tab4, text='Valor Unitario:')
        self.valor_unitario_label.grid(row=0, column=4, padx=5, pady=5, sticky="w") 
        self.valor_unitario_entry = ttk.Spinbox(self.frame_um_tab4, from_=0.0, to=1000, increment=0.1)
        self.valor_unitario_entry.grid( row=0, column=5,  padx=5,pady=5, sticky="ew")
        
        # Quantidade 
        self.qntd_label = ttk.Label(self.frame_um_tab4, text='Quantidade:') 
        self.qntd_label.grid(row=1, column=0, pady=5, sticky="w")
        self.quantidade_entry = ttk.Spinbox(self.frame_um_tab4, from_=1, to=1000, increment=1)
        self.quantidade_entry.grid(row=1, column=1, pady=10, sticky="ew") 
       
        # Fornecedor 
        self.fornecedor_label = ttk.Label(self.frame_um_tab4, text='Fornecedor:')
        self.fornecedor_label.grid(row=1, column=2, padx=5, pady=5, sticky="w") 
        self.fornecedor_entry = ttk.Entry(self.frame_um_tab4)
        self.fornecedor_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
         

        self.tipo_produto_label = ttk.Label(self.frame_um_tab4, text='Tipo do Produto:')
        self.tipo_produto_label.grid(row=2, column=0, pady=5, sticky="w")
        self.tipo_produto_combobox = ttk.Combobox(self.frame_um_tab4, values=["Milímetros", "Metros", "Líquido", "Caixa", 'Pacote', 'Unidade'])
        self.tipo_produto_combobox.grid(row=2, column=1,  pady=5, sticky="ew")
        
        self.adicionar_produto_button = ttk.Button(self.frame_um_tab4, text="Adicionar Produto", command=self.inserir_produto)
        self.adicionar_produto_button.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.excluir_produto = ttk.Button(self.frame_um_tab4, text="Excluir Produto", command=self.excluir_produto_do_bd)
        self.excluir_produto.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        self.alterar_produto = ttk.Button(self.frame_um_tab4, text="Alterar Produto", command=self.atualizar_produto_no_bd)
        self.alterar_produto.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        
        self.executar_busca_produto = ttk.Button(self.frame_um_tab4, text="Buscar", command=self.cadastro_produto_tab4)
        self.executar_busca_produto.grid(row=3, column=3, padx=5, pady=5, sticky="w")
    
    def treeeview_tab4(self):
        self.columns_produto = ("Codigo","Produto","Valor Unitario","Quantidade","Fornecedor","Tipo do Produto")
        self.treeview_produto = ttk.Treeview(self.frame_tab4, show="headings", columns=self.columns_produto, height=16)
        self.treeview_produto.column("Codigo", width=50)
        self.treeview_produto.column("Produto", width=50)
        self.treeview_produto.column("Valor Unitario", width=180)
        self.treeview_produto.column("Quantidade", width=100) 
        self.treeview_produto.column("Fornecedor", width=100)
        self.treeview_produto.column("Tipo do Produto", width=150)
       
        self.treeview_produto.heading("Codigo", text="Codigo")
        self.treeview_produto.heading("Produto", text="Produto")
        self.treeview_produto.heading("Valor Unitario", text="Valor Unitario")
        self.treeview_produto.heading("Quantidade", text="Quantidade")       
        self.treeview_produto.heading("Fornecedor",text="Fornecedor")
        self.treeview_produto.heading("Tipo do Produto", text="Tipo do Produto")

        
        # Adicione uma barra de rolagem vertical
        self.scrollbar = ttk.Scrollbar(self.frame_tab4, orient="vertical", command=self.treeview_produto.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.treeview_produto.configure(yscrollcommand=self.scrollbar.set) 
        
        self.treeview_produto.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.treeview_produto.bind("<Return>", self.selecionar_produto_tab4)
        self.treeview_produto.bind("<Double-1>", self.selecionar_produto_tab4)  
    
    def cadastro_produto_tab4(self):
        self.janela_cadastrar_cliente = Toplevel(self.janela)
        self.janela_cadastrar_cliente.title("Cadastro de cliente")
        self.janela_cadastrar_cliente.geometry("450x350")
        self.janela_cadastrar_cliente.resizable(False, False)
        self.janela_cadastrar_cliente.transient(self.janela)
        self.janela_cadastrar_cliente.focus_force()
        self.janela_cadastrar_cliente.grab_set()
    
    def tela_de_busca_de_produto(self):
        self.janela_procurar_produto = Toplevel(self.janela)
        self.janela_procurar_produto.title("Busca de produto")
        self.janela_procurar_produto.geometry("810x500")
        self.janela_procurar_produto.resizable(False, False)
        self.janela_procurar_produto.transient(self.janela)
        self.janela_procurar_produto.focus_force()
        self.janela_procurar_produto.grab_set()
        
        largura = 810
        altura = 500
        x = (self.janela_procurar_produto.winfo_screenwidth() - largura) // 2
        y = (self.janela_procurar_produto.winfo_screenheight() - altura) // 2
        self.janela_procurar_produto.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.frame_um_top_tab2 = ttk.Labelframe(self.janela_procurar_produto)
        self.frame_um_top_tab2.pack(fill='both', expand=True)
         
        self.label_busca_produto = ttk.Label(self.frame_um_top_tab2, text='Buscar Produto:')
        self.label_busca_produto.pack(side='left', pady=10)
        
        self.produto_buscar = ttk.Entry(self.frame_um_top_tab2)
        self.produto_buscar.pack(side='left', pady=10, fill='x', expand=True)
        
        self.botao_produto = ttk.Button(
            self.frame_um_top_tab2, text='Buscar', command=self.busca_produto_top)
        self.botao_produto.pack(side='right', pady=10)
         
        self.frame_dois_top_tab2 = ttk.Labelframe(self.janela_procurar_produto)
        self.frame_dois_top_tab2.pack(fill='both', expand=True)
       
        self.frame_tres_top_tab2 = ttk.Frame(self.frame_dois_top_tab2)
        self.frame_tres_top_tab2.pack(fill='both', expand=True)
           
        self.columns_produto = ('Codigo',"Produto","Valor Unitario","Quantidade","Fornecedor","Tipo do Produto")
        self.treeview_produto_top = ttk.Treeview(self.frame_tres_top_tab2, show="headings", columns=self.columns_produto, height=16)
        self.treeview_produto_top.column("Codigo", width=80) 
        self.treeview_produto_top.column("Produto", width=200)
        self.treeview_produto_top.column("Valor Unitario", width=80)
        self.treeview_produto_top.column("Quantidade", width=80) 
        self.treeview_produto_top.column("Fornecedor", width=150)
        self.treeview_produto_top.column("Tipo do Produto", width=80)
        
        self.treeview_produto_top.heading("Codigo", text="Codigo")
        self.treeview_produto_top.heading("Produto", text="Produto")
        self.treeview_produto_top.heading("Valor Unitario", text="Valor Unitario")
        self.treeview_produto_top.heading("Quantidade", text="Quantidade")       
        self.treeview_produto_top.heading("Fornecedor",text="Fornecedor")
        self.treeview_produto_top.heading("Tipo do Produto", text="Tipo do Produto")

        
        self.scrollbar = ttk.Scrollbar(self.frame_tres_top_tab2, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")
         
        self.treeview_produto_top.pack(padx=10, pady=10, fill=tk.BOTH, expand=True) 
        # Adicione uma barra de rolagem vertical
        self.scrollbar.config(command=self.treeview_produto_top.yview)
  
        self.treeview_produto_top.bind("<Double-1>", self.selecionar_produto) 
        # self.treeview_produto_top.bind("<<TreeviewSelect>>", self.selecionar_produto) 
        self.treeview_produto_top.bind("<Return>", self.selecionar_produto) 
        self.janela_procurar_produto.columnconfigure(0, weight=1)
    
    def selecionar_produto(self, event):
        # Obtém o item selecionado na treeview
        item_selecionado = self.treeview_produto_top.selection()

        if item_selecionado:
            # Recupera os valores do item selecionado
            valores = self.treeview_produto_top.item(item_selecionado, 'values')

            # Exibe os valores onde você precisar
            print("Produto selecionado:", valores)

            produto_info = (valores[1], valores[2])

            if produto_info:
                # O produto foi encontrado, você pode acessar as informações aqui
                descricao, valor_unitario = produto_info
                self.produto_entry_tab2.delete(0, END)
                self.produto_entry_tab2.insert(0, descricao)
                self.entry_unidade_tab2.delete(0, END)
                self.entry_unidade_tab2.insert(0, valor_unitario)
            else:
                messagebox.showerror("Produto não encontrado", "Produto não encontrado no banco de dados.")

            self.janela_procurar_produto.destroy()
    
    def selecionar_cliente(self, event):
            # Obtém o item selecionado na treeview
        item_selecionado = self.treeview_cliente_top.selection()

        if item_selecionado:
            # Recupera os valores do item selecionado
            valores = self.treeview_cliente_top.item(item_selecionado, 'values')

            # Exibe os valores onde você precisar
            print("Produto selecionado:", valores)

            produto_info = (valores[1], valores[2],valores[6])

            if produto_info:
                # O produto foi encontrado, você pode acessar as informações aqui
                nome, sobrenome, telefone = produto_info
                self.nome_entry_tab2.delete(0, END)
                self.nome_entry_tab2.insert(0, nome)
                self.sobrenome_entry_aba_dois.delete(0, END)
                self.sobrenome_entry_aba_dois.insert(0, sobrenome)
                self.phone_entry_tab2.delete(0, END)
                self.phone_entry_tab2.insert(0, telefone)
            else:
                messagebox.showerror("Produto não encontrado", "Produto não encontrado no banco de dados.")

            self.janela_procurar_cliente.destroy()
     
    def pdv(self):
        
        self.label_produto = ttk.Label(self.frame_um_tab5, text='Produto:')
        self.label_produto.pack(side='left',  pady=5, padx=5)
         
        self.entry_produto_pdv = ttk.Entry(self.frame_um_tab5)
        self.entry_produto_pdv.pack(side='left', pady=5, padx=5,fill='both', expand=True)
        
        self.botao_busca_produto_pdv = ttk.Button(self.frame_um_tab5, text='Busca')
        self.botao_busca_produto_pdv.pack(side='right', pady=5, padx=5) 
        
        self.entry_qnt_tab5 = ttk.Entry(self.frame_cinco_tab5)
        self.entry_qnt_tab5.pack(padx=10,pady=5, expand=True)
        
        self.label_qnt_pdv = ttk.Label(self.frame_cinco_tab5, text= 'Quantidade')
        self.label_qnt_pdv.pack(fill='both',pady=5, expand=True, anchor='e')
        
        self.entry_valor_unt_tab5 = ttk.Entry(self.frame_cinco_tab5)
        self.entry_valor_unt_tab5.pack( padx=10,pady=5, expand=True)
        
        self.label_valor_unt_pdv = ttk.Label(self.frame_cinco_tab5, text= 'Valor Unitário')
        self.label_valor_unt_pdv.pack(fill='both',pady=5,expand=True, anchor='e')
        
        self.entry_total_item_tab5 = ttk.Entry(self.frame_cinco_tab5)
        self.entry_total_item_tab5.pack(padx=10,pady=5, expand=True)
        
        self.label_total_item_pdv = ttk.Label(self.frame_cinco_tab5, text= 'Total Item')
        self.label_total_item_pdv.pack(fill='both',pady=5,expand=True, anchor='e')
        
        self.entry_total_tab5 = ttk.Entry(self.frame_cinco_tab5)
        self.entry_total_tab5.pack(padx=10, pady=5,expand=True)
        
        self.label_total_compra_pdv = ttk.Label(self.frame_cinco_tab5, text= 'Total')
        self.label_total_compra_pdv.pack(fill='both',pady=5,expand=True, anchor='e')
       
        self.label_codigo_produto_pdv = ttk.Label(self.frame_quatro_tab5, text='Código Produto:')
        self.label_codigo_produto_pdv.pack(side='left', padx=5, pady=5)

        self.codigo_produto_pdv = ttk.Entry(self.frame_quatro_tab5)
        self.codigo_produto_pdv.pack(side='left', pady=5, padx=5,fill='both', expand=True)

    def tree_pdv(self):
        self.invoice_list_tab5 = []
        
        self.columns = ("Item", "Código", "Descrição", "Qtde", "Un", "Vl. Unitário", "Total Item")
        self.tree_tab5 = ttk.Treeview(self.frame_dois_tab5, columns= self.columns, show="headings", height=18) 
        
        self.tree_tab5.column("Item", width=5)
        self.tree_tab5.column("Código", width=20)
        self.tree_tab5.column("Descrição", width=30)
        self.tree_tab5.column("Qtde", width=15)
        self.tree_tab5.column("Un", width=30)
        self.tree_tab5.column("Vl. Unitário", width=15)
        self.tree_tab5.column("Total Item", width=30)
        
        
        self.tree_tab5.heading("Item", text="Item")
        self.tree_tab5.heading("Código", text="Código")
        self.tree_tab5.heading("Descrição",text="Descrição")
        self.tree_tab5.heading("Qtde", text="Qtde")
        self.tree_tab5.heading("Un", text="Un")
        self.tree_tab5.heading("Vl. Unitário", text="Vl. Unitário")
        self.tree_tab5.heading("Total Item", text="Total Item")
        
        self.tree_tab5.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    def tela_de_busca_de_cliente_top(self):
        self.janela_procurar_cliente = Toplevel(self.janela)
        self.janela_procurar_cliente.title("Busca de cliente")
        self.janela_procurar_cliente.geometry("810x500")
        self.janela_procurar_cliente.resizable(False, False)
        self.janela_procurar_cliente.transient(self.janela)
        self.janela_procurar_cliente.focus_force()
        self.janela_procurar_cliente.grab_set()
        
        largura = 1200
        altura = 600
        x = (self.janela_procurar_cliente.winfo_screenwidth() - largura) // 2
        y = (self.janela_procurar_cliente.winfo_screenheight() - altura) // 2
        self.janela_procurar_cliente.geometry(f'{largura}x{altura}+{x}+{y}')
        
        self.frame_um_top_cliente = ttk.Labelframe(self.janela_procurar_cliente)
        self.frame_um_top_cliente.pack(fill='both', expand=True)
         
        self.label_busca_cliente = ttk.Label(self.frame_um_top_cliente, text='Buscar cliente:')
        self.label_busca_cliente.pack(side='left', pady=10)
        
        self.produto_cliente = ttk.Entry(self.frame_um_top_cliente)
        self.produto_cliente.pack(side='left', pady=10, fill='x', expand=True)
        
        self.botao_cliente = ttk.Button(self.frame_um_top_cliente, text='Buscar', command=self.busca_cliente_top)
        self.botao_cliente.pack(side='right', pady=10)
         
        self.frame_dois_top_cliente = ttk.Labelframe(self.janela_procurar_cliente)
        self.frame_dois_top_cliente.pack(fill='both', expand=True)
       
        self.frame_tres_top_cliente = ttk.Frame(self.frame_dois_top_cliente)
        self.frame_tres_top_cliente.pack(fill='both', expand=True)
           
        self.columns_cliente = ("Código","Nome","Sobrenome","Genero","Cidade","Bairro","Telefone" ,"Empresa/PF")
        self.treeview_cliente_top = ttk.Treeview(self.frame_tres_top_cliente, show="headings", columns=self.columns_cliente, height=16)
        self.treeview_cliente_top.column("Código", width=50)
        self.treeview_cliente_top.column("Nome", width=180)
        self.treeview_cliente_top.column("Sobrenome", width=100)
        self.treeview_cliente_top.column("Genero", width=100)
        self.treeview_cliente_top.column("Cidade", width=150)
        self.treeview_cliente_top.column("Bairro", width=100) 
        self.treeview_cliente_top.column("Telefone", width=80) 
        self.treeview_cliente_top.column("Empresa/PF", width=200)
        
        self.treeview_cliente_top.heading("Código", text="Código")
        self.treeview_cliente_top.heading("Nome", text="Nome")
        self.treeview_cliente_top.heading("Sobrenome", text="Sobrenome")  
        self.treeview_cliente_top.heading("Genero",text="Genero")     
        self.treeview_cliente_top.heading("Cidade", text="Cidade")
        self.treeview_cliente_top.heading("Bairro", text="Bairro")
        self.treeview_cliente_top.heading("Telefone", text="Telefone") 
        self.treeview_cliente_top.heading("Empresa/PF", text="Empresa/PF")

        self.scrollbar_cliente = ttk.Scrollbar(
            self.frame_tres_top_cliente, orient="vertical")
        self.scrollbar_cliente.pack(side="right", fill="y")
         
        self.treeview_cliente_top.pack(padx=10, pady=10, fill=tk.BOTH, expand=True) 
        # Adicione uma barra de rolagem vertical
        self.scrollbar.config(command=self.treeview_cliente_top.yview)
  
        self.treeview_cliente_top.bind("<Double-1>", self.selecionar_cliente) 
        # self.treeview_produto_top.bind("<<TreeviewSelect>>", self.selecionar_produto) 
        self.treeview_cliente_top.bind("<Return>", self.selecionar_cliente) 
        self.janela_procurar_cliente.columnconfigure(0, weight=1)

class Application(tela):

    def __init__(self):
        super().__init__()
        self.janela.mainloop()


if __name__ == "__main__":
    app = Application()
    banco = Bancodedados()
