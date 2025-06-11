import tkinter as tk

# ------------------------------------------------------------------------------
# Função auxiliar para limpar tags de erro
# ------------------------------------------------------------------------------
def limpar_tags_erro(text_area):
    """Remove todas as tags de erro do editor de texto."""
    for tag in text_area.tag_names():
        if tag == 'erro_linha':
            text_area.tag_remove(tag, "1.0", tk.END) 