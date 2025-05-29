import tkinter as tk
from tkinter import ttk

# ------------------------------------------------------------------------------
# 7. Criação do bloco inferior com Notebook (duas abas)
# ------------------------------------------------------------------------------
def criar_bloco_inferior(root, tabela_sintatica):
    """Cria o bloco inferior com três abas: Log, Tabela de Lexemas e Tabela Sintática."""
    print("\nCriando bloco inferior...")
    print(f"Tabela sintática recebida tem {len(tabela_sintatica)} não-terminais")
    print(f"Não-terminais: {sorted(tabela_sintatica.keys())}")
    
    notebook = ttk.Notebook(root)
    notebook.grid(row=1, column=0, sticky="nsew")

    # Aba: Log de Compilação
    frame_log = ttk.Frame(notebook)
    text_log = tk.Text(frame_log)
    text_log.pack(expand=True, fill="both")
    notebook.add(frame_log, text="Log de Compilação")

    # Aba: Tabela de Lexemas
    frame_lexemas = ttk.Frame(notebook)
    colunas_lexemas = ("Lexema", "Token", "Erro", "Linha", "ColIni", "ColFim")
    tree_lexemas = ttk.Treeview(frame_lexemas, columns=colunas_lexemas, show="headings")

    # Configura o alinhamento e largura das colunas da tabela de lexemas
    for col in colunas_lexemas:
        tree_lexemas.heading(col, text=col)
        # Centraliza colunas numéricas
        if col in ["Linha", "ColIni", "ColFim"]:
            tree_lexemas.column(col, width=100, anchor="center")
        else:
            tree_lexemas.column(col, width=100)

    # Adiciona scrollbars para a tabela de lexemas
    vsb_lexemas = ttk.Scrollbar(frame_lexemas, orient="vertical", command=tree_lexemas.yview)
    hsb_lexemas = ttk.Scrollbar(frame_lexemas, orient="horizontal", command=tree_lexemas.xview)
    tree_lexemas.configure(yscrollcommand=vsb_lexemas.set, xscrollcommand=hsb_lexemas.set)
    
    # Posiciona os elementos usando grid
    tree_lexemas.grid(row=0, column=0, sticky="nsew")
    vsb_lexemas.grid(row=0, column=1, sticky="ns")
    hsb_lexemas.grid(row=1, column=0, sticky="ew")
    
    # Configura o grid
    frame_lexemas.grid_rowconfigure(0, weight=1)
    frame_lexemas.grid_columnconfigure(0, weight=1)

    notebook.add(frame_lexemas, text="Tabela de Lexemas")

    # Aba: Tabela Sintática
    frame_tabela = ttk.Frame(notebook)
    frame_tabela.grid_rowconfigure(0, weight=1)
    frame_tabela.grid_columnconfigure(0, weight=1)
    
    # Lista de todos os terminais possíveis na ordem desejada
    terminais = [
        'PALAVRA_RESERVADA_PROGRAM',
        'PALAVRA_RESERVADA_BEGIN',
        'PALAVRA_RESERVADA_END',
        'PALAVRA_RESERVADA_END_PONTO',
        'PALAVRA_RESERVADA_IF',
        'PALAVRA_RESERVADA_THEN',
        'PALAVRA_RESERVADA_ELSE',
        'PALAVRA_RESERVADA_WHILE',
        'PALAVRA_RESERVADA_DO',
        'PALAVRA_RESERVADA_READ',
        'PALAVRA_RESERVADA_WRITE',
        'PALAVRA_RESERVADA_TRUE',
        'PALAVRA_RESERVADA_FALSE',
        'PALAVRA_RESERVADA_INT',
        'PALAVRA_RESERVADA_BOOLEAN',
        'PALAVRA_RESERVADA_VAR',
        'PALAVRA_RESERVADA_PROCEDURE',
        'IDENTIFICADOR',
        'NUMERO_INTEIRO',
        'NUMERO_REAL',
        'OPERADOR_SOMA',
        'OPERADOR_SUBTRACAO',
        'OPERADOR_MULTIPLICACAO',
        'OPERADOR_DIV',
        'MENOR',
        'MAIOR',
        'MENOR_IGUAL',
        'MAIOR_IGUAL',
        'IGUALDADE',
        'DIFERENTE',
        'ATRIBUICAO',
        'VIRGULA',
        'PONTO_E_VIRGULA',
        'ABRE_PARENTESES',
        'FECHA_PARENTESES',
        'SEPARADOR',
        'PONTO',
        '$'
    ]
    print("frame_tabela", frame_tabela)
    # Configura a tabela sintática com as colunas
    colunas_sintatica = ["Não Terminal"] + terminais
    print(f"Colunas da tabela sintática: {colunas_sintatica}")
    tree_sintatica = ttk.Treeview(frame_tabela, columns=colunas_sintatica, show="headings")

    # Configura o estilo para linhas mais altas
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)  # Reduzindo de 80 para 25 pixels

    # Configura os cabeçalhos e larguras das colunas
    tree_sintatica.heading("Não Terminal", text="Não Terminal")
    tree_sintatica.column("Não Terminal", width=150, minwidth=100, anchor="center")
    
    # Define larguras diferentes para diferentes tipos de terminais
    for col in terminais:
        tree_sintatica.heading(col, text=col)
        # Palavras reservadas e identificadores precisam de mais espaço
        if col.startswith('PALAVRA_RESERVADA_') or col == 'IDENTIFICADOR':
            tree_sintatica.column(col, width=250, minwidth=200, anchor="center")
        # Operadores e símbolos especiais precisam de menos espaço
        elif col.startswith('OPERADOR_') or col in ['MENOR', 'MAIOR', 'VIRGULA', 'PONTO_E_VIRGULA', 'PONTO', '$']:
            tree_sintatica.column(col, width=80, minwidth=60, anchor="center")
        # Outros tokens têm tamanho médio
        else:
            tree_sintatica.column(col, width=120, minwidth=100, anchor="center")

    # Adiciona scrollbars para a tabela sintática
    vsb_sintatica = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree_sintatica.yview)
    hsb_sintatica = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tree_sintatica.xview)
    tree_sintatica.configure(yscrollcommand=vsb_sintatica.set, xscrollcommand=hsb_sintatica.set)
    
    # Posiciona os elementos usando grid
    tree_sintatica.grid(row=0, column=0, sticky="nsew")
    vsb_sintatica.grid(row=0, column=1, sticky="ns")
    hsb_sintatica.grid(row=1, column=0, sticky="ew")

    notebook.add(frame_tabela, text="Tabela Sintática")
    
    # Configura o notebook para expandir
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Tenta popular a tabela sintática inicialmente
    try:
        from compiler.executor import popular_tabela_sintatica
        popular_tabela_sintatica(tree_sintatica)
    except Exception as e:
        print(f"Erro ao popular tabela sintática inicialmente: {str(e)}")
        import traceback
        traceback.print_exc()

    return tree_lexemas, text_log, tree_sintatica

def obter_todos_terminais(tabela):
    terminais = set()
    for producoes in tabela.values():
        terminais.update(producoes.keys())
    return sorted(terminais)
