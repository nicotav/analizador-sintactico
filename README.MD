# Analizador sintáctico en Python

Este es un analizador sintáctico básico implementado en Python utilizando la biblioteca `nltk` (Natural Language Toolkit). El objetivo de este analizador es analizar la estructura gramatical de las oraciones en español.

## Requisitos

Antes de ejecutar el código del analizador sintáctico, asegúrate de tener instalada la biblioteca `nltk` en tu entorno de Python. Si no la tienes instalada, puedes ejecutar el siguiente comando en tu terminal para instalarla:


Además, necesitarás descargar los recursos necesarios para el tokenizador de oraciones (`punkt`) de NLTK. Para descargar estos recursos, puedes ejecutar el siguiente código en Python:

```python
import nltk
nltk.download('punkt')
```

## Uso
Una vez que hayas instalado las dependencias y descargado los recursos necesarios, puedes utilizar el analizador sintáctico. El código proporcionado incluye una gramática simple para analizar oraciones en español. Puedes personalizar y expandir esta gramática según tus necesidades.

Para analizar una oración, puedes llamar a la función parse_sentence y pasarle la oración como argumento. El analizador sintáctico intentará analizar la estructura gramatical de la oración y mostrará el árbol de análisis sintáctico resultante.

Aquí tienes un ejemplo de cómo utilizar el analizador sintáctico:

```
sentence = "El perro persiguió al gato"
parse_sentence(sentence)
```