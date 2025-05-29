from tkinter import Menu, filedialog
from compiler.executor import executar_analise

import tkinter as tk

# ------------------------------------------------------------------------------
# 4. Criação do Menu
# ------------------------------------------------------------------------------
def criar_menu(root, text_area, tree, text_log, tree_sintatica):
    """Cria a barra de menu e adiciona ao root."""
    print("\nCriando menu...")
    
    menubar = tk.Menu(root)

    # Menu "Arquivo"
    menu_arquivo = tk.Menu(menubar, tearoff=False)
    menu_arquivo.add_command(label="Novo")
    menu_arquivo.add_command(label="Abrir", command=lambda: abrir_arquivo(text_area, tree, text_log, tree_sintatica))
    menu_arquivo.add_command(label="Salvar")
    menu_arquivo.add_separator()
    menu_arquivo.add_command(label="Sair", command=root.quit)
    menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

    # Menu "Editar"
    menu_editar = tk.Menu(menubar, tearoff=False)
    menu_editar.add_command(label="Desfazer")
    menu_editar.add_command(label="Refazer")
    menubar.add_cascade(label="Editar", menu=menu_editar)

    # Menu "Exibir"
    menu_exibir = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Exibir", menu=menu_exibir)

    # Menu "Localizar"
    menu_localizar = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Localizar", menu=menu_localizar)

    # Menu "Compiler"
    menu_compiler = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Compiler", menu=menu_compiler)

    # Menu "Executar" - faz a análise e preenche a tabela
    menu_executar = tk.Menu(menubar, tearoff=False)
    menu_executar.add_command(
        label="Executar Análise Sintática",
        command=lambda: executar_analise(text_area, tree, text_log, options="executar", tree_sintatica=tree_sintatica)
    )
    menu_executar.add_command(
        label="Executar Análise Léxica",
        command=lambda: executar_analise(text_area, tree, text_log, options="analise_lexica", tree_sintatica=tree_sintatica)
    )
    menu_executar.add_command(
        label="Executar Análise Semântica",
        command=lambda: executar_analise(text_area, tree, text_log, options="analise_semantica", tree_sintatica=tree_sintatica)
    )
    menubar.add_cascade(label="Executar", menu=menu_executar)
    

    # Menu "Ajuda"
    menu_ajuda = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

    # Atribui a barra de menus à janela principal
    root.config(menu=menubar)

# ------------------------------------------------------------------------------
# 5. Abertura de Arquivo (para carregar texto no editor)
# ------------------------------------------------------------------------------
def abrir_arquivo(text_area, tree, text_log, tree_sintatica):
    """Abre um arquivo de texto e carrega o conteúdo na área de texto."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )
    if file_path:
        try:
            # Limpa a área de texto
            text_area.delete("1.0", tk.END)
            
            # Habilita, limpa e desabilita o log
            text_log.config(state='normal')
            text_log.delete("1.0", tk.END)
            text_log.config(state='disabled')
            
            # Limpa apenas a tabela de lexemas
            for item in tree.get_children():
                tree.delete(item)
            
            # Carrega o novo arquivo
            with open(file_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            text_area.insert("1.0", conteudo)
            
            # Atualiza o log
            text_log.config(state='normal')
            text_log.insert("1.0", f"Arquivo carregado com sucesso: {file_path}\n")
            text_log.config(state='disabled', foreground='green')
            
        except Exception as e:
            text_log.config(state='normal')
            text_log.delete("1.0", tk.END)
            text_log.insert("1.0", f"Erro ao ler o arquivo: {e}\n")
            text_log.config(state='disabled', foreground='red')
