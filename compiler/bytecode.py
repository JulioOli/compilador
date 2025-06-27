# ----------------------------------------------------------------------------
# Simple Stack-Based Bytecode Generator for LALG
# ----------------------------------------------------------------------------

# Converts infix token list to Reverse Polish Notation (RPN) via Shunting Yard
def infix_to_rpn(tokens):
    prec = {
        'OPERADOR_SOMA': 1,
        'OPERADOR_SUBTRACAO': 1,
        'OPERADOR_MULTIPLICACAO': 2,
        'OPERADOR_DIV': 2
    }
    output = []
    stack = []
    for t in tokens:
        tok = t['token']
        if tok in ('NUMERO_INTEIRO', 'IDENTIFICADOR'):
            output.append(t)
        elif tok in ('OPERADOR_SOMA', 'OPERADOR_SUBTRACAO', 'OPERADOR_MULTIPLICACAO', 'OPERADOR_DIV'):
            while stack and stack[-1]['token'] != 'ABRE_PARENTESES' and \
                  prec.get(stack[-1]['token'], 0) >= prec[tok]:
                output.append(stack.pop())
            stack.append(t)
        elif tok == 'ABRE_PARENTESES':
            stack.append(t)
        elif tok == 'FECHA_PARENTESES':
            while stack and stack[-1]['token'] != 'ABRE_PARENTESES':
                output.append(stack.pop())
            stack.pop()  # discard '('
    while stack:
        output.append(stack.pop())
    return output

# Main bytecode generation function
def generate_bytecode(tokens):
    code = []
    i = 0
    n = len(tokens)

    while i < n:
        t = tokens[i]
        # Assignment: IDENTIFICADOR ':=' expr ';'
        if t['token'] == 'IDENTIFICADOR' and i+1 < n and tokens[i+1]['token'] == 'ATRIBUICAO':
            var = t['lexema']
            # find end of expression
            j = i+2
            while j < n and tokens[j]['token'] != 'PONTO_E_VIRGULA':
                j += 1
            expr_tokens = tokens[i+2:j]
            rpn = infix_to_rpn(expr_tokens)
            # emit bytecode for RPN
            for x in rpn:
                if x['token'] == 'NUMERO_INTEIRO':
                    code.append(f"ICONST {x['lexema']}")
                elif x['token'] == 'IDENTIFICADOR':
                    code.append(f"LOAD {x['lexema']}")
                elif x['token'] == 'OPERADOR_SOMA':
                    code.append("IADD")
                elif x['token'] == 'OPERADOR_SUBTRACAO':
                    code.append("ISUB")
                elif x['token'] == 'OPERADOR_MULTIPLICACAO':
                    code.append("IMUL")
                elif x['token'] == 'OPERADOR_DIV':
                    code.append("IDIV")
            code.append(f"STORE {var}")
            i = j + 1
            continue

        # Read: 'READ' '(' IDENT ')' ';'
        if t['token'] == 'PALAVRA_RESERVADA_READ':
            var = tokens[i+2]['lexema']
            code.append(f"READ {var}")
            i += 4
            continue

        # Write: 'WRITE' '(' IDENT ')' ';'
        if t['token'] == 'PALAVRA_RESERVADA_WRITE':
            var = tokens[i+2]['lexema']
            code.append(f"WRITE {var}")
            i += 4
            continue

        # TODO: support IF, WHILE, PROC CALL in future
        i += 1

    code.append("HALT")
    return code