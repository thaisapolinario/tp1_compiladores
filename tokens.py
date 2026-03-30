

#CONTEM A TABELA DE SIMBOLOS QUE DEFINEM O SIGNIFICADO DE CADA UM

import re


DEFINICAO_CONJUNTOS = [
    ('COMENTARIO_BLOCO', r'/\*[\s\S]*?\*/'),   
    ('COMENTARIO_LINHA', r'//.*'),             
    ('RESERVADA',    r'\b(if|for|int|bool|string|float)\b'),
    ('OPERADOR_LOGICO',       r'(&&|\|\|)'), 
    ('OPERADOR_COMP',  r'(==|!=|<=|>=|<|>)'),
    ('OPERADOR_ARIT',        r'(\+|\-|\*|/)'),
    ('ATRIBUICAO',        r'='),
    ('IDENTIFICADORES',           r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUMEROS',r'\d+\.\d+|\d+'),
    ('SEPARADORES',          r'[\(\)\{\};,]'),
]

class Token:
    def __init__(self, cod, lexema, classe, linha, coluna):
        self.cod = cod  # codigo do token
        self.lexema = lexema # texto completo encontrado
        self.classe = classe # categoria
        self.linha = linha  # ele foi encontrado
        self.coluna = coluna # onde foi encontrado

    def __repr__(self):
        return f"| {self.cod:<15} | {self.lexema:<15} | {self.classe:<15} | {self.linha:<15} | {self.coluna:<15} |"