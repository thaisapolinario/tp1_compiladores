import re  # importa o regex

#PERCORRE A ENTRADA CARACTERE POR CARACTERE E TENTA ACHAR UM CASAMENTO COM AS REGRAS DEFINIDAS

from tokens import DEFINICAO_CONJUNTOS, Token

class Scanner:
    def __init__(self, entrada):
        self.entrada = entrada # conteudo do codigo fonte
        self.pos = 0  # começa na posicao 0, indica o caractere atual
        self.linha = 0 # contador linha
        self.coluna = 0 # contador coluna
        self.contador_cod = 0 # identificador de cada token

    def eof(self):
        return self.pos >= len(self.entrada) # verifica se chegou no final da entrada, se o ponteiro esta fora da entrada

    def proximo_token(self):
        while not self.eof():
            char_atual = self.entrada[self.pos]
            if char_atual.isspace(): 
                if char_atual == '\n':
                    self.linha += 1  # pula a linha se ler uma quebra de linha 
                    self.coluna = 1
                else:
                    self.coluna += 1 # se nao for enter, so anda a coluna
                self.pos += 1
                continue

            posicao_inicial = self.pos
            coluna_inicial = self.coluna
            
            #tabela de definicoes definidas em tokens.py
            for nome, regex in DEFINICAO_CONJUNTOS:
                padrao = re.compile(regex)
                casamento = padrao.match(self.entrada, self.pos) #procura o padrao na posicao
                
                if casamento:
                    lexema = casamento.group() # se encontrar um padrao, retorna o texto encontrado
                    
                    # Se for comentario
                    if nome.startswith('COMENTARIO'): 
                        quebras_linha = lexema.count('\n')
                        if quebras_linha > 0:
                            self.linha += quebras_linha # se for mais de uma linha de comentario
                            self.coluna = len(lexema.split('\n')[-1]) + 1
                        else:
                            self.coluna += len(lexema)
                        self.pos += len(lexema)
                        return self.proximo_token() # Busca o próximo token real

                    # Atualiza posição para tokens normais
                    self.pos += len(lexema)
                    self.coluna += len(lexema)
                    
                    # Incrementa o cod do token
                    self.contador_cod += 1  # gera o codigo do token
                    return Token(self.contador_cod, lexema, nome, self.linha, coluna_inicial)

            # ERRO LÉXICO
            char_erro = self.entrada[self.pos]
            while not self.eof() and self.entrada[self.pos] not in [';', '\n']:
                self.pos += 1
                self.coluna += 1
            return Token("ERRO", char_erro, "ERRO_LEXICO", self.linha, coluna_inicial)

        return None