import sys
import re

def ler_arquivo(caminho):
    with open(caminho, 'r') as f:
        linhas = [linha.strip() for linha in f.readlines()]
    quantidade = int(linhas[0])
    expressoes = linhas[1:]
    if quantidade != len(expressoes):
        raise ValueError("Quantidade de expressões não bate com o número informado.")
    return expressoes

TOKEN_REGEX = [
    ('ABREPAREN', r'\('),
    ('FECHAPAREN', r'\)'),
    ('OPUNARIO', r'\\neg'),
    ('OPBINARIO', r'\\wedge|\\vee|\\rightarrow|\\leftrightarrow'),
    ('CONSTANTE', r'true|false'),
    ('PROPOSICAO', r'[0-9][0-9a-z]*'),
    ('ESPACO', r'\s+'),
]

def lexer(expr):
    tokens = []
    i = 0
    while i < len(expr):
        match = None
        for tipo, regex in TOKEN_REGEX:
            pattern = re.compile(regex)
            match = pattern.match(expr, i)
            if match:
                if tipo != 'ESPACO':
                    tokens.append((tipo, match.group()))
                i = match.end()
                break
        if not match:
            raise ValueError(f"Erro léxico na posição {i}: '{expr[i]}'")
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def consumir(self, tipo):
        if self.atual()[0] == tipo:
            self.pos += 1
        else:
            raise ValueError(f"Esperado {tipo}, encontrado {self.atual()}")

    def parse(self):
        self.formula()
        if self.pos != len(self.tokens):
            raise ValueError("Tokens extras após fim da fórmula")

    def formula(self):
        tipo, _ = self.atual()
        if tipo == 'CONSTANTE' or tipo == 'PROPOSICAO':
            self.pos += 1
        elif tipo == 'ABREPAREN':
            self.consumir('ABREPAREN')
            tipo, _ = self.atual()
            if tipo == 'OPUNARIO':
                self.consumir('OPUNARIO')
                self.formula()
                self.consumir('FECHAPAREN')
            elif tipo == 'OPBINARIO':
                self.consumir('OPBINARIO')
                self.formula()
                self.formula()
                self.consumir('FECHAPAREN')
            else:
                raise ValueError("Operador esperado após parêntese de abertura")
        else:
            raise ValueError("Fórmula inválida")

def validar_expressao(expr):
    try:
        tokens = lexer(expr)
        parser = Parser(tokens)
        parser.parse()
        return "valida"
    except Exception as e:
        return f"inválida\n{e}"

def main():
    if len(sys.argv) < 2:
        print("Uso: python validador_logico.py <arquivo.txt>")
        return

    caminho = sys.argv[1]
    expressoes = ler_arquivo(caminho)
    for expr in expressoes:
        print(validar_expressao(expr))

if __name__ == "__main__":
    main()
