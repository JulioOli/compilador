import tkinter as tk
import platform

def criar_janela_principal():
    root = tk.Tk()
    root.title("PCIDE - Compilador da FCT")

    # Maximiza a janela de acordo com o sistema operacional
    sistema = platform.system()
    if sistema == "Windows":
        root.state('zoomed')
    else:  # Linux ou macOS
        # Obtém as dimensões da tela
        largura_tela = root.winfo_screenwidth()
        altura_tela = root.winfo_screenheight()
        # Configura o tamanho da janela para ocupar a tela toda
        root.geometry(f"{largura_tela}x{altura_tela}+0+0")
    
    # Configura o grid para expandir
    root.rowconfigure(0, weight=85)   # Área do editor (85% do espaço)
    root.rowconfigure(1, weight=15)  # Área das tabelas (15% do espaço)
    root.columnconfigure(0, weight=1)
    
    return root
