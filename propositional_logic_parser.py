# Guilherme Schwarz, Julia Cristina Moreira da Silva

import sys

def ler_arquivo(caminho):
    with open(caminho, 'r') as f:
        linhas = [linha.strip() for linha in f.readlines()]
    quantidade = int(linhas[0])
    expressoes = linhas[1:]
    if quantidade != len(expressoes):
        raise ValueError("Quantidade de expressões não bate com o número informado.")
    return expressoes

class Lexer:
    def __init__(self, expression: str):
        self.expression: str = expression
        self.tokens: list[tuple] = []
        self.char_index: int = 0
        
    def get_tokens(self):
        while self.char_index < len(self.expression):
            char = self.expression[self.char_index]
            rest = self.expression[self.char_index:]

            if char.isspace():
                self.space_state()
            elif char == '(':
                self.abreparen_state()
            elif char == ')':
                self.fechaparen_state()
            elif rest.startswith('\\leftrightarrow'):
                self.opbinario_state('\\leftrightarrow')
            elif rest.startswith('\\rightarrow'):
                self.opbinario_state('\\rightarrow')
            elif rest.startswith('\\wedge'):
                self.opbinario_state('\\wedge')
            elif rest.startswith('\\vee'):
                self.opbinario_state('\\vee')
            elif rest.startswith('\\neg'):
                self.opunario_state('\\neg')
            elif rest.startswith('true'):
                self.constante_state('true')
            elif rest.startswith('false'):
                self.constante_state('false')
            elif char.isdigit():
                self.preposicao_state()
            else:
                raise ValueError(f"Erro léxico na posição {self.char_index}: '{char}'")
        return self.tokens
    
    def space_state(self):
        self.char_index += 1
    
    def abreparen_state(self):
        self.tokens.append(('ABREPAREN', '('))
        self.char_index += 1
        
    def fechaparen_state(self):
        self.tokens.append(('FECHAPAREN', ')'))
        self.char_index += 1
        
    def opbinario_state(self, operator: str):
        self.tokens.append(('OPBINARIO', operator))
        self.char_index += len(operator)
        
    def opunario_state(self, operator: str):
        self.tokens.append(('OPUNARIO', operator))
        self.char_index += len(operator)
    
    def constante_state(self, constante: str):
        self.tokens.append(('CONSTANTE', constante))
        self.char_index += len(constante)
        
    def preposicao_state(self):
        prep_end = self.char_index + 1
        while prep_end < len(self.expression) and self.expression[prep_end].isalnum():
            prep_end += 1
        self.tokens.append(('PROPOSICAO', self.expression[self.char_index:prep_end]))
        self.char_index = prep_end

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
        lexer = Lexer(expr)
        tokens = lexer.get_tokens()
        parser = Parser(tokens)
        parser.parse()
        return "valida"
    except Exception as e:
        return f"inválida\n{e}"

def main():
    if len(sys.argv) < 2:
        print("Uso: python propositional_logic_parser.py <arquivo.txt>")
        return

    caminho = sys.argv[1]
    expressoes = ler_arquivo(caminho)
    for expr in expressoes:
        print(f"Expressão: {expr}")
        print(validar_expressao(expr))

if __name__ == "__main__":
    main()
