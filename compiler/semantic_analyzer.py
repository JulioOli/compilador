# ----------------------------------------------------------------------------
# Utils para análise semântica: construção e checagem de tabela de símbolos
# ----------------------------------------------------------------------------

def build_symbol_table(tokens):
    """
    Retorna um dict: nome → info ({ 'kind': 'var'|'proc'|'prog', 'type': <tipo opcional>, 'line': <linha> })
    """
    table = {}
    i = 0
    n = len(tokens)

    while i < n:
        t = tokens[i]

        # programa <IDENTIFICADOR>
        if t['token'] == 'PALAVRA_RESERVADA_PROGRAM' and i+1 < n and tokens[i+1]['token']=='IDENTIFICADOR':
            prog_name = tokens[i+1]['lexema']
            table[prog_name] = {'kind':'prog','line':tokens[i+1]['linha']}
            i += 2
            continue

        # declarações de variáveis: int/boolean
        if t['token'] in ('PALAVRA_RESERVADA_INT','PALAVRA_RESERVADA_BOOLEAN'):
            tipo = 'int' if t['token'].endswith('INT') else 'boolean'
            j = i+1
            while j < n and tokens[j]['token']=='IDENTIFICADOR':
                name = tokens[j]['lexema']
                table[name] = {'kind':'var','type':tipo,'line':tokens[j]['linha']}
                j += 1
                if j<n and tokens[j]['token']=='VIRGULA':
                    j += 1
                else:
                    break
            i = j
            continue

        # parâmetros formais: var x,y : tipo
        if t['token']=='PALAVRA_RESERVADA_VAR':
            j = i+1
            while j<n and tokens[j]['token']=='IDENTIFICADOR':
                name = tokens[j]['lexema']
                table[name] = {'kind':'param','line':tokens[j]['linha']}
                j += 1
                if j<n and tokens[j]['token']=='VIRGULA':
                    j += 1
                else:
                    break
            i = j
            continue

        # procedure <IDENTIFICADOR>
        if t['token']=='PALAVRA_RESERVADA_PROCEDURE' and i+1<n and tokens[i+1]['token']=='IDENTIFICADOR':
            name = tokens[i+1]['lexema']
            table[name] = {'kind':'proc','line':tokens[i+1]['linha']}
            i += 2
            continue

        i += 1

    return table


def check_semantics(tokens, symtab):
    """
    Retorna lista de mensagens de erro semântico:
     - identificadores não declarados,
     - chamadas de procedures não declaradas,
     - procedures declaradas mas não usadas.
    """
    erros = []
    used_procs = set()

    # 1) Coleta chamadas de proc e verifica usos de identificadores
    for idx, t in enumerate(tokens):
        if t['token']=='IDENTIFICADOR':
            name = t['lexema']
            nxt = tokens[idx+1]['token'] if idx+1<len(tokens) else None
            # chamada de procedure detectada: IDENT '(' mas não declaração
            if nxt=='ABRE_PARENTESES' and not (idx>0 and tokens[idx-1]['token']=='PALAVRA_RESERVADA_PROCEDURE'):
                used_procs.add(name)
                info = symtab.get(name)
                if info is None or info.get('kind')!='proc':
                    erros.append(f"Erro semântico: chamada não declarada de procedure '{name}' na linha {t['linha']}." )
            else:
                # uso normal de var/prog/param
                if name not in symtab:
                    erros.append(f"Erro semântico: '{name}' não declarado na linha {t['linha']}." )

    # 2) Verifica procedures declaradas mas não usadas
    for name, info in symtab.items():
        if info.get('kind')=='proc' and name not in used_procs:
            erros.append(
                f"Erro semântico: procedure declarada mas não usada '{name}' na linha {info.get('line')}.")

    return erros
