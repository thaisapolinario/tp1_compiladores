from scanner import Scanner

def main():
    try:
        with open("entrada.txt", "r") as f:
            conteudo = f.read()
    except FileNotFoundError:
        print("Arquivo nao encontrado.")
        return

    lex = Scanner(conteudo)
    
    print("-" * 67)
    print(f"| {'Cod':<5} | {'Token':<15} | {'Classe':<20} | {'Linha':<6} | {'Col':<6} |")
    print("-" * 67)

    while not lex.eof():
        token = lex.proximo_token()
        if token:
            print(token)

if __name__ == "__main__":
    main()