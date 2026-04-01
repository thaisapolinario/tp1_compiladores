

#CONTEM A TABELA DE SIMBOLOS QUE DEFINEM O SIGNIFICADO DE CADA UM

import re


DEFINICAO_CONJUNTOS = [
    ('COMENTARIO_BLOCO', r'/\*[\s\S]*?\*/'),
    ('COMENTARIO_LINHA', r'//.*'),
    ('ID_INVALIDO', r'\d+[a-zA-Z_][a-zA-Z0-9_]*'),
    ('RESERVADA', r'\b(if|else|for|while|int|bool|string|float|return)\b'),
    ('IDENTIFICADORES', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('NUMEROS', r'\d+\.\d+|\d+'),
    ('SEPARADORES', r'[\(\)\{\}\[\];,]'),
    ('OPERADOR', r'[\*/]'),
]
class Token:
    def __init__(self, cod, lexema, classe, linha, coluna):
        self.cod = cod  # codigo do token
        self.lexema = lexema # texto completo encontrado
        self.classe = classe # categoria
        self.linha = linha  # ele foi encontrado
        self.coluna = coluna # onde foi encontrado

    def __repr__(self):
        return f"| {self.cod:<5} | {self.lexema:<15} | {self.classe:<15} | {self.linha:<15} | {self.coluna:<15} |"