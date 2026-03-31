import re
from tokens import DEFINICAO_CONJUNTOS, Token

class Scanner:
    def __init__(self, entrada):
        self.entrada = entrada
        self.pos = 0        # pivo 
        self.linha = 1      # contador linha
        self.coluna = 1        # contador coluna
        self.contador_cod = 0  # identificador de cada token

    def eof(self):
        return self.pos >= len(self.entrada)  # verifica se chegou no final da entrada, se o ponteiro esta fora da entrada

    # verificar o proximo caractere sem mover o pivo
    def batedor(self):
        if self.pos + 1 < len(self.entrada):
            return self.entrada[self.pos + 1]
        return None

    def proximo_token(self):
        while not self.eof():
            char_atual = self.entrada[self.pos]

            # Ignora espaços
            if char_atual.isspace():
                if char_atual == '\n':
                    self.linha += 1
                    self.coluna = 1
                else:
                    self.coluna += 1
                self.pos += 1
                continue

            # deferenciar 
            proximo = self.batedor()
            
            # + do ++
            if char_atual == '+' and proximo == '+':
                lexema = "++"
                t = Token(self.cod_token(), lexema, "OPERADOR_ARIT", self.linha, self.coluna)
                self.move_pivo(2)
                return t
            
            # - do --
            if char_atual == '-' and proximo == '-':
                lexema = "--"
                t = Token(self.cod_token(), lexema, "OPERADOR_ARIT", self.linha, self.coluna)
                self.move_pivo(2)
                return t

            if char_atual == '>' and proximo == '=':
                t = Token(self.cod_token(), ">=", "OPERADOR_LOGICO", self.linha, self.coluna)
                self.move_pivo(2)   
                return t

            if char_atual == '<' and proximo == '=':
                t = Token(self.cod_token(), "<=", "OPERADOR_LOGICO", self.linha, self.coluna)
                self.move_pivo(2)   
                return t

            if char_atual == '=' and proximo == '=':
                t = Token(self.cod_token(), "==", "OPERADOR_LOGICO", self.linha, self.coluna)
                self.move_pivo(2)   
                return t

            if char_atual == '!' and proximo == '=':
                t = Token(self.cod_token(), "!=", "OPERADOR_LOGICO", self.linha, self.coluna)
                self.move_pivo(2)   
                return t

            # REGEX PARA OS DEMAIS TOKENS
            coluna_inicial = self.coluna
            for nome, regex in DEFINICAO_CONJUNTOS:
                padrao = re.compile(regex)
                casamento = padrao.match(self.entrada, self.pos)

                if casamento:
                    lexema = casamento.group()
                    
                    # Se for comentário, pula e chama proximo_token de novo (Recursão)
                    if nome.startswith('COMENTARIO'):
                        self.atualizar_posicao_comentario(lexema, nome)
                        return self.proximo_token()


                    t = Token(self.cod_token(), lexema, nome, self.linha, coluna_inicial)
                    self.move_pivo(len(lexema))
                    return t

            # ERRO LÉXICO
            t_erro = Token("ERRO", char_atual, "ERRO_LEXICO", self.linha, self.coluna)
            self.move_pivo(1)
            return t_erro

        return None

    # move o pivo apos reconhecer um token e atualiza a coluna
    def move_pivo(self, n):
        self.pos += n
        self.coluna += n
    # a cada token reconhecido, aumenta o contador de tokens para gerar um id unico
    def cod_token(self):
        self.contador_cod += 1
        return self.contador_cod

    def atualizar_posicao_comentario(self, lexema, tipo):
        quebras = lexema.count('\n')
        if quebras > 0:
            self.linha += quebras
            self.coluna = len(lexema.split('\n')[-1]) + 1
        else:
            self.coluna += len(lexema)
        self.pos += len(lexema)