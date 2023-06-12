class LRItem:
    def __init__(self, production, dot_index):
        self.production = production
        self.dot_index = dot_index

    def next_symbol(self):
        if self.dot_index < len(self.production):
            return self.production[self.dot_index]

    def is_reduce_item(self):
        return self.dot_index == len(self.production)

    def is_shift_item(self):
        return self.next_symbol() is not None and not self.is_reduce_item()

    def shift(self):
        return LRItem(self.production, self.dot_index + 1)


class LRParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.parse_table = {}

    def build_parse_table(self):
        for item in self.grammar.productions:
            for terminal in self.grammar.terminals:
                if item.is_reduce_item() and terminal in item.production:
                    self.parse_table[(item.production, terminal)] = item
                elif item.is_shift_item() and item.next_symbol() == terminal:
                    self.parse_table[(item.production, terminal)] = item.shift()

    def parse(self, input_tokens):
        stack = [0]
        input_tokens.append("$")
        current_token = input_tokens[0]
        while True:
            state = stack[-1]
            item = self.parse_table.get((state, current_token))
            if item is None:
                raise ValueError("Error: Unexpected token {}".format(current_token))
            if item.is_shift_item():
                stack.append(current_token)
                stack.append(item.state)
                input_tokens = input_tokens[1:]
                current_token = input_tokens[0]
            elif item.is_reduce_item():
                for _ in range(2 * len(item.production)):
                    stack.pop()
                goto_state = stack[-1]
                stack.append(item.production[0])
                stack.append(self.parse_table[(goto_state, item.production[0])].state)
            elif item.is_accept_item(self.grammar):
                break
        print("Input accepted.")


class Grammar:
    def __init__(self):
        self.non_terminals = set()
        self.terminals = set()
        self.productions = []
        self.start_symbol = None

    def add_production(self, production):
        non_terminal = production[0]
        self.non_terminals.add(non_terminal)
        for symbol in production[1:]:
            if isinstance(symbol, list):
                for nested_symbol in symbol:
                    self.terminals.add(nested_symbol)
            else:
                self.terminals.add(symbol)
        self.productions.append(production)


grammar = Grammar()

# Define the grammar productions
grammar.add_production(["E", ["E", "+", "T"]])
grammar.add_production(["E", ["T"]])
grammar.add_production(["T", ["T", "*", "F"]])
grammar.add_production(["T", ["F"]])
grammar.add_production(["F", ["(", "E", ")"]])
grammar.add_production(["F", ["id"]])

# Set the start symbol of the grammar
grammar.start_symbol = "E"

# Create the LR parser
parser = LRParser(grammar)

# Build the parsing table
parser.build_parse_table()

# Define the input tokens
input_tokens = ["id", "+", "id", "*", "id"]

# Parse the input
parser.parse(input_tokens)
