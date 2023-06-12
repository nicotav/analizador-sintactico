import nltk
from nltk import CFG

# Definir la gramática
grammar = CFG.fromstring(
    """
    S -> NP VP
    NP -> Det N
    VP -> V NP
    Det -> 'the' | 'a'
    N -> 'dog' | 'cat'
    V -> 'chased' | 'saw'
"""
)
# Crear el analizador sintáctico
parser = nltk.ChartParser(grammar)


# Función para analizar una oración
def parse_sentence(sentence):
    words = nltk.word_tokenize(
        sentence.lower()
    )  # Tokenizar la oración en palabras y convertirlas a minúsculas
    for tree in parser.parse(words):  # Intentar analizar la oración
        tree.pretty_print()  # Imprimir el árbol de análisis sintáctico


# Ejemplo de uso
sentence = "The dog chased a cat"
parse_sentence(sentence)
