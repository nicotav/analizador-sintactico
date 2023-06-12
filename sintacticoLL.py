class LLParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first_sets = {}
        self.follow_sets = {}
        self.table = {}

    def compute_first_sets(self):
        for nonterminal in self.grammar.nonterminals:
            self.first_sets[nonterminal] = self.first(nonterminal)

    def first(self, symbol):
        if symbol in self.first_sets:
            return self.first_sets[symbol]

        first_set = set()

        if symbol in self.grammar.terminals:
            first_set.add(symbol)
        else:
            for production in self.grammar.productions[symbol]:
                if production[0] == symbol:
                    continue
                for term in production:
                    first_set |= self.first(term)
                    if term not in self.grammar.nullable:
                        break

        self.first_sets[symbol] = first_set
        return first_set

    def compute_follow_sets(self):
        for nonterminal in self.grammar.nonterminals:
            self.follow_sets[nonterminal] = set()

        self.follow_sets[self.grammar.start].add("$")

        while True:
            updated = False

            for nonterminal in self.grammar.nonterminals:
                for production in self.grammar.productions[nonterminal]:
                    for i, symbol in enumerate(production):
                        if symbol in self.grammar.nonterminals:
                            next_symbol = (
                                production[i + 1] if i + 1 < len(production) else None
                            )
                            follow_set = self.follow_sets[symbol]

                            if (
                                next_symbol is None
                                or next_symbol in self.grammar.terminals
                            ):
                                follow_set |= self.follow_sets[nonterminal]
                            else:
                                first_set = self.first(next_symbol)
                                follow_set |= first_set - {"epsilon"}

                                if "epsilon" in first_set or next_symbol == symbol:
                                    follow_set |= self.follow_sets[nonterminal]

                            if follow_set != self.follow_sets[symbol]:
                                updated = True
                                self.follow_sets[symbol] = follow_set

            if not updated:
                break

    def build_parse_table(self):
        for nonterminal in self.grammar.nonterminals:
            self.table[nonterminal] = {}

            for terminal in self.grammar.terminals:
                self.table[nonterminal][terminal] = None

            self.table[nonterminal]["$"] = None

        for production in self.grammar.productions:
            nonterminal = production[0]
            first_set = self.first(production[1])

            for terminal in first_set:
                self.table[nonterminal][terminal] = production

            if "epsilon" in first_set:
                follow_set = self.follow_sets[nonterminal]

                for terminal in follow_set:
                    self.table[nonterminal][terminal] = production

    def parse(self, input_string):
        stack = ["$"]
        input_string += "$"
        current_symbol = input_string[0]

        while True:
            top = stack[-1]

            if top == current_symbol:
                stack.pop()
                input_string = input_string[1:]
                current_symbol = input_string[0]
            else:
                if top in self.grammar.nonterminals:
                    production = self.table[top][current_symbol]

                    if production is None:
                        raise ValueError("Error: Invalid input")

                    stack.pop()

                    if production != ["epsilon"]:
                        stack += reversed(production)
                else:
                    raise ValueError("Error: Invalid input")

            if top == "$" and current_symbol == "$":
                print("Accepted")
                break


class Grammar:
    def __init__(self):
        self.nonterminals = set()
        self.terminals = set()
        self.productions = {}
        self.start = None
        self.nullable = set()

    def add_nonterminal(self, nonterminal):
        self.nonterminals.add(nonterminal)

    def add_terminal(self, terminal):
        self.terminals.add(terminal)

    def add_production(self, nonterminal, production):
        if nonterminal not in self.productions:
            self.productions[nonterminal] = []

        self.productions[nonterminal].append(production)

    def set_start_symbol(self, start):
        self.start = start

    def add_nullable(self, symbol):
        self.nullable.add(symbol)


# Ejemplo de uso

# Crear una instancia de la gramática
grammar = Grammar()

# Definir los no terminales
grammar.add_nonterminal("E")
grammar.add_nonterminal("T")
grammar.add_nonterminal("F")

# Definir los terminales
grammar.add_terminal("+")
grammar.add_terminal("*")
grammar.add_terminal("(")
grammar.add_terminal(")")
grammar.add_terminal("id")

# Definir las producciones
grammar.add_production("E", ["T", "E'"])
grammar.add_production("E'", ["+", "T", "E'"])
grammar.add_production("E'", ["epsilon"])
grammar.add_production("T", ["F", "T'"])
grammar.add_production("T'", ["*", "F", "T'"])
grammar.add_production("T'", ["epsilon"])
grammar.add_production("F", ["(", "E", ")"])
grammar.add_production("F", ["id"])

# Definir el símbolo inicial
grammar.set_start_symbol("E")

# Marcar los símbolos nulos
grammar.add_nullable("E'")
grammar.add_nullable("T'")
grammar.add_nullable("F")

# Crear el analizador sintáctico LL(1)
parser = LLParser(grammar)

# Calcular los conjuntos FIRST
parser.compute_first_sets()

# Calcular los conjuntos FOLLOW
parser.compute_follow_sets()

# Construir la tabla de análisis
parser.build_parse_table()

# Analizar una cadena de entrada
input_string = "id + id * id"
parser.parse(input_string)
