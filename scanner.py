import re
from tokens import DEFINICAO_CONJUNTOS, Token
class Scanner:
    def __init__(self, entrada):
        self.entrada = entrada
        self.pos = 0        # pivo 
        self.linha = 0      # contador linha
        self.coluna = 0        # contador coluna
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
                    self.coluna = 0
                else:
                    self.coluna += 1
                self.pos += 1
                continue

            # deferenciar 
            proximo = self.batedor()
            coluna_inicial = self.coluna

            if char_atual == '/' and proximo == '*':
                if self.entrada.find('*/', self.pos + 2) == -1:
                    self.pos = len(self.entrada) # Encerra o processamento
                    return Token("ERRO", "/*", "ERRO_LEXICO", self.linha, coluna_inicial)

            # + do ++
            if char_atual == '+':
                if proximo == '+':
                    lexema = "++"
                    self.pos += 2
                    self.coluna += 2          
                    return Token(self.cod_token(), "++", "OPERADOR", self.linha, coluna_inicial)
            
                else:
                    self.pos += 1
                    self.coluna += 1
                    return Token(self.cod_token(), "+", "OPERADOR", self.linha, coluna_inicial)
            
            # - do --
            if char_atual == '-' and proximo == '-':
                lexema = "--"
                self.pos += 2
                self.coluna += 2          
                return Token(self.cod_token(), lexema, "OPERADOR", self.linha, coluna_inicial)

            if char_atual == '>':
                if proximo == '=':
                    self.pos += 2; self.coluna += 2
                    return Token(self.cod_token(), ">=", "OPERADOR", self.linha, coluna_inicial)
                self.pos += 1; self.coluna += 1
                return Token(self.cod_token(), ">", "OPERADOR", self.linha, coluna_inicial)

            if char_atual == '<':
                if proximo == '=':
                    self.pos += 2; self.coluna += 2
                    return Token(self.cod_token(), "<=", "OPERADOR", self.linha, coluna_inicial)
                self.pos += 1; self.coluna += 1
                return Token(self.cod_token(), "<", "OPERADOR", self.linha, coluna_inicial)
                        

            if char_atual == '=':
                if proximo == '=':
                    self.pos += 2
                    self.coluna += 2
                    return Token(self.cod_token(), "==", "OPERADOR", self.linha, coluna_inicial)
                else:
                    self.pos += 1
                    self.coluna += 1
                    return Token(self.cod_token(), "=", "ATRIBUICAO", self.linha, coluna_inicial)
                

            if char_atual == '&' and proximo == '&':
                self.pos += 2
                self.coluna += 2
                return Token(self.cod_token(), "&&", "OPERADOR", self.linha, coluna_inicial) 
            
            
            if char_atual == '|' and proximo == '|':
                self.pos += 2; self.coluna += 2
                return Token(self.cod_token(), "||", "OPERADOR", self.linha, coluna_inicial)


            if char_atual == '!':
                if proximo == '=':
                    self.pos += 2; self.coluna += 2
                    return Token(self.cod_token(), "!=", "OPERADOR", self.linha, coluna_inicial)
                self.pos += 1; self.coluna += 1
                return Token(self.cod_token(), "!", "OPERADOR", self.linha, coluna_inicial)

            # REGEX PARA OS DEMAIS TOKENS

            for nome, regex in DEFINICAO_CONJUNTOS:
                padrao = re.compile(regex)
                casamento = padrao.match(self.entrada, self.pos)
               
                if casamento:
                    lexema = casamento.group()
                
                # Se for comentário, pula e chama proximo_token de novo 
                    if nome == "ID_INVALIDO":
                        t = Token("ERRO", lexema, "ERRO_LEXICO", self.linha, coluna_inicial)
                        self.pos += len(lexema)
                        self.coluna += len(lexema)
                        return t

                    if nome.startswith('COMENTARIO'):
                        self.pos += len(lexema)

                        if '\n' in lexema:
                            self.linha += lexema.count('\n')
                            self.coluna = len(lexema.split('\n')[-1]) 
                        else:
                            self.coluna += len(lexema)

                        return self.proximo_token()

                    t = Token(self.cod_token(), lexema, nome, self.linha, coluna_inicial)

                    self.pos += len(lexema)

                    if '\n' in lexema:
                        self.linha += lexema.count('\n')
                        self.coluna = len(lexema.split('\n')[-1]) + 1
                    else:
                        self.coluna += len(lexema)

                    return t

            # ERRO LÉXICO
            t_erro = Token("ERRO", char_atual, "ERRO_LEXICO", self.linha, self.coluna)
            self.pos += 1
            self.coluna += 1
            return t_erro

        return None
    # a cada token reconhecido, aumenta o contador de tokens para gerar um id unico
    def cod_token(self):
        cod = self.contador_cod
        self.contador_cod += 1
        return cod

