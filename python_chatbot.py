"""
Chatbot Inteligente by Monica
Basado en el curso de Python de python.datalumina.com
Potenciado por DeepSeek API
"""

import os
import sys
import json
import textwrap
import random
import requests

# ============================================================================
# BASE DE CONOCIMIENTO
# ============================================================================

KNOWLEDGE_BASE = {
    "definir_funciones": {
        "keywords": ["funcion", "funciones", "definir funcion", "crear funcion", "def"],
        "title": "Definir Funciones",
        "content": """Las funciones son bloques reutilizables de codigo.
SINTAXIS: def nombre_funcion():
    # Codigo aqui (indentado)
EJEMPLO:
    def saludar():
        print("Hola, mundo!")
    saludar()
PARTES CLAVE: def, nombre, (), :, indentacion
NOMBRAMIENTO: snake_case (calculate_total, send_email)""",
        "examples": [
            'def saludar():\n    print("Hola!")',
            'def calcular_area(ancho, alto):\n    return ancho * alto'
        ]
    },
    "parametros": {
        "keywords": ["parametro", "parametros", "argumento", "argumentos"],
        "title": "Parametros",
        "content": """Los parametros permiten pasar datos a funciones.
EJEMPLO:
    def saludar(nombre):
        print(f"Hola, {nombre}!")
    saludar("Alice")
VALORES POR DEFECTO:
    def saludar(nombre, saludo="Hola"):
        print(f"{saludo}, {nombre}!")
ARGUMENTOS POR PALABRA CLAVE:
    crear_perfil(ciudad="NYC", edad=25, nombre="Alice")""",
        "examples": [
            'def saludar(nombre, saludo="Hola"):\n    print(f"{saludo}, {nombre}!")'
        ]
    },
    "valores_retorno": {
        "keywords": ["return", "retorno", "devolver", "resultado"],
        "title": "Valores de Retorno",
        "content": """Las funciones devuelven valores con 'return'.
RETURN vs PRINT:
    def sumar(a, b):
        return a + b  # Devuelve valor
    resultado = sumar(5, 3)  # resultado = 8
MULTIPLES VALORES:
    def min_max(numeros):
        return min(numeros), max(numeros)
    minimo, maximo = min_max([5, 2, 8])""",
        "examples": [
            'def calcular_area(ancho, alto):\n    return ancho * alto',
            'def es_par(numero):\n    return numero % 2 == 0'
        ]
    },
    "variables": {
        "keywords": ["variable", "variables", "almacenar", "guardar datos"],
        "title": "Variables",
        "content": """Las variables almacenan datos con un nombre.
CREAR: nombre = "Alice", edad = 25
REGLAS: snake_case, no numeros al inicio, sin guiones/espacios
CAMBIAR: puntuacion = 0, puntuacion = 10""",
        "examples": [
            'nombre = "Alice"\nedad = 25\nprint(f"{nombre} tiene {edad} anos")'
        ]
    },
    "numeros": {
        "keywords": ["numero", "numeros", "entero", "float", "decimal", "matematicas"],
        "title": "Numeros",
        "content": """ENTEROS (int): 25, -10
FLOTANTES (float): 19.99, 3.14159
OPERACIONES: +, -, *, /, //(entero), **(potencia), %(resto)
NOTA: 10 / 3 = 3.333, 10 // 3 = 3""",
        "examples": [
            'total = 10 + 5\narea = 6 * 4\npotencia = 2 ** 10'
        ]
    },
    "cadenas_texto": {
        "keywords": ["string", "texto", "cadena", "strings"],
        "title": "Cadenas de Texto (Strings)",
        "content": """Strings son texto entre comillas.
CREAR: nombre = "Alice", mensaje = 'Hola'
COMBINAR: nombre + " " + apellido
LONGITUD: len(mensaje)
F-STRINGS: f"Hola, {nombre}!" (la mejor forma)""",
        "examples": [
            'nombre = "Alice"\nprint(f"Hola, {nombre}!")',
            'texto = "Python"\nprint(len(texto))  # 6'
        ]
    },
    "booleans": {
        "keywords": ["boolean", "booleans", "bool", "verdadero", "falso", "true", "false"],
        "title": "Booleans",
        "content": """Solo pueden ser True o False (con mayuscula).
COMPARACIONES: ==, !=, >, <, >=, <=
LOGICOS: and, or, not
EJEMPLO: puede_votar = edad >= 18""",
        "examples": [
            'edad = 25\npuede_votar = edad >= 18\nprint(puede_votar)  # True'
        ]
    },
    "listas": {
        "keywords": ["lista", "listas", "array", "append", "agregar"],
        "title": "Listas",
        "content": """Colecciones ordenadas y mutables.
CREAR: frutas = ["manzana", "platano"]
ACCEDER: frutas[0], frutas[-1]
MODIFICAR: append(), insert(), remove(), pop()
METODOS: len(), sort(), reverse(), count(), index()""",
        "examples": [
            'frutas = ["manzana", "platano"]\nfrutas.append("naranja")\nprint(frutas)'
        ]
    },
    "diccionarios": {
        "keywords": ["diccionario", "diccionarios", "dict", "clave valor"],
        "title": "Diccionarios",
        "content": """Pares clave-valor.
CREAR: persona = {"nombre": "Alice", "edad": 30}
ACCEDER: persona["nombre"], persona.get("clave", default)
MODIFICAR: persona["email"] = "a@b.com"
METODOS: keys(), values(), items()""",
        "examples": [
            'persona = {"nombre": "Alice", "edad": 30}\nprint(persona["nombre"])'
        ]
    },
    "tuplas": {
        "keywords": ["tupla", "tuplas", "tuple", "inmutable"],
        "title": "Tuplas",
        "content": """Como listas pero INMUTABLES.
CREAR: punto = (3, 5)
DESEMPAQUETAR: x, y = punto
USOS: coordenadas, colores RGB, retornos de funciones""",
        "examples": [
            'punto = (3, 5)\nx, y = punto\nprint(f"X: {x}, Y: {y}")'
        ]
    },
    "conjuntos": {
        "keywords": ["conjunto", "conjuntos", "set", "sets", "unico"],
        "title": "Conjuntos (Sets)",
        "content": """Valores UNICOS (sin duplicados).
CREAR: numeros = {1, 2, 3}
VACIO: set() NO {}
OPERACIONES: add(), remove(), discard()
ELIMINAR DUPLICADOS: list(set(lista))""",
        "examples": [
            'numeros = [1, 2, 2, 3]\nunicos = set(numeros)\nprint(unicos)  # {1, 2, 3}'
        ]
    },
    "if_statements": {
        "keywords": ["if", "si", "condicional", "condicion", "elif", "else"],
        "title": "If Statements",
        "content": """Decisiones en el codigo.
IF: if condicion:
ELSE: if condicion: ... else:
ELIF: if ... elif ... else:
LOGICOS: and, or, not
ANIDADOS: if dentro de if""",
        "examples": [
            'nota = 85\nif nota >= 90:\n    print("A")\nelif nota >= 80:\n    print("B")\nelse:\n    print("C")'
        ]
    },
    "loops": {
        "keywords": ["loop", "loops", "bucle", "bucles", "for", "while", "iterar"],
        "title": "Bucles (Loops)",
        "content": """Repetir codigo.
FOR: for i in range(5):
WHILE: while condicion:
ITERAR: for item in lista:
IMPORTANTE: while siempre debe terminar!""",
        "examples": [
            'for i in range(5):\n    print(f"Hola {i+1} veces!")',
            'frutas = ["a", "b", "c"]\nfor f in frutas:\n    print(f)'
        ]
    },
    "clases": {
        "keywords": ["clase", "clases", "oop", "objeto", "objetos", "self", "init"],
        "title": "Clases (POO)",
        "content": """Organizar codigo con datos y funciones juntos.
CREAR: class Persona:
    def __init__(self, nombre):
        self.nombre = nombre
METODOS: funciones dentro de la clase
HERENCIA: class Hijo(Padre):""",
        "examples": [
            'class Persona:\n    def __init__(self, nombre):\n        self.nombre = nombre\n    def saludar(self):\n        print(f"Hola, soy {self.nombre}")'
        ]
    },
    "manejo_errores": {
        "keywords": ["error", "errores", "try", "except", "excepcion"],
        "title": "Manejo de Errores",
        "content": """Capturar errores con try/except.
BASICO:
    try:
        risky_operation()
    except ValueError:
        print("Error de valor")
ESPECIFICOS: ValueError, FileNotFoundError, ZeroDivisionError
ELSE: ejecuta si NO hubo error
FINALLY: siempre se ejecuta""",
        "examples": [
            'try:\n    numero = int(input("Edad: "))\nexcept ValueError:\n    print("Ingresa un numero")'
        ]
    }
}

# ============================================================================
# SYSTEM PROMPT PARA DEEPSEEK
# ============================================================================

SYSTEM_PROMPT = """Eres un asistente de Python experto y amigable llamado "Chatbot Inteligente by Monica".

Tu conocimiento esta basado en el curso de Python de python.datalumina.com. Debes:

1. Responder en espanol
2. Ser conciso pero completo
3. Siempre incluir ejemplos de codigo cuando sea relevante
4. Explicar conceptos de forma simple
5. Si te preguntan algo de Python, responder con la mejor explicacion posible
6. Si no sabes algo, ser honesto pero intentar ayudar

Formato de respuesta:
- Usa bloques de codigo con ```python
- Secciona respuestas largas
- Incluye ejemplos practicos
- Sé amigable y motivador

Aqui tienes referencia de los temas del curso:

FUNCIONES: def nombre(), parametros, return, alcance (local/global)
VARIABLES: nombre = valor, snake_case, tipos dinamicos
TIPOS: int, float, str, bool
ESTRUCTURAS: listas [], diccionarios {}, tuplas (), conjuntos {}
CONTROL: if/elif/else, for, while
POO: class, __init__, self, herencia
ERRORES: try/except/else/finally
"""

# ============================================================================
# FUNCIONES DE LA API DEEPSEEK
# ============================================================================

def call_deepseek_api(messages, api_key):
    """Llama a la API de DeepSeek para obtener una respuesta."""
    url = "https://api.deepseek.com/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000,
        "top_p": 0.9
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "Error: La conexion tardo demasiado. Intenta de nuevo."
    except requests.exceptions.ConnectionError:
        return "Error: No se pudo conectar a DeepSeek. Verifica tu conexion a internet."
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            return "Error: API key invalida. Verifica tu clave."
        elif e.response.status_code == 429:
            return "Error: Demasiadas solicitudes. Espera un momento."
        else:
            return f"Error de la API: {e}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

def build_context_messages(user_input, conversation_history, api_key):
    """Construye los mensajes con contexto del curso."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in conversation_history[-10:]:
        messages.append(msg)

    messages.append({"role": "user", "content": user_input})

    return messages

# ============================================================================
# FUNCIONES UTILITARIAS
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

    for topic_id, topic in KNOWLEDGE_BASE.items():
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

def get_help_text():
    """Retorna texto de ayuda."""
    return """
╔══════════════════════════════════════════════════════════════╗
║        CHATBOT INTELIGENTE BY MONICA                        ║
║        Potenciado por DeepSeek API                          ║
╚══════════════════════════════════════════════════════════════╝

  COMANDOS:
    /ayuda     - Muestra esta ayuda
    /temas     - Lista todos los temas disponibles
    /quiz      - Inicia un quiz aleatorio
    /limpiar   - Limpia el historial de conversacion
    /salir     - Sale del chatbot

  PUEDES PREGUNTAR SOBRE CUALQUIER TEMA DE PYTHON:
    * Funciones (def, parametros, return)
    * Variables y tipos de datos
    * Numeros, strings, booleans
    * Listas, diccionarios, tuplas, conjuntos
    * If statements y loops
    * Clases y POO
    * Manejo de errores (try/except)
    * Y CUALQUIER otra pregunta de Python!

  EJEMPLOS:
    "Que son las funciones?"
    "Como creo una lista?"
    "Enseñame if statements"
    "Dame un ejemplo de loops"
    "Que es un diccionario?"
    "Como manejo errores en Python?"
    "Cual es la diferencia entre print y return?"
    "Como instalo Python?"
    "Explicame decoradores"
    "Que son las list comprehension?"

  Consejo: Puedes escribir en espanol natural!
  Pregunta lo que quieras, DeepSeek te respondra!
"""

def get_topics_list():
    """Retorna lista de temas disponibles."""
    response = "\n  TEMAS DISPONIBLES:\n"
    response += "  " + "─" * 40 + "\n"
    categories = {
        "FUNCIONES": ["definir_funciones", "parametros", "valores_retorno"],
        "VARIABLES Y TIPOS": ["variables", "numeros", "cadenas_texto", "booleans"],
        "ESTRUCTURAS DE DATOS": ["listas", "diccionarios", "tuplas", "conjuntos"],
        "FLUJO DE CONTROL": ["if_statements", "loops"],
        "POO": ["clases"],
        "MANEJO DE ERRORES": ["manejo_errores"]
    }

    for category, topics in categories.items():
        response += f"\n  {category}:\n"
        for topic_id in topics:
            if topic_id in KNOWLEDGE_BASE:
                response += f"    * {KNOWLEDGE_BASE[topic_id]['title']}\n"

    response += "\n  " + "─" * 40
    response += "\n  Tambien puedes preguntar cualquier otra cosa sobre Python!\n"
    return response

def generate_quiz():
    """Genera un quiz aleatorio."""
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
# LOOP PRINCIPAL DEL CHATBOT
# ============================================================================

def main():
    print("\n" + "╔" + "═"*58 + "╗")
    print("║" + " "*10 + "CHATBOT INTELIGENTE BY MONICA" + " "*18 + "║")
    print("║" + " "*14 + "Potenciado por DeepSeek API" + " "*17 + "║")
    print("╚" + "═"*58 + "╝")
    print()

    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        print("  No se encontro la variable de entorno DEEPSEEK_API_KEY.")
        print()
        api_key = input("  Ingresa tu API key de DeepSeek: > ").strip()

        if not api_key:
            print("\n  Error: Necesitas una API key para usar el chatbot.")
            print("  Obtala gratis en: https://platform.deepseek.com/")
            print()
            save = input("  Quieres guardarla como variable de entorno? (s/n): > ").strip().lower()
            if save == 's':
                try:
                    os.system(f'setx DEEPSEEK_API_KEY "{api_key}"')
                    print("  API key guardada. Reinicia PowerShell para que surta efecto.")
                except:
                    print("  No se pudo guardar automaticamente.")
                    print(f"  Guarda manualmente: setx DEEPSEEK_API_KEY \"{api_key}\"")
            print()
            input("  Presiona Enter para continuar sin API...")

    conversation_history = []

    print("  Escribe /ayuda para ver los comandos disponibles.")
    print("  Escribe cualquier pregunta sobre Python!")
    print()

    while True:
        try:
            user_input = input("Tu > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Hasta luego! Sigue practicando Python!")
            break

        if not user_input:
            continue

        if user_input.lower() in ["/salir", "/exit", "/quit", "salir", "adios", "chao"]:
            print("  Hasta luego! Sigue practicando Python!")
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

        if user_input.lower() in ["/limpiar", "/clear", "limpiar", "clear"]:
            conversation_history.clear()
            print("  Historial limpiado!")
            continue

        if not api_key:
            local_topic = find_local_match(user_input)
            if local_topic:
                topic = KNOWLEDGE_BASE[local_topic]
                print(f"\n{'='*60}")
                print(f"  {topic['title']}")
                print(f"{'='*60}")
                print(topic['content'])
                if topic['examples']:
                    print(f"\n  Ejemplos:")
                    for ex in topic['examples']:
                        print(f"  {ex}")
                print(f"{'='*60}\n")
            else:
                print("  Sin API key, solo puedo responder preguntas del curso.")
                print("  Ingresa tu API key o escribe /ayuda para ver temas.\n")
            continue

        print("  Pensando...", end="\r")

        conversation_history.append({"role": "user", "content": user_input})

        messages = build_context_messages(user_input, conversation_history, api_key)

        response = call_deepseek_api(messages, api_key)

        conversation_history.append({"role": "assistant", "content": response})

        print(f"\nMonica > {response}\n")

if __name__ == "__main__":
    main()
