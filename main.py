from compiler.syntatic_analyzer import tabela_sintatica

from gui.window import criar_janela_principal
from gui.editor import criar_area_principal
from gui.notebook import criar_bloco_inferior
from gui.menu import criar_menu

print("\nIniciando aplicação...")
print(f"Tabela sintática importada tem {len(tabela_sintatica)} não-terminais")
print(f"Não-terminais: {sorted(tabela_sintatica.keys())}")

def main():
    # Cria a janela principal
    root = criar_janela_principal()
    
    # Cria a área principal (editor)
    text_area = criar_area_principal(root)
    
    # Cria o bloco inferior com as três abas
    print("\nCriando bloco inferior...")
    print(f"Tabela sintática tem {len(tabela_sintatica)} não-terminais")
    print(f"Não-terminais: {sorted(tabela_sintatica.keys())}")
    tree_lexemas, text_log, tree_sintatica = criar_bloco_inferior(root, tabela_sintatica)
    
    # Cria o menu
    criar_menu(root, text_area, tree_lexemas, text_log, tree_sintatica)
    
    # Inicia o loop principal
    root.mainloop()

if __name__ == "__main__":
    main()
