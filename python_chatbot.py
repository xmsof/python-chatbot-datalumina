"""
Chatbot Inteligente by Monica
Busca informacion en internet para responder cualquier pregunta.
Basado en el curso de Python de python.datalumina.com.
"""

import os
import sys
import textwrap
import random
import wikipedia
from duckduckgo_search import DDGS

# ============================================================================
# BASE DE CONOCIMIENTO LOCAL (Python)
# ============================================================================

PYTHON_TOPICS = {
    "definir_funciones": {
        "keywords": ["funcion", "funciones", "definir funcion", "crear funcion", "def"],
        "title": "Definir Funciones",
        "content": """Las funciones son bloques reutilizables de codigo que realizan tareas especificas.

SINTAXIS BASICA:
    def nombre_funcion():
        # Codigo aqui (indentado)
        pass

EJEMPLO:
    def saludar():
        print("Hola, mundo!")
        print("Bienvenido a Python!")

    saludar()  # Llamar a la funcion

PARTES CLAVE:
    * def - palabra clave que crea la funcion
    * Nombre seguido de parentesis ()
    * Dos puntos : para iniciar el cuerpo
    * Bloque de codigo indentado

NOMBRAMIENTO:
    * Usa minusculas
    * Separa palabras con guion bajo (_)
    * Ejemplo: calculate_total(), send_email()
    * NO uses: func1(), Calculate()""",
        "examples": [
            'def saludar():\n    print("Hola!")',
            'def calcular_area(ancho, alto):\n    return ancho * alto',
            'def verificar_edad(edad):\n    if edad >= 18:\n        print("Mayor de edad")\n    else:\n        print("Menor de edad")'
        ]
    },
    "parametros": {
        "keywords": ["parametro", "parametros", "argumento", "argumentos", "pasar datos"],
        "title": "Parametros",
        "content": """Los parametros permiten pasar datos a funciones para hacerlas flexibles.

PARAMETROS BASICOS:
    def saludar(nombre):
        print(f"Hola, {nombre}!")

    saludar("Alice")  # Hola, Alice!

MULTIPLES PARAMETROS:
    def presentar(nombre, edad):
        print(f"Me llamo {nombre}")
        print(f"Tengo {edad} anos")

VALORES POR DEFECTO:
    def saludar(nombre, saludo="Hola"):
        print(f"{saludo}, {nombre}!")

    saludar("Alice")            # Hola, Alice!
    saludar("Bob", "Hi")        # Hi, Bob!

ARGUMENTOS POR PALABRA CLAVE:
    def crear_perfil(nombre, edad, ciudad):
        print(f"{nombre}, {edad}, de {ciudad}")

    crear_perfil(ciudad="NYC", edad=25, nombre="Alice")""",
        "examples": [
            'def saludar(nombre, saludo="Hola"):\n    print(f"{saludo}, {nombre}!")',
            'def calcular_total(precio, impuesto, descuento):\n    return precio + (precio * impuesto) - descuento'
        ]
    },
    "valores_retorno": {
        "keywords": ["return", "retorno", "devolver", "resultado", "return values"],
        "title": "Valores de Retorno",
        "content": """Las funciones pueden calcular algo y devolver el resultado con 'return'.

RETURN vs PRINT:
    def sumar_print(a, b):
        print(a + b)  # Solo muestra

    def sumar_return(a, b):
        return a + b  # Devuelve valor

    resultado = sumar_return(5, 3)
    print(f"El resultado es {resultado}")  # El resultado es 8

RETORNAR MULTIPLES VALORES:
    def obtener_min_max(numeros):
        return min(numeros), max(numeros)

    minimo, maximo = obtener_min_max([5, 2, 8, 1, 9])

VALORES RETORNADOS PUEDEN USARSE EN:
    * Variables: resultado = funcion()
    * Expresiones: total = funcion1() + funcion2()
    * Condiciones: if funcion() > 10:
    * Como argumentos: print(funcion())""",
        "examples": [
            'def calcular_area(ancho, alto):\n    return ancho * alto',
            'def es_par(numero):\n    return numero % 2 == 0'
        ]
    },
    "alcance_variables": {
        "keywords": ["alcance", "scope", "variable local", "variable global", "local", "global"],
        "title": "Alcance de Variables (Scope)",
        "content": """Las variables tienen un "alcance" - donde pueden ser usadas.

VARIABLES LOCALES (solo existen dentro de la funcion):
    def calcular_precio():
        precio = 100
        impuesto = precio * 0.1
        print(f"Total: {precio + impuesto}")

    calcular_precio()  # Funciona
    print(precio)  # ERROR! precio no existe fuera

VARIABLES GLOBALES (existentes fuera de funciones):
    tasa_descuento = 0.15

    def aplicar_descuento(precio):
        descuento = precio * tasa_descuento
        return precio - descuento

MODIFICAR GLOBALES (usar global):
    contador = 0

    def incrementar():
        global contador
        contador += 1

MEJOR PRACTICA: Usa parametros y return, no globals!""",
        "examples": [
            'tasa = 0.15\ndef calcular_impuesto(precio):\n    return precio * tasa'
        ]
    },
    "variables": {
        "keywords": ["variable", "variables", "almacenar", "guardar datos", "asignar"],
        "title": "Variables",
        "content": """Las variables son como cajas etiquetadas donde guardas informacion.

CREAR VARIABLES:
    nombre = "Alice"
    edad = 25
    es_estudiante = True

NOMBRAMIENTO (reglas):
    * user_name = "Dave"    # snake_case (estilo Python)
    * age2 = 30             # numeros OK (no al inicio)
    * _privado = "secret"   # guion bajo al inicio OK
    * 2age = 30             # NO - no puede empezar con numero
    * my-name = "Dave"      # NO - no guiones
    * my name = "Dave"      # NO - no espacios
    * class = "Python"      # NO - palabra clave de Python

CAMBIAR VARIABLES:
    puntuacion = 0
    puntuacion = 10
    puntuacion = puntuacion + 5  # Ahora es 15

CONVENCION PYTHON: snake_case (minusculas con guion bajo)""",
        "examples": [
            'nombre = "Alice"\nedad = 25\nprint(f"{nombre} tiene {edad} anos")',
            'total = 0\ntotal += 10\ntotal += 20\nprint(total)  # 30'
        ]
    },
    "numeros": {
        "keywords": ["numero", "numeros", "entero", "float", "integer", "decimal", "matematicas", "suma", "resta", "multiplicacion", "division"],
        "title": "Numeros",
        "content": """Python tiene dos tipos de numeros:

ENTEROS (int) - numeros sin decimales:
    edad = 25
    puntuacion = -10

FLOTANTES (float) - numeros con decimales:
    precio = 19.99
    temperatura = -5.5
    pi = 3.14159

OPERACIONES MATEMATICAS:
    total = 10 + 5      # 15 - Suma
    cambio = 20 - 7     # 13 - Resta
    area = 6 * 4        # 24 - Multiplicacion
    mitad = 10 / 2      # 5.0 - Division (siempre float!)
    potencia = 5 ** 2   # 25 - Exponente

DIVISION ENTERA vs NORMAL:
    10 / 3   # 3.333... (float)
    10 // 3  # 3 (entero, redondea hacia abajo)

NOTA: Python usa punto (.) para decimales, NO coma!""",
        "examples": [
            'edad = 25\nprecio = 19.99\npi = 3.14159',
            'total = 10 + 5\narea = 6 * 4\npotencia = 2 ** 10'
        ]
    },
    "cadenas_texto": {
        "keywords": ["string", "texto", "cadena", "cadena de texto", "cadenas", "strings", "letras", "caracteres", "comillas"],
        "title": "Cadenas de Texto (Strings)",
        "content": """Los strings son texto - cualquier caracter entre comillas.

CREAR STRINGS:
    nombre = "Alice"
    mensaje = 'Hola, Mundo!'

COMBINAR STRINGS:
    nombre_completo = nombre + " " + apellido
    estrellas = "*" * 5  # "*****"

LONGITUD:
    mensaje = "Hola"
    print(len(mensaje))  # 4

CONVERTIR A STRING:
    edad = 25
    mensaje = "Tengo " + str(edad) + " anos"

F-STRINGS (la mejor forma):
    edad = 25
    mensaje = f"Tengo {edad} anos"
    print(f"La suma es {10 + 5}")  # La suma es 15""",
        "examples": [
            'nombre = "Alice"\nprint(f"Hola, {nombre}!")',
            'edad = 25\nmensaje = f"Tengo {edad} anos"',
            'texto = "Python"\nprint(len(texto))  # 6'
        ]
    },
    "booleans": {
        "keywords": ["boolean", "booleans", "bool", "verdadero", "falso", "true", "false"],
        "title": "Booleans (Verdadero/Falso)",
        "content": """Los booleans solo pueden ser True o False - son como respuestas si/no.

CREAR BOOLEANS:
    esta_logueado = True
    es_admin = False

IMPORTANTE: True y False con MAYUSCULA inicial!

COMPARACIONES:
    ==   Igual a
    !=   No igual a
    >    Mayor que
    <    Menor que
    >=   Mayor o igual
    <=   Menor o igual

EJEMPLO:
    edad = 18
    puede_votar = edad >= 18  # True""",
        "examples": [
            'es_adulto = True\nprint(type(es_adulto))  # <class \'bool\'>',
            'edad = 25\npuede_votar = edad >= 18\nprint(puede_votar)  # True'
        ]
    },
    "listas": {
        "keywords": ["lista", "listas", "array", "arreglo", "coleccion", "list", "append", "agregar"],
        "title": "Listas",
        "content": """Las listas son la estructura de datos mas versatil de Python.

CREAR LISTAS:
    frutas = ["manzana", "platano", "naranja"]
    numeros = [1, 2, 3, 4, 5]

ACCEDER A ELEMENTOS (empieza en 0):
    frutas[0]   # "manzana"
    frutas[-1]  # "naranja" (ultimo)

MODIFICAR LISTAS:
    frutas.append("uva")      # Agregar al final
    frutas.insert(1, "kiwi")  # Insertar en posicion
    frutas.remove("banana")   # Eliminar por valor
    ultimo = frutas.pop()     # Eliminar y devolver ultimo

METODOS UTILES:
    len(numeros)         # 6 (longitud)
    numeros.count(1)     # 2 (contar apariciones)
    numeros.sort()       # Ordenar
    numeros.reverse()    # Invertir""",
        "examples": [
            'frutas = ["manzana", "platano", "naranja"]\nfrutas.append("uva")\nprint(frutas)',
            'numeros = [1, 2, 3, 4, 5]\nfor num in numeros:\n    print(num)'
        ]
    },
    "diccionarios": {
        "keywords": ["diccionario", "diccionarios", "dict", "key value", "clave valor"],
        "title": "Diccionarios",
        "content": """Los diccionarios almacenan datos en pares clave-valor.

CREAR DICCIONARIOS:
    persona = {
        "nombre": "Alice",
        "edad": 30,
        "ciudad": "New York"
    }

ACCEDER A VALORES:
    print(persona["nombre"])          # "Alice"
    print(persona.get("trabajo"))     # None (sin error)

MODIFICAR DICCIONARIOS:
    persona["email"] = "alice@email.com"  # Agregar nuevo
    persona["edad"] = 31                   # Actualizar
    del persona["email"]                   # Eliminar

METODOS UTILES:
    persona.keys()    # Claves
    persona.values()  # Valores
    persona.items()   # Pares clave-valor""",
        "examples": [
            'persona = {"nombre": "Alice", "edad": 30}\nprint(persona["nombre"])',
            'notas = {"mat": 95, "ing": 87}\nfor clave, valor in notas.items():\n    print(f"{clave}: {valor}")'
        ]
    },
    "tuplas": {
        "keywords": ["tupla", "tuplas", "tuple", "immutable", "inmutable"],
        "title": "Tuplas",
        "content": """Las tuplas son como listas pero INMUTABLES (no se pueden cambiar).

CREAR TUPLAS:
    punto = (3, 5)
    colores = ("rojo", "verde", "azul")

DESEMPAQUETAR TUPLAS:
    punto = (3, 5)
    x, y = punto  # x = 3, y = 5

    # Intercambiar variables:
    x, y = y, x  # Intercambia valores!

PARA QUE USAR TUPLAS:
    * Coordenadas (x, y)
    * Colores RGB (255, 0, 0)
    * Registros de base de datos""",
        "examples": [
            'punto = (3, 5)\nx, y = punto\nprint(f"X: {x}, Y: {y}")',
            'colores = ("rojo", "verde", "azul")\nfor color in colores:\n    print(color)'
        ]
    },
    "conjuntos": {
        "keywords": ["conjunto", "conjuntos", "set", "sets", "unico", "sin duplicados"],
        "title": "Conjuntos (Sets)",
        "content": """Los conjuntos solo almacenan valores UNICOS (sin duplicados).

CREAR CONJUNTOS:
    numeros = {1, 2, 3, 4, 5}
    frutas = set(["manzana", "platano", "naranja"])

OPERACIONES:
    colores.add("verde")      # Agregar
    colores.remove("azul")    # Eliminar

ELIMINAR DUPLICADOS:
    nombres = ["Ana", "Bob", "Ana", "Charlie", "Bob"]
    nombres_unicos = list(set(nombres))""",
        "examples": [
            'numeros = [1, 2, 2, 3, 3, 4]\nunicos = set(numeros)\nprint(unicos)  # {1, 2, 3, 4}',
            'colores = {"rojo", "azul", "verde"}\nprint("rojo" in colores)  # True'
        ]
    },
    "if_statements": {
        "keywords": ["if", "si", "condicional", "condicion", "condicionales", "elif", "else", "decision"],
        "title": "If Statements (Condicionales)",
        "content": """Las sentencias if permiten que tu programa tome decisiones.

IF BASICO:
    edad = 18
    if edad >= 18:
        print("Puedes votar!")

IF-ELSE:
    temperatura = 25
    if temperatura > 30:
        print("Hace calor!")
    else:
        print("Clima agradable!")

IF-ELIF-ELSE (multiples condiciones):
    puntaje = 85
    if puntaje >= 90:
        print("A - Excelente!")
    elif puntaje >= 80:
        print("B - Buen trabajo!")
    elif puntaje >= 70:
        print("C - Sigue asi!")
    else:
        print("F - Necesitas mejorar")

COMBINAR CONDICIONES:
    # AND - ambas deben ser verdaderas
    if edad >= 18 and tiene_licencia:
        print("Puedes conducir!")

    # OR - al menos una debe ser verdadera
    if es_finde or es_feriado:
        print("No hay trabajo!")

    # NOT - invierte el valor
    if not llueve:
        print("Salgamos!")""",
        "examples": [
            'edad = 20\nif edad >= 18:\n    print("Mayor de edad")\nelse:\n    print("Menor de edad")',
            'nota = 85\nif nota >= 90:\n    print("A")\nelif nota >= 80:\n    print("B")\nelse:\n    print("C")'
        ]
    },
    "loops": {
        "keywords": ["loop", "loops", "bucle", "bucles", "for", "while", "iterar", "repetir"],
        "title": "Bucles (Loops)",
        "content": """Los bucles permiten repetir codigo sin copiar y pegar.

FOR LOOP (el mas comun):
    for i in range(5):
        print(i)  # 0, 1, 2, 3, 4

    # Contar desde 1
    for i in range(1, 6):
        print(i)  # 1, 2, 3, 4, 5

ITERAR TEXTO:
    nombre = "Python"
    for letra in nombre:
        print(letra)

ITERAR LISTA:
    colores = ["rojo", "azul", "verde"]
    for color in colores:
        print(f"Me gusta {color}")

WHILE LOOP (mientras sea verdadero):
    contador = 0
    while contador < 5:
        print(f"Contador: {contador}")
        contador += 1  # Siempre actualizar!

IMPORTANTE: Asegurate de que el while termine!""",
        "examples": [
            'for i in range(5):\n    print(f"Hola {i+1} veces!")',
            'frutas = ["manzana", "platano", "naranja"]\nfor fruta in frutas:\n    print(fruta)',
            'numero = 1\nwhile numero <= 10:\n    print(numero)\n    numero += 1'
        ]
    },
    "clases": {
        "keywords": ["clase", "clases", "object oriented", "orientado a objetos", "oop", "objeto", "objetos", "metodo", "self", "init"],
        "title": "Clases (POO)",
        "content": """Las clases permiten organizar codigo agrupando datos y funciones relacionadas.

QUE ES UNA CLASE?
    class MiBot:
        def __init__(self, nombre, modelo):
            self.nombre = nombre
            self.modelo = modelo

        def responder(self, pregunta):
            return "respuesta"

CREAR UNA CLASE:
    class Persona:
        def __init__(self, nombre, edad):
            self.nombre = nombre
            self.edad = edad

        def saludar(self):
            print(f"Hola, soy {self.nombre}")

    persona1 = Persona("Alice", 25)
    persona1.saludar()  # Hola, soy Alice

HERENCIA:
    class Animal:
        def hacer_sonido(self):
            print("Sonido generico")

    class Perro(Animal):
        def hacer_sonido(self):
            print("Guau!")""",
        "examples": [
            'class Persona:\n    def __init__(self, nombre, edad):\n        self.nombre = nombre\n        self.edad = edad\n\n    def saludar(self):\n        print(f"Hola, soy {self.nombre}")',
            'class Circulo:\n    def __init__(self, radio):\n        self.radio = radio\n\n    def area(self):\n        return 3.14 * self.radio ** 2'
        ]
    },
    "manejo_errores": {
        "keywords": ["error", "errores", "excepcion", "excepciones", "try", "except", "try except"],
        "title": "Manejo de Errores (Try/Except)",
        "content": """Try/except permite capturar errores antes de que tu programa se cierre.

ESTRUCTURA BASICA:
    try:
        # Codigo que podria fallar
        operacion_riesgosa()
    except:
        # Se ejecuta si hay error
        print("Algo salio mal")

ERRORES ESPECIFICOS:
    try:
        edad = int(input("Edad: "))
        print(f"En 10 anos tendras {edad + 10}")
    except ValueError:
        print("Por favor ingresa un numero")

MULTIPLES ERRORES:
    try:
        archivo = open('datos.txt', 'r')
        datos = archivo.read()
    except FileNotFoundError:
        print("Archivo no encontrado")
    except ValueError:
        print("Formato invalido")

ELSE (solo si NO hubo error):
    try:
        archivo = open('datos.txt', 'r')
    else:
        print(f"Archivo tiene {len(datos)} caracteres")

FINALLY (siempre se ejecuta):
    try:
        archivo = open('datos.txt', 'r')
    finally:
        print("Limpieza completa")""",
        "examples": [
            'try:\n    numero = int(input("Ingresa un numero: "))\nexcept ValueError:\n    print("Eso no es un numero valido")',
            'try:\n    resultado = 10 / 0\nexcept ZeroDivisionError:\n    print("No se puede dividir por cero")'
        ]
    },
    "organizar_codigo": {
        "keywords": ["organizar", "modular", "imports", "importar", "archivos", "modulos"],
        "title": "Organizar Codigo",
        "content": """A medida que tus scripts crecen, debes organizarlos en funciones y archivos.

CREAR ARCHIVOS HELPER:
    # helpers.py
    def calcular_total(cantidad, precio):
        return cantidad * precio

    def formatear_moneda(monto):
        return f"${monto:,.2f}"

USAR EN OTRO ARCHIVO:
    # analizador.py
    from helpers import calcular_total, formatear_moneda

    total = calcular_total(5, 10)
    print(formatear_moneda(total))  # $50.00

BENEFICIOS:
    * Reutilizable - escribe una vez, usa muchas veces
    * Legible - el script principal queda limpio
    * Testeable - facil probar cada funcion por separado""",
        "examples": [
            '# helpers.py\ndef calcular_total(cant, precio):\n    return cant * precio',
            '# main.py\nfrom helpers import calcular_total\ntotal = calcular_total(3, 15)\nprint(total)'
        ]
    },
    "primer_programa": {
        "keywords": ["primer", "primero", "hello world", "iniciar", "empezar", "instalar python", "vscode"],
        "title": "Tu Primer Programa en Python",
        "content": """Para empezar con Python:

INSTALAR PYTHON:
    Descarga desde python.org e instala.
    Marca "Add Python to PATH" durante la instalacion.

CREAR ARCHIVO:
    1. Abre VS Code
    2. Crea un archivo llamado hola.py
    3. Escribe:
        print("Hola, Mundo!")
        print("Estoy aprendiendo Python para IA")

EJECUTAR:
    * Boton Run (triangulo) en la esquina superior derecha
    * Click derecho > "Run Python File in Terminal"
    * Ctrl+F5 (Windows) o Cmd+F5 (Mac)""",
        "examples": [
            'print("Hola, Mundo!")',
            'print("Estoy aprendiendo Python para IA")'
        ]
    },
    "por_que_python": {
        "keywords": ["por que python", "porque python", "ventajas python", "beneficios python", "ia", "inteligencia artificial"],
        "title": "Por Que Python?",
        "content": """Python es el lenguaje dominante en IA y desarrollo:

VENTAJAS:
    * Facil de aprender - Python se lee como ingles
    * Librerias de IA - TensorFlow, PyTorch, scikit-learn
    * Estandar de la industria - Usado por todas las empresas de IA
    * Gran comunidad - Millones de desarrolladores

PYTHON EN IA:
    * Modelos de lenguaje (ChatGPT, Claude)
    * Vision por computadora (Tesla Autopilot)
    * Analisis de datos (Netflix recommendations)
    * Machine Learning (Spotify playlists)

MERCADO LABORAL:
    * Alta demanda: Desarrolladores Python IA ganan $130,000+
    * Trabajo remoto: Programa desde cualquier lugar
    * Campo creciente: 40% de crecimiento anual""",
        "examples": []
    }
}

# ============================================================================
# SISTEMA DE BUSQUEDA EN INTERNET
# ============================================================================

def search_internet(query, num_results=5):
    """Busca informacion en internet usando DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_results))
            return results
    except Exception as e:
        return []

def search_wikipedia(query, sentences=3):
    """Busca en Wikipedia."""
    try:
        wikipedia.set_lang("es")
        page = wikipedia.page(query, auto_suggest=True)
        summary = wikipedia.summary(query, sentences=sentences, auto_suggest=True)
        return summary, page.url
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            page = wikipedia.page(e.options[0], auto_suggest=False)
            summary = wikipedia.summary(e.options[0], sentences=sentences, auto_suggest=False)
            return summary, page.url
        except:
            return None, None
    except wikipedia.exceptions.PageError:
        return None, None
    except Exception as e:
        return None, None

def smart_search(query):
    """Busqueda inteligente: primero Wikipedia, luego DuckDuckGo."""
    print("  Buscando en internet...", end="\r")

    summary, url = search_wikipedia(query)
    if summary and len(summary) > 100:
        print(" " * 30)
        return format_wikipedia_response(query, summary, url)

    results = search_internet(query, num_results=5)
    if results:
        print(" " * 30)
        return format_search_results(query, results)

    print(" " * 30)
    return None

def format_wikipedia_response(query, summary, url):
    """Formatea respuesta de Wikipedia."""
    response = []
    response.append(f"\n{'='*60}")
    response.append(f"  Wikipedia: {query}")
    response.append(f"{'='*60}")
    response.append("")
    response.append(textwrap.fill(summary, width=60))
    response.append("")
    response.append(f"  Mas informacion: {url}")
    response.append(f"{'='*60}")
    return "\n".join(response)

def format_search_results(query, results):
    """Formatea resultados de busqueda."""
    response = []
    response.append(f"\n{'='*60}")
    response.append(f"  Resultados para: {query}")
    response.append(f"{'='*60}")

    for i, result in enumerate(results[:5], 1):
        title = result.get("title", "Sin titulo")
        body = result.get("body", "Sin descripcion")
        link = result.get("href", "")

        response.append(f"\n  {i}. {title}")
        response.append(f"     {body[:200]}..." if len(body) > 200 else f"     {body}")
        if link:
            response.append(f"     Link: {link}")

    response.append(f"\n{'='*60}")
    return "\n".join(response)

# ============================================================================
# FUNCIONES DEL CHATBOT
# ============================================================================

def normalize(text):
    """Normaliza texto para mejor coincidencia."""
    text = text.lower().strip()
    replacements = {
        'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u',
        'n': 'n', 'u': 'u'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def find_local_match(query):
    """Busca si hay un tema local que coincida."""
    query_norm = normalize(query)
    scores = {}

    for topic_id, topic in PYTHON_TOPICS.items():
        score = 0
        for keyword in topic["keywords"]:
            keyword_norm = normalize(keyword)
            if keyword_norm in query_norm:
                score += 10
            elif any(word in query_norm for word in keyword_norm.split()):
                score += 3
        if score > 0:
            scores[topic_id] = score

    if scores:
        return max(scores, key=scores.get)
    return None

def format_local_response(topic_id):
    """Formatea respuesta local de Python."""
    topic = PYTHON_TOPICS[topic_id]
    response = []
    response.append(f"\n{'='*60}")
    response.append(f"  {topic['title']}")
    response.append(f"{'='*60}")
    response.append(topic['content'])

    if topic['examples']:
        response.append(f"\n{'─'*60}")
        response.append("  EJEMPLOS DE CODIGO:")
        response.append(f"{'─'*60}")
        for i, example in enumerate(topic['examples'], 1):
            response.append(f"\n  Ejemplo {i}:")
            response.append(textwrap.indent(example, "    "))

    response.append(f"{'='*60}")
    return "\n".join(response)

def get_help_text():
    """Retorna texto de ayuda."""
    return """
╔══════════════════════════════════════════════════════════════╗
║        CHATBOT INTELIGENTE BY MONICA                        ║
║        Busca informacion en internet                        ║
╚══════════════════════════════════════════════════════════════╝

  COMANDOS:
    /ayuda     - Muestra esta ayuda
    /temas     - Lista temas de Python
    /quiz      - Quiz aleatorio de Python
    /web       - Buscar algo en internet
    /salir     - Sale del chatbot

  PUEDES PREGUNTAR SOBRE CUALQUIER TEMA:
    * Python (funciones, variables, listas, etc.)
    * Cualquier tema en general
    * Ciencia, historia, tecnologia, etc.

  EJEMPLOS:
    "Que son las funciones?"
    "Como creo una lista?"
    "Que es la inteligencia artificial?"
    "Quien es Elon Musk?"
    "Como funciona Bitcoin?"
    "Cual es la capital de Francia?"
    "Explicame la fisica cuantica"

  Consejo: Puedes escribir en espanol natural!
  Si no se el tema local, busco en internet!
"""

def get_topics_list():
    """Retorna lista de temas de Python."""
    response = "\n  TEMAS DE PYTHON DISPONIBLES:\n"
    response += "  " + "─" * 40 + "\n"
    categories = {
        "FUNCIONES": ["definir_funciones", "parametros", "valores_retorno", "alcance_variables"],
        "VARIABLES Y TIPOS": ["variables", "numeros", "cadenas_texto", "booleans"],
        "ESTRUCTURAS DE DATOS": ["listas", "diccionarios", "tuplas", "conjuntos"],
        "FLUJO DE CONTROL": ["if_statements", "loops"],
        "POO": ["clases"],
        "MANEJO DE ERRORES": ["manejo_errores"],
        "ORGANIZACION": ["organizar_codigo", "primer_programa", "por_que_python"]
    }

    for category, topics in categories.items():
        response += f"\n  {category}:\n"
        for topic_id in topics:
            if topic_id in PYTHON_TOPICS:
                response += f"    * {PYTHON_TOPICS[topic_id]['title']}\n"

    response += "\n  " + "─" * 40
    response += "\n  Puedes preguntar cualquier otra cosa y buscare en internet!\n"
    return response

def generate_quiz():
    """Genera un quiz aleatorio de Python."""
    quizzes = [
        {
            "question": "Quiz: Cual es la sintaxis correcta para definir una funcion?",
            "options": ["A) function mi_funcion(): pass", "B) def mi_funcion(): pass", "C) func mi_funcion() pass", "D) define mi_funcion(): pass"],
            "correct": "B",
            "explanation": "Correcto! Se usa 'def' seguido del nombre y parentesis."
        },
        {
            "question": "Quiz: Cual de estas es una variable valida en Python?",
            "options": ["A) 2nombre = 'Ana'", "B) mi-nombre = 'Ana'", "C) mi_nombre = 'Ana'", "D) my name = 'Ana'"],
            "correct": "C",
            "explanation": "Correcto! Python usa snake_case: mi_nombre."
        },
        {
            "question": "Quiz: Como se escribe 'else if' en Python?",
            "options": ["A) elseif", "B) else if", "C) elif", "D) elifse"],
            "correct": "C",
            "explanation": "Correcto! En Python se usa 'elif'."
        },
        {
            "question": "Quiz: Como agregas un elemento al final de una lista?",
            "options": ["A) lista.add(elemento)", "B) lista.append(elemento)", "C) lista.insert(elemento)", "D) lista.push(elemento)"],
            "correct": "B",
            "explanation": "Correcto! append() agrega al final."
        },
        {
            "question": "Quiz: Que imprime 'for i in range(3): print(i)'?",
            "options": ["A) 1, 2, 3", "B) 0, 1, 2", "C) 0, 1, 2, 3", "D) 1, 2"],
            "correct": "B",
            "explanation": "Correcto! range(3) genera 0, 1, 2."
        }
    ]

    quiz = random.choice(quizzes)
    print(f"\n{quiz['question']}\n")
    for option in quiz['options']:
        print(f"  {option}")
    print()

    answer = input("Tu respuesta (A/B/C/D): > ").strip().upper()
    if answer == quiz['correct']:
        print(f"\n  Correcto! {quiz['explanation']}")
    else:
        print(f"\n  Incorrecto. {quiz['explanation']}")

# ============================================================================
# LOOP PRINCIPAL
# ============================================================================

def main():
    print("\n" + "╔" + "═"*58 + "╗")
    print("║" + " "*10 + "CHATBOT INTELIGENTE BY MONICA" + " "*18 + "║")
    print("║" + " "*12 + "Busca informacion en internet" + " "*16 + "║")
    print("╚" + "═"*58 + "╝")
    print()
    print("  Escribe /ayuda para ver los comandos disponibles.")
    print("  Pregunta cualquier cosa - busco en internet si no se la respuesta!")
    print()

    while True:
        try:
            user_input = input("Tu > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Hasta luego! Sigue aprendiendo!")
            break

        if not user_input:
            continue

        if user_input.lower() in ["/salir", "/exit", "/quit", "salir", "adios", "chao"]:
            print("  Hasta luego! Sigue aprendiendo!")
            break

        if user_input.lower() in ["/ayuda", "/help", "ayuda", "help"]:
            print(get_help_text())
            continue

        if user_input.lower() in ["/temas", "/topics", "temas"]:
            print(get_topics_list())
            continue

        if user_input.lower() in ["/quiz", "quiz"]:
            generate_quiz()
            continue

        if user_input.lower().startswith("/web "):
            query = user_input[5:].strip()
            if query:
                result = smart_search(query)
                if result:
                    print(result)
                else:
                    print("  No encontre resultados. Intenta con otra busqueda.")
            else:
                print("  Usa /web seguido de lo que quieras buscar.")
            continue

        local_topic = find_local_match(user_input)
        if local_topic:
            print(format_local_response(local_topic))
        else:
            result = smart_search(user_input)
            if result:
                print(result)
            else:
                print("  No encontre informacion sobre eso.")
                print("  Intenta reformular tu pregunta o usa /web seguido de tu busqueda.")

if __name__ == "__main__":
    main()
