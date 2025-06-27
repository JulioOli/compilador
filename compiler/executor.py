from compiler.lexer import analisar_expressao
from compiler.syntatic_analyzer import analisar_declaracoes
from compiler.semantic_analyzer import build_symbol_table, check_semantics
from compiler.bytecode import generate_bytecode
from compiler.syntatic import tabela_sintatica
from lark import Lark, UnexpectedInput
from datetime import datetime
import tkinter as tk

# Função de timestamp
def get_timestamp():
    """Retorna um timestamp formatado para o log."""
    return datetime.now().strftime("[%H:%M:%S] ")

# Função para popular a tabela de lexemas
def popular_tabela_lexemas(tree, tokens):
    for item in tree.get_children():
        tree.delete(item)
    
    for t in tokens:
        tags = ('erro',) if t['token'] == "DESCONHECIDO" else ()
        tree.insert("", "end", 
                    values=(t['lexema'], t['token'], t['erro'], t['linha'], t['col_ini'], t['col_fim']),
                    tags=tags)

# Função para popular a tabela sintática
def popular_tabela_sintatica(tree_sintatica):    
    try:
        for item in tree_sintatica.get_children():
            tree_sintatica.delete(item)

        colunas_interface = tree_sintatica["columns"]
        
        for nao_terminal in sorted(tabela_sintatica.keys()):
            linha_valores = [nao_terminal]
            for terminal_coluna in colunas_interface[1:]:
                producao_valor = tabela_sintatica.get(nao_terminal, {}).get(terminal_coluna, '-')
                if isinstance(producao_valor, list):
                    producao_formatada = f"{nao_terminal} ⟶ {' '.join(str(x) for x in producao_valor)}"
                elif producao_valor == 'ε':
                    producao_formatada = f"{nao_terminal} ⟶ ε"
                else:
                    producao_formatada = '-'
                linha_valores.append(producao_formatada)

            tree_sintatica.insert("", "end", values=tuple(linha_valores))

    except Exception as e:
        print(f"Erro GERAL e INESPERADO dentro de popular_tabela_sintatica: {str(e)}")
        import traceback
        traceback.print_exc()

# Função de callback para o menu "Executar"
def executar_analise(text_area, tree, text_log, options, tree_sintatica):
    """
    Lê o texto da área principal, analisa e exibe o resultado na Tabela de Lexemas.
    Também atualiza o Log de Compilação com mensagens de sucesso ou erro.
    Inclui checagem semântica de identificadores e procedures.
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
            print("Iniciando análise completa (sintática + semântica + bytecode)...")
            
            # Análise sintática LL(1)
            analisar_declaracoes(tokens)
            
            # Construção da tabela de símbolos e checagem semântica
            symtab = build_symbol_table(tokens)
            semantic_errors = check_semantics(tokens, symtab)
            if semantic_errors:
                raise SyntaxError("\n".join(semantic_errors))
            
            # Geração de bytecode
            bytecode = generate_bytecode(tokens)
            
            # Exibe bytecode no log
            text_log.config(state='normal')
            text_log.delete('1.0', tk.END)
            text_log.insert('1.0', "Bytecode gerado:\n" + "\n".join(bytecode))
            text_log.config(foreground='black', state='disabled')
            
            # Salva resultado
            salvar_resultado(bytecode)
            
            # Atualiza tabela sintática
            popular_tabela_sintatica(tree_sintatica)
            
            msg = "Análise completa concluída com sucesso!"
            
        elif options == "analise_lexica":
            msg = "Análise léxica concluída com sucesso!"
            
        elif options == "analise_semantica":
            # Análise sintática LL(1)
            analisar_declaracoes(tokens)
            
            # Construção da tabela de símbolos e checagem semântica
            symtab = build_symbol_table(tokens)
            semantic_errors = check_semantics(tokens, symtab)
            if semantic_errors:
                raise SyntaxError("\n".join(semantic_errors))
            
            msg = "Análise semântica concluída com sucesso!"
            
    except SyntaxError as e:
        # Exibe erros sintáticos ou semânticos
        text_log.config(state='normal')
        text_log.delete('1.0', tk.END)
        text_log.insert('1.0', f"Erro de sintaxe: {str(e)}\n")
        text_log.config(foreground='red', state='disabled')
        # Atualiza tabela de lexemas mesmo em erro
        if tokens:
            popular_tabela_lexemas(tree, tokens)
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
        
        if has_errors:
            text_log.insert('2.0', get_timestamp() + "Erro de análise\n")
            text_log.config(foreground='red')  # Define a cor do texto como vermelho
        else:
            text_log.insert('2.0', get_timestamp() + "Análise concluída com sucesso!\n")
            text_log.config(foreground='green')  # Define a cor do texto como verde
        
        text_log.config(state='disabled')  # Desabilita a edição

def salvar_resultado(bytecode):
    """Salva o bytecode no arquivo 'resultado.by' na raiz do projeto."""
    with open('resultado.by', 'w', encoding='utf-8') as f:
        for ins in bytecode:
            f.write(ins + '\n')
