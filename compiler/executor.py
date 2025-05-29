from compiler.lexer import analisar_expressao
from compiler.syntatic_analyzer import analisar_declaracoes, tabela_sintatica
from datetime import datetime
import tkinter as tk

print("\nImportando módulos...")
print(f"Tabela sintática importada tem {len(tabela_sintatica)} não-terminais")
print(f"Não-terminais: {sorted(tabela_sintatica.keys())}")

def get_timestamp():
    """Retorna um timestamp formatado para o log."""
    return datetime.now().strftime("[%H:%M:%S] ")

# ------------------------------------------------------------------------------
# 2. Função para popular o Treeview com o resultado da análise
# ------------------------------------------------------------------------------
def popular_tabela_lexemas(tree, tokens):
    """
    Recebe o Treeview (tabela) e a lista de tokens gerada por analisar_expressao().
    Limpa a tabela e insere os novos valores.
    """
    # Remove itens antigos
    for item in tree.get_children():
        tree.delete(item)

    # Insere os novos tokens
        
    for t in tokens:
        # Define a tag se for um token desconhecido
        tags = ('erro',) if t['token'] == "DESCONHECIDO" else ()
        
        tree.insert(
            "", "end", 
            values=(
                t['lexema'], t['token'], t['erro'],
                t['linha'], t['col_ini'], t['col_fim']
            ),
            tags=tags  # Aplica a tag aqui
        )

def popular_tabela_sintatica(tree_sintatica):
    """
    Preenche a tabela sintática (ttk.Treeview) com as regras de produção.
    Inclui prints de depuração detalhados.
    """
    # Garante que a tabela_sintatica esteja disponível
    try:
        # Tenta importar localmente se não for global
        from compiler.syntatic_analyzer import tabela_sintatica
    except ImportError:
        print("ERRO CRÍTICO: Não foi possível encontrar 'tabela_sintatica'. Verifique a importação em executor.py")
        return

    print("\n--- INICIANDO popular_tabela_sintatica ---")
    print(f"Tabela sintática (escopo local) tem {len(tabela_sintatica)} não-terminais")
    # print(f"Não-terminais (escopo local): {sorted(tabela_sintatica.keys())}") # Log opcional

    try:
        # 1. Limpa a tabela na interface antes de preencher
        print("Limpando itens antigos da Treeview...")
        for item in tree_sintatica.get_children():
            tree_sintatica.delete(item)
        print("Itens antigos limpos.")

        # 2. Obtém as colunas (terminais) como definidas na interface
        colunas_interface = tree_sintatica["columns"]
        print(f"Colunas da interface Treeview: {colunas_interface}")
        if not colunas_interface or colunas_interface[0] != 'Não Terminal':
            print("ERRO: Colunas da Treeview não parecem estar configuradas corretamente.")
            return

        # 3. Preenche a tabela linha por linha (para cada não-terminal)
        print("\n--- INÍCIO DO PREENCHIMENTO DAS LINHAS NA INTERFACE ---")
        for nao_terminal in sorted(tabela_sintatica.keys()):  # Itera sobre não-terminais da estrutura de dados
            print(f"\nProcessando Não-Terminal: '{nao_terminal}'")
            linha_valores = [nao_terminal]  # Primeira célula da linha é o nome do não-terminal

            # Itera sobre cada nome de coluna da interface (representando um terminal), exceto a primeira ("Não Terminal")
            for terminal_coluna in colunas_interface[1:]:
                # Busca a produção na estrutura tabela_sintatica para o par (nao_terminal, terminal_coluna)
                # Usamos .get() para evitar KeyError se o não-terminal não tiver entrada para esse terminal_coluna
                producao_valor = tabela_sintatica.get(nao_terminal, {}).get(terminal_coluna, '-') # Retorna '-' se não encontrar

                # --- PRINT DE DEBUG 1 --- Mostra o resultado da busca
                print(f"  DEBUG: Lookup: NonTerminal='{nao_terminal}', TerminalColuna='{terminal_coluna}', Found='{producao_valor}'")

                # Formata o valor encontrado para exibição na célula
                producao_formatada = '-'
                if isinstance(producao_valor, list):
                    producao_str = ' '.join(str(x) for x in producao_valor)
                    producao_formatada = f"{nao_terminal} ⟶ {producao_str}"
                    # Opcional: Quebra de linha para produções longas (pode complicar a visualização)
                    # if len(producao_str) > 40:
                    #     producao_formatada = f"{nao_terminal} ⟶\n{producao_str}"
                elif producao_valor == 'ε':
                    producao_formatada = f"{nao_terminal} ⟶ ε"
                # Se for '-', já está formatado como '-' (caso padrão)

                # Adiciona o valor formatado à lista de valores da linha atual
                linha_valores.append(producao_formatada)

                # --- PRINT DE DEBUG 2 --- Mostra o valor que será inserido na célula
                # print(f"    DEBUG: Appending to row: '{producao_formatada}'") # Log opcional, pode poluir muito

            # 4. Insere a linha completa na interface Treeview
            print(f"-> Inserindo linha para '{nao_terminal}' com {len(linha_valores)} valores.")
            try:
                # Garante que o número de valores corresponde ao número de colunas
                if len(linha_valores) == len(colunas_interface):
                     tree_sintatica.insert("", "end", values=tuple(linha_valores))
                     # print(f"   Linha inserida com sucesso para '{nao_terminal}'!") # Log opcional
                else:
                     # Este erro é crítico e indica um problema na lógica do loop ou nas colunas
                     print(f"   ERRO FATAL: Número de valores ({len(linha_valores)}) não corresponde ao número de colunas ({len(colunas_interface)}) para '{nao_terminal}'. Linha não inserida.")
                     print(f"   Valores da linha: {linha_valores}")

            except Exception as e:
                print(f"   Erro CRÍTICO ao inserir linha para '{nao_terminal}': {str(e)}")
                print(f"   Linha que causou o erro: {linha_valores}")
                # Considerar não levantar a exceção para tentar preencher o resto da tabela

        print("\n--- FIM DO PREENCHIMENTO DAS LINHAS NA INTERFACE ---")

        # 5. Opcional: Ajustar tamanho das colunas (pode ser feito na criação da tabela)
        # print("Ajustando largura das colunas...")
        # for col in colunas_interface:
        #     tree_sintatica.column(col, width=150, anchor='center') # Exemplo de ajuste

        print("\nFunção popular_tabela_sintatica concluída.")
        print(f"Número final de linhas na interface Treeview: {len(tree_sintatica.get_children())}")

    except Exception as e:
        print(f"Erro GERAL e INESPERADO dentro de popular_tabela_sintatica: {str(e)}")
        import traceback
        traceback.print_exc()

# ------------------------------------------------------------------------------
# 3. Função de callback para o menu "Executar"
# ------------------------------------------------------------------------------
def executar_analise(text_area, tree, text_log, options, tree_sintatica):
    """
    Lê o texto da área principal, analisa e exibe o resultado na Tabela de Lexemas.
    Também atualiza o Log de Compilação com mensagens de sucesso ou erro.
    """
    print(f"\nExecutando análise com opção: {options}")
    
    # Obtém o texto da área principal
    expressao = text_area.get("1.0", tk.END).strip()
    print(f"Texto para análise: {expressao[:50]}...")  # Mostra os primeiros 50 caracteres
    
    msg = ''
    tokens = None
    
    try:
        # Sempre executa a análise léxica primeiro para obter os tokens
        tokens = analisar_expressao(expressao)
        print(f"Análise léxica gerou {len(tokens)} tokens")
        
        if options == "executar":
            print("Iniciando análise sintática...")
            # Executa a análise léxica e sintática
            analisar_declaracoes(tokens)
            msg = "Análise sintática concluída com sucesso!"
            # Preenche a tabela sintática apenas na execução da análise sintática
            print("Chamando popular_tabela_sintatica...")
            print(f"Tabela sintática tem {len(tabela_sintatica)} não-terminais")
            print(f"Não-terminais: {sorted(tabela_sintatica.keys())}")
            popular_tabela_sintatica(tree_sintatica)
            print("Retornou da popular_tabela_sintatica")
            
        elif options == "analise_lexica":
            msg = "Análise léxica concluída com sucesso!"
            
        elif options == "analise_semantica":
            analisar_declaracoes(tokens)
            msg = "Análise semântica concluída com sucesso!"
            
    except SyntaxError as e:
        text_log.config(state='normal')
        text_log.delete('1.0', tk.END)
        text_log.insert('1.0', f"Erro de sintaxe: {str(e)}\n")
        text_log.config(foreground='red', state='disabled')
        return
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        text_log.config(state='normal')
        text_log.delete('1.0', tk.END)
        text_log.insert('1.0', f"Erro inesperado: {str(e)}\n")
        text_log.config(foreground='red', state='disabled')
        return
    
    if tokens:  # Só popula a tabela de lexemas se tivermos tokens
        # Limpa a tabela de lexemas antes de inserir novos resultados
        popular_tabela_lexemas(tree, tokens)
        
        # Verifica se há erros nos tokens
        has_errors = any(token['erro'] for token in tokens)
        
        # Limpa o Log de Compilação
        text_log.config(state='normal')  # Habilita a edição
        text_log.delete('1.0', tk.END)   # Limpa o conteúdo
        
        text_log.insert('1.0', get_timestamp() + msg + "\n")  # Exibe a mensagem de análise
        
        # Exibe a mensagem apropriada no Log de Compilação
        if has_errors:
            text_log.insert('2.0', get_timestamp() + "Erro de análise\n")
            text_log.config(foreground='red')  # Define a cor do texto como vermelho
        else:
            text_log.insert('2.0', get_timestamp() + "Analise concluída com sucesso!\n")
            text_log.config(foreground='green')  # Define a cor do texto como verde
        
        text_log.config(state='disabled')  # Desabilita a edição