import re

class Token:
    def __init__(self, id, lexema, classe, linha, coluna):
        self.id =id
        self.lexema = lexema
        self.classe = classe
        self.linha = linha
        self.coluna = coluna
    
    def printaToken(self):
        print(f'| {self.id:<4} | {self.lexema:<15} | {self.classe:<18} | {self.linha:<6} | {self.coluna:<6} |')

def analisador(codigo_fonte):
    delimitadores = [' ', '\t', '\n', ';', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<', '>', '!', '&', '|']
    lista_tokens = []
    comeco_linha = 0
    linha_atual = 1
    coluna = 1
    id = 0
    tamanho_codigo = len(codigo_fonte)
    
    pivo = 0
    batedor = 0
    
    lista_padroes = [('COMENTARIO', r'/\*[\s\S]*?\*/|//.*'),
                     ('PALAVRA_RESERVADA', r'\b(int|for|if|bool|string|float)\b'), 
                     ('SEPARADOR', r'\(|\)|\{|\}|;'), 
                     ('OPERADOR', r'\+\+|--|/|\*|\+|-|<=|>=|==|!=|<|>|=|&&|\|\|'),
                     ('NUMERO', r'[0-9]+(\.[0-9]+)?'),
                     ('IDENTIFICADOR', r'[a-zA-Z]([a-zA-Z]|[0-9]|_)*'),
                     ('LITERAL', r'"(?:[^"\\]|\\.)*"'),
                     ('ESPACO', r'[ \t]+'),
                     ('QUEBRA_LINHA', r'\n'),]
    
    regex = '|'.join(f'(?P<{nome}>{padrao})'for nome, padrao in lista_padroes)
    regex = re.compile(regex)
    
    while pivo < tamanho_codigo:
        coluna = pivo - comeco_linha + 1
        sequencia_invalida = ""
        
        match = regex.match(codigo_fonte, pos=pivo)
    
        if match:
            lexema = match.group()
            classe = match.lastgroup
            batedor = match.end()
            pivo = batedor
            
            if classe == 'ESPACO':
                continue
            elif classe == 'QUEBRA_LINHA':
                linha_atual += 1
                comeco_linha = pivo
            elif classe == 'COMENTARIO':
                linha_atual += lexema.count('\n')
                aux = lexema.rfind('\n')
                if aux != -1:
                    comeco_linha = (pivo - len(lexema) + aux + 1)
            elif classe == 'OPERADOR':
                if batedor < tamanho_codigo and lexema == '/' and codigo_fonte[batedor] == '*':
                    print(f'Erro: Comentário não fechado na linha {linha_atual} e coluna {coluna}!')
                    pivo += 1
                else:
                    novo_token = Token(id, lexema, classe, linha_atual, coluna)
                    lista_tokens.append(novo_token)
                    id += 1
                    
            elif classe == 'NUMERO':
                if batedor < tamanho_codigo and codigo_fonte[batedor].isalpha():
                    sequencia_invalida += lexema
                    while pivo < tamanho_codigo and codigo_fonte[pivo] not in delimitadores:
                        sequencia_invalida += codigo_fonte[pivo]
                        pivo += 1
                    print(f'Erro: sequência {sequencia_invalida} inválida na linha {linha_atual} e coluna {coluna}!')
                else:
                    novo_token = Token(id, lexema, classe, linha_atual, coluna)
                    lista_tokens.append(novo_token)
                    id += 1
            else:
                novo_token = Token(id, lexema, classe, linha_atual, coluna)
                lista_tokens.append(novo_token)
                id += 1
        else:
            if codigo_fonte[pivo] == '"':
                print(f"Erro: String não fechada na linha {linha_atual} e coluna {coluna}!")
                pivo += 1
            else:
                while pivo < tamanho_codigo and codigo_fonte[pivo] not in delimitadores:
                    sequencia_invalida += codigo_fonte[pivo]
                    pivo += 1
                print(f'Erro: Caractere ou sequência {sequencia_invalida} inválida na linha {linha_atual} e coluna {coluna}!')
                    
    
    print("\n" + "-"*70)
    print(f"| {'ID':<4} | {'LEXEMA':<15} | {'CLASSE':<18} | {'LINHA':<6} | {'COLUNA':<6} |")
    print("-"*70)
    
    for t in lista_tokens:
        t.printaToken()
        
    return lista_tokens