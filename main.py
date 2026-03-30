from scanner import Scanner

def main():
    try:
        with open("entrada.txt", "r") as f:
            conteudo = f.read()
    except FileNotFoundError:
        print("Arquivo nao encontrado.")
        return

    lex = Scanner(conteudo)

    print("-" * 100)
    print(f"{'Cod':<15} | {'Token':<15} | {'Classe':<15} | {'Linha':<15} | {'Coluna':<15}")
    print("-" * 100)
    
    while not lex.eof():
        token = lex.proximo_token()
        if token:
            print(token)

if __name__ == "__main__":
    main()