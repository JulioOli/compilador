from tkinter import ttk
import tkinter as tk

# ------------------------------------------------------------------------------
# 6. Criação da área principal de texto
# ------------------------------------------------------------------------------
def criar_area_principal(root):
    """Cria a área principal (como um editor de texto) e a posiciona na janela."""
    # Frame para conter o contador e o texto
    frame_texto = ttk.Frame(root)
    frame_texto.grid(row=0, column=0, sticky="nsew")
    frame_texto.grid_rowconfigure(0, weight=1)  # Aumenta o peso da área de texto
    frame_texto.grid_columnconfigure(1, weight=1)  # Aumenta o peso da coluna do texto
    
    # Widget do contador de linhas (Text com fundo cinza)
    text_line_numbers = tk.Text(
        frame_texto,
        width=4,
        bg="#f0f0f0",
        bd=0,
        highlightthickness=0,
        state='disabled',
        takefocus=0
    )
    text_line_numbers.grid(row=0, column=0, sticky="ns")
    
    # Área principal de texto com scrollbar horizontal
    text_area = tk.Text(frame_texto, wrap="none", height=35)  # Aumentando para 35 linhas
    text_area.grid(row=0, column=1, sticky="nsew")
    
    # Configura a tag para destacar linhas com erro
    text_area.tag_configure('erro_linha', background='#FFCDD2')
    
    # Scrollbars vertical e horizontal
    vsb = ttk.Scrollbar(frame_texto, orient="vertical")
    hsb = ttk.Scrollbar(frame_texto, orient="horizontal")
    
    # Configura os scrollbars
    vsb.config(command=text_area.yview)
    hsb.config(command=text_area.xview)
    text_area.config(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    # Posiciona os scrollbars
    vsb.grid(row=0, column=2, sticky="ns")
    hsb.grid(row=1, column=1, sticky="ew")
    
    # Função para atualizar os números de linha
    def update_line_numbers(event=None):
        text_line_numbers.config(state='normal')
        text_line_numbers.delete('1.0', tk.END)
        
        # Obtém o número total de linhas no texto
        total_lines = int(float(text_area.index("end-1c")))
        
        # Obtém a primeira linha visível
        first_visible = text_area.index("@0,0")
        first_line = int(float(first_visible))
        
        # Obtém a última linha visível
        last_visible = text_area.index(f"@0,{text_area.winfo_height()}")
        last_line = int(float(last_visible)) + 1
        
        # Gera números apenas para as linhas visíveis
        line_numbers = '\n'.join(str(i).rjust(3) for i in range(first_line, last_line))
        
        text_line_numbers.insert('1.0', line_numbers)
        text_line_numbers.config(state='disabled')
        
        # Sincroniza a posição de rolagem
        text_line_numbers.yview_moveto(text_area.yview()[0])
    
    # Sincroniza a rolagem vertical
    def on_vertical_scroll(*args):
        text_area.yview(*args)
        text_line_numbers.yview(*args)
        update_line_numbers()
    
    # Configura o scrollbar vertical para usar a nova função
    vsb.config(command=on_vertical_scroll)
    
    # Vincula eventos que modificam o texto ou a visualização
    text_area.bind('<<Modified>>', update_line_numbers)
    text_area.bind('<Configure>', update_line_numbers)
    text_area.bind('<Key>', lambda e: root.after(1, update_line_numbers))
    
    # Suporte a rolagem do mouse
    def on_mousewheel(event):
        if event.state == 0:  # Sem modificadores (rolagem vertical)
            text_area.yview_scroll(int(-1 * (event.delta/120)), "units")
            update_line_numbers()
        elif event.state == 1:  # Shift pressionado (rolagem horizontal)
            text_area.xview_scroll(int(-1 * (event.delta/120)), "units")
        return "break"
    
    # Vincula eventos de rolagem do mouse
    text_area.bind('<MouseWheel>', on_mousewheel)  # Windows
    text_area.bind('<Button-4>', lambda e: [text_area.yview_scroll(-1, "units"), update_line_numbers()])  # Linux scroll up
    text_area.bind('<Button-5>', lambda e: [text_area.yview_scroll(1, "units"), update_line_numbers()])   # Linux scroll down
    text_area.bind('<Shift-Button-4>', lambda e: text_area.xview_scroll(-1, "units"))  # Linux horizontal scroll
    text_area.bind('<Shift-Button-5>', lambda e: text_area.xview_scroll(1, "units"))   # Linux horizontal scroll
    
    # Atualiza inicialmente
    update_line_numbers()
    
    return text_area