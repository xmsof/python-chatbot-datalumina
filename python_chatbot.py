"""
Python Datalumina Chatbot - Basado en el curso de Python de python.datalumina.com
Un chatbot inteligente que puede responder preguntas sobre Python, enseñar conceptos,
dar ejemplos de codigo, y hacer seguimiento del progreso del estudiante.
"""

import re
import sys
import textwrap
from datetime import datetime

# ============================================================================
# BASE DE CONOCIMIENTO
# ============================================================================

KNOWLEDGE_BASE = {
    # --- FUNCIONES ---
    "definir_funciones": {
        "keywords": ["funcion", "funciones", "definir funcion", "crear funcion", "def", "como se crea", "como creo"],
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
        "keywords": ["parametro", "parametros", "argumento", "argumentos", "pasar datos", "entrada", "parametro por defecto", "valor por defecto", "keyword argument"],
        "title": "Parametros",
        "content": """Los parametros permiten pasar datos a funciones para hacerlas flexibles.

PARAMETROS BASICOS:
    def saludar(nombre):
        print(f"Hola, {nombre}!")

    saludar("Alice")  # Hola, Alice!
    saludar("Bob")    # Hola, Bob!

MULTIPLES PARAMETROS:
    def presentar(nombre, edad):
        print(f"Me llamo {nombre}")
        print(f"Tengo {edad} anos")

    presentar("Alice", 25)

VALORES POR DEFECTO:
    def saludar(nombre, saludo="Hola"):
        print(f"{saludo}, {nombre}!")

    saludar("Alice")            # Hola, Alice!
    saludar("Bob", "Hi")        # Hi, Bob!

ARGUMENTOS POR PALABRA CLAVE:
    def crear_perfil(nombre, edad, ciudad):
        print(f"{nombre}, {edad}, de {ciudad}")

    crear_perfil(ciudad="NYC", edad=25, nombre="Alice")

REGLA IMPORTANTE: Pon los parametros con valores por defecto AL FINAL.
    def mi_funcion(x, y=10):  # Correcto
    def mi_funcion(x=10, y):  # ERROR!""",
        "examples": [
            'def saludar(nombre, saludo="Hola"):\n    print(f"{saludo}, {nombre}!")',
            'def calcular_total(precio, impuesto, descuento):\n    return precio + (precio * impuesto) - descuento'
        ]
    },

    "valores_retorno": {
        "keywords": ["return", "retorno", "devolver", "resultado", "return values", "retorno de valores"],
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
    * Como argumentos: print(funcion())

SIN RETURN:
    def saludar(nombre):
        print(f"Hola, {nombre}!")
    # Sin return explicito, devuelve None""",
        "examples": [
            'def calcular_area(ancho, alto):\n    return ancho * alto',
            'def obtener_min_max(numeros):\n    return min(numeros), max(numeros)',
            'def es_par(numero):\n    return numero % 2 == 0'
        ]
    },

    "alcance_variables": {
        "keywords": ["alcance", "scope", "variable local", "variable global", "local", "global", "ambito"],
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

    resultado = aplicar_descuento(100)
    print(resultado)  # 85.0

MODIFICAR GLOBALES (usar global):
    contador = 0

    def incrementar():
        global contador
        contador += 1

    incrementar()
    print(contador)  # 1

MEJOR PRACTICA: Usa parametros y return, no globals!
    # MAL: variable global + global
    # BIEN: pasar datos como parametro y devolver resultado""",
        "examples": [
            'tasa = 0.15\ndef calcular_impuesto(precio):\n    return precio * tasa'
        ]
    },

    # --- VARIABLES ---
    "variables": {
        "keywords": ["variable", "variables", "almacenar", "guardar datos", "nombres", "asignar"],
        "title": "Variables",
        "content": """Las variables son como cajas etiquetadas donde guardas informacion.

CREAR VARIABLES:
    nombre = "Alice"
    edad = 25
    es_estudiante = True

NOMBRAMIENTO (reglas):
    ALLOWED:
        user_name = "Dave"    # snake_case (estilo Python)
        age2 = 30             # numeros OK (no al inicio)
        _privado = "secret"   # guion bajo al inicio OK

    NOT ALLOWED:
        2age = 30      # No puede empezar con numero
        my-name = "Dave"  # No guiones (Python piensa que es resta)
        my name = "Dave"  # No espacios
        class = "Python"  # No palabras clave de Python

CAMBIAR VARIABLES:
    puntuacion = 0
    puntuacion = 10
    puntuacion = puntuacion + 5  # Ahora es 15

CONVENCION PYTHON: snake_case (minusculas con guion bajo)
    first_name, user_age, shopping_cart_total""",
        "examples": [
            'nombre = "Alice"\nedad = 25\nprint(f"{nombre} tiene {edad} anos")',
            'total = 0\ntotal += 10\ntotal += 20\nprint(total)  # 30'
        ]
    },

    # --- TIPOS DE DATOS ---
    "numeros": {
        "keywords": ["numero", "numeros", "entero", "float", "integer", "decimal", "matematicas", "calcular", "suma", "resta", "multiplicacion", "division"],
        "title": "Numeros",
        "content": """Python tiene dos tipos de numeros:

ENTEROS (int) - numeros sin decimales:
    edad = 25
    puntuacion = -10

FLOTANTES (float) - numeros con decimales:
    precio = 19.99
    temperatura = -5.5
    pi = 3.14159

NOTA: Python usa punto (.) para decimales, NO coma!
    3.14 es correcto
    3,14 crea una tupla!

OPERACIONES MATEMATICAS:
    total = 10 + 5      # 15 - Suma
    cambio = 20 - 7     # 13 - Resta
    area = 6 * 4        # 24 - Multiplicacion
    mitad = 10 / 2      # 5.0 - Division (siempre float!)
    potencia = 5 ** 2   # 25 - Exponente

DIVISION ENTERA vs NORMAL:
    10 / 3   # 3.333... (float)
    10 // 3  # 3 (entero, redondea hacia abajo)

NUMEROS GRANDES: Python permite guion bajo para legibilidad:
    millon = 1_000_000  # Mejor que 1000000""",
        "examples": [
            'edad = 25\nprecio = 19.99\npi = 3.14159',
            'total = 10 + 5\narea = 6 * 4\npotencia = 2 ** 10',
            'resultado = 10 // 3   # Division entera: 3\nresultado = 10 / 3    # Division normal: 3.333...'
        ]
    },

    "cadenas_texto": {
        "keywords": ["string", "texto", "cadena", "cadena de texto", "cadenas", "strings", "letras", "caracteres", "comillas"],
        "title": "Cadenas de Texto (Strings)",
        "content": """Los strings son texto - cualquier caracter entre comillas.

CREAR STRINGS:
    nombre = "Alice"
    mensaje = 'Hola, Mundo!'

    # Tres comillas para multilinea:
    parrafo = ("Esto es\\n"
               "un string\\n"
               "multilinea")

COMBINAR STRINGS:
    nombre = "John"
    apellido = "Doe"
    nombre_completo = nombre + " " + apellido  # "John Doe"

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
        "keywords": ["boolean", "booleans", "bool", "verdadero", "falso", "true", "false", "true/false"],
        "title": "Booleans (Verdadero/Falso)",
        "content": """Los booleans solo pueden ser True o False - son como respuestas si/no.

CREAR BOOLEANS:
    esta_logueado = True
    es_admin = False
    tiene_permiso = True

IMPORTANTE: True y False con MAYUSCULA inicial!
    True  # Correcto
    true  # ERROR!
    TRUE  # ERROR!

BOOLEANS DE COMPARACION:
    edad = 18
    puede_votar = edad >= 18  # True

    puntaje = 75
    aprobo = puntaje > 60   # True

COMPARACIONES:
    ==   Igual a
    !=   No igual a
    >    Mayor que
    <    Menor que
    >=   Mayor o igual
    <=   Menor o igual

MEJOR PRACTICA:
    if esta_logueado:  # Mejor
        print("Bienvenido")

    if esta_logueado == True:  # Redundante
        print("Bienvenido")""",
        "examples": [
            'es_adulto = True\nprint(type(es_adulto))  # <class \'bool\'>',
            'edad = 25\npuede_votar = edad >= 18\nprint(puede_votar)  # True'
        ]
    },

    # --- ESTRUCTURAS DE DATOS ---
    "listas": {
        "keywords": ["lista", "listas", "array", "arreglo", "coleccion", "list", "indices", "indices de lista", "append", "agregar"],
        "title": "Listas",
        "content": """Las listas son la estructura de datos mas versatil de Python.

CREAR LISTAS:
    mi_lista = []
    frutas = ["manzana", "platano", "naranja"]
    numeros = [1, 2, 3, 4, 5]
    mixta = ["hola", 42, True, 3.14]

ACCEDER A ELEMENTOS (empieza en 0):
    frutas = ["manzana", "platano", "naranja"]
    frutas[0]   # "manzana"
    frutas[1]   # "platano"
    frutas[-1]  # "naranja" (ultimo)

MODIFICAR LISTAS:
    frutas = ["manzana", "platano", "naranja"]
    frutas[0] = "mango"
    frutas.append("uva")      # Agregar al final
    frutas.insert(1, "kiwi")  # Insertar en posicion
    frutas.remove("platano")  # Eliminar por valor
    ultimo = frutas.pop()     # Eliminar y devolver ultimo

METODOS UTILES:
    numeros = [3, 1, 4, 1, 5, 9]
    len(numeros)        # 6 (longitud)
    numeros.count(1)    # 2 (contar apariciones)
    numeros.index(4)    # 2 (buscar posicion)
    numeros.sort()      # Ordenar
    numeros.reverse()   # Invertir

VERIFICAR EXISTENCIA:
    if "manzana" in frutas:
        print("Encontrado!")""",
        "examples": [
            'frutas = ["manzana", "platano", "naranja"]\nfrutas.append("uva")\nprint(frutas)',
            'numeros = [1, 2, 3, 4, 5]\nfor num in numeros:\n    print(num)',
            'nombres = ["Ana", "Bob", "Charlie"]\nprint(len(nombres))  # 3'
        ]
    },

    "diccionarios": {
        "keywords": ["diccionario", "diccionarios", "dict", "key value", "clave valor", "clave-valor"],
        "title": "Diccionarios",
        "content": """Los diccionarios almacenan datos en pares clave-valor.

CREAR DICCIONARIOS:
    persona = {
        "nombre": "Alice",
        "edad": 30,
        "ciudad": "New York"
    }

    puntuaciones = dict(matematicas=95, ingles=87)

ACCEDER A VALORES:
    persona = {"nombre": "Alice", "edad": 30}
    print(persona["nombre"])          # "Alice"
    print(persona.get("trabajo"))     # None (sin error)
    print(persona.get("trabajo", "Desconocido"))  # "Desconocido"

MODIFICAR DICCIONARIOS:
    persona["email"] = "alice@email.com"  # Agregar nuevo
    persona["edad"] = 31                   # Actualizar
    del persona["email"]                   # Eliminar
    persona.pop("edad")                    # Eliminar y devolver

METODOS UTILES:
    persona.keys()    # Claves
    persona.values()  # Valores
    persona.items()   # Pares clave-valor

DICCIONARIOS ANIDADOS:
    estudiantes = {
        "alice": {"edad": 20, "nota": "A"},
        "bob": {"edad": 21, "nota": "B"}
    }
    print(estudiantes["alice"]["nota"])  # "A"

VERIFICAR CLAVE:
    if "nombre" in persona:
        print("Nombre encontrado!")""",
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
   单个元素 tupla necesita coma!
    single = (42,)  # Con coma es tupla
    no_tupla = (42)  # Sin coma es solo 42

ACCEDER A ELEMENTOS:
    punto = (3, 5)
    print(punto[0])      # 3
    print(punto[-1])     # 5

DESEMPAQUETAR TUPLAS (cool!):
    punto = (3, 5)
    x, y = punto  # x = 3, y = 5

    a, b, c = 1, 2, 3

    # Intercambiar variables:
    x, y = y, x  # Intercambia valores!

PARA QUE USAR TUPLAS:
    * Coordenadas (x, y)
    * Colores RGB (255, 0, 0)
    * Registros de base de datos
    * Valores de retorno de funciones""",
        "examples": [
            'punto = (3, 5)\nx, y = punto\nprint(f"X: {x}, Y: {y}")',
            'colores = ("rojo", "verde", "azul")\nfor color in colores:\n    print(color)'
        ]
    },

    "conjuntos": {
        "keywords": ["conjunto", "conjuntos", "set", "sets", "unico", "sin duplicados", "duplicados"],
        "title": "Conjuntos (Sets)",
        "content": """Los conjuntos solo almacenan valores UNICOS (sin duplicados).

CREAR CONJUNTOS:
    numeros = {1, 2, 3, 4, 5}
    frutas = set(["manzana", "platano", "naranja"])

    # De lista (elimina duplicados):
    notas = [85, 90, 85, 92, 90]
    notas_unicas = set(notas)  # {85, 90, 92}

    # Conjunto vacio: set() NO {} (eso es dict!)
    vacio = set()

OPERACIONES:
    colores = {"rojo", "azul"}
    colores.add("verde")      # Agregar
    colores.remove("azul")    # Eliminar (error si no existe)
    colores.discard("verde")  # Eliminar (sin error)

USOS COMUNES:
    # Eliminar duplicados:
    nombres = ["Ana", "Bob", "Ana", "Charlie", "Bob"]
    nombres_unicos = list(set(nombres))

    # Verificacion rapida:
    usuarios = {"alice", "bob", "charlie"}
    if "alice" in usuarios:  # Muy rapido!
        print("Acceso concedido")""",
        "examples": [
            'numeros = [1, 2, 2, 3, 3, 4]\nunicos = set(numeros)\nprint(unicos)  # {1, 2, 3, 4}',
            'colores = {"rojo", "azul", "verde"}\nprint("rojo" in colores)  # True'
        ]
    },

    # --- FLUJO DE CONTROL ---
    "if_statements": {
        "keywords": ["if", "si", "condicional", "condicion", "condicionales", "if else", "elif", "decision", "decisiones"],
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
    edad = 25
    tiene_licencia = True

    # AND - ambas deben ser verdaderas
    if edad >= 18 and tiene_licencia:
        print("Puedes conducir!")

    # OR - al menos una debe ser verdadera
    if es_finde or es_feriado:
        print("No hay trabajo!")

    # NOT - invierte el valor
    if not llueve:
        print("Salgamos!")

ANIDADOS:
    if tiene_boleto:
        if edad >= 18:
            print("Disfruta la pelicula!")
        else:
            print("Necesitas supervision adulta")
    else:
        print("Compra un boleto primero")""",
        "examples": [
            'edad = 20\nif edad >= 18:\n    print("Mayor de edad")\nelse:\n    print("Menor de edad")',
            'nota = 85\nif nota >= 90:\n    print("A")\nelif nota >= 80:\n    print("B")\nelse:\n    print("C")'
        ]
    },

    "loops": {
        "keywords": ["loop", "loops", "bucle", "bucles", "for", "while", "iterar", "repetir", "repetir codigo"],
        "title": "Bucles (Loops)",
        "content": """Los bucles permiten repetir codigo sin copiar y pegar.

FOR LOOP (el mas comun):
    # Repetir cierto numero de veces
    for i in range(5):
        print(i)  # 0, 1, 2, 3, 4

    # Contar desde 1
    for i in range(1, 6):
        print(i)  # 1, 2, 3, 4, 5

    # Contar de 2 en 2
    for i in range(0, 10, 2):
        print(i)  # 0, 2, 4, 6, 8

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
        contador += 1  # ¡Siempre actualizar!

IMPORTANTE: Asegurate de que el while termine!
    Si olvidas actualizar la variable, corre infinitamente!""",
        "examples": [
            'for i in range(5):\n    print(f"Hola {i+1} veces!")',
            'frutas = ["manzana", "platano", "naranja"]\nfor fruta in frutas:\n    print(fruta)',
            'numero = 1\nwhile numero <= 10:\n    print(numero)\n    numero += 1'
        ]
    },

    # --- POO ---
    "clases": {
        "keywords": ["clase", "clases", "object oriented", "orientado a objetos", "oop", "objeto", "objetos", "metodo", "atributo", "self", "init"],
        "title": "Clases (POO)",
        "content": """Las clases permiten organizar codigo agrupando datos y funciones relacionadas.

QUE ES UNA CLASE?
    # Sin clases - datos y funciones separados
    nombre = "MiBot"
    modelo = "GPT-4"

    def generar_respuesta(prompt):
        return "respuesta"

    # Con clases - todo junto
    class MiBot:
        def __init__(self, nombre, modelo):
            self.nombre = nombre
            self.modelo = modelo

        def generar_respuesta(self, prompt):
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

METODOS Y ATRIBUTOS:
    class Circulo:
        def __init__(self, radio):
            self.radio = radio  # Atributo

        def area(self):  # Metodo
            return 3.14 * self.radio ** 2

        def perimetro(self):  # Metodo
            return 2 * 3.14 * self.radio

HERENCIA (construir sobre clases existentes):
    class Animal:
        def __init__(self, nombre):
            self.nombre = nombre

        def hacer_sonido(self):
            print("Sonido generico")

    class Perro(Animal):
        def hacer_sonido(self):
            print("Guau!")

CUANDO USAR CLASES:
    * Interfaces a APIs
    * Pipelines de datos complejos
    * Componentes reutilizables
    * Operaciones con estado""",
        "examples": [
            'class Persona:\n    def __init__(self, nombre, edad):\n        self.nombre = nombre\n        self.edad = edad\n\n    def saludar(self):\n        print(f"Hola, soy {self.nombre}")',
            'class Circulo:\n    def __init__(self, radio):\n        self.radio = radio\n\n    def area(self):\n        return 3.14 * self.radio ** 2'
        ]
    },

    # --- MANEJO DE ERRORES ---
    "manejo_errores": {
        "keywords": ["error", "errores", "excepcion", "excepciones", "try", "except", "try except", "manejo de errores", "error handling"],
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
    except ZeroDivisionError:
        print("No se puede dividir por cero")

ELSE (solo si NO hubo error):
    try:
        archivo = open('datos.txt', 'r')
    except FileNotFoundError:
        print("No encontrado")
    else:
        print(f"Archivo tiene {len(datos)} caracteres")

FINALLY (siempre se ejecuta):
    try:
        archivo = open('datos.txt', 'r')
    finally:
        # Siempre se ejecuta
        print("Limpieza completa")

NO hagas esto:
    try:
        procesar_datos()
    except:
        pass  # Silenciar errores es MALO!""",
        "examples": [
            'try:\n    numero = int(input("Ingresa un numero: "))\nexcept ValueError:\n    print("Eso no es un numero valido")',
            'try:\n    resultado = 10 / 0\nexcept ZeroDivisionError:\n    print("No se puede dividir por cero")'
        ]
    },

    # --- ORGANIZACION ---
    "organizar_codigo": {
        "keywords": ["organizar", "modular", "imports", "importar", "archivos", "modulos", "helpers", "separar"],
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
    * Testeable - facil probar cada funcion por separado
    * Mantenible - cambios en un archivo no afectan todos""",
        "examples": [
            '# helpers.py\ndef calcular_total(cant, precio):\n    return cant * precio',
            '# main.py\nfrom helpers import calcular_total\ntotal = calcular_total(3, 15)\nprint(total)'
        ]
    },

    "primer_programa": {
        "keywords": ["primer", "primero", "hello world", "iniciar", "empezar", "instalar python", "vscode", "python file", "py"],
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
    * Ctrl+F5 (Windows) o Cmd+F5 (Mac)

SALIDA EN TERMINAL:
    Hola, Mundo!
    Estoy aprendiendo Python para IA

EL TERMINAL INTEGRADO:
    * Abre con Ctrl + ` (Windows) o Cmd + ` (Mac)
    * Puedes escribir comandos directamente
    * Usa flecha arriba para recordar comandos anteriores""",
        "examples": [
            'print("Hola, Mundo!")',
            'print("Estoy aprendiendo Python para IA")'
        ]
    },

    "por_que_python": {
        "keywords": ["por que python", "porque python", "por que aprender", "ventajas python", "beneficios python", "ia", "inteligencia artificial", "machine learning"],
        "title": "Por Que Python?",
        "content": """Python es el lenguaje dominante en IA y desarrollo:

VENTAJAS:
    * Facil de aprender - Python se lee como ingles
    * Librerias de IA - TensorFlow, PyTorch, scikit-learn
    * Estandar de la industria - Usado por todas las empresas de IA
    * Gran comunidad - Millones de desarrolladores

PYTHON EN IA:
    * Modelos de lenguaje (ChatGPT, Claude) - Transformers y redes neuronales
    * Vision por computadora (Tesla Autopilot) - OpenCV y PyTorch
    * Analisis de datos (Netflix) - pandas y NumPy
    * Machine Learning (Spotify) - scikit-learn y TensorFlow

MERCADO LABORAL:
    * Alta demanda: Desarrolladores Python IA ganan $130,000+
    * Trabajo remoto: Programa desde cualquier lugar
    * Campo creciente: 40% de crecimiento anual en empleos de IA""",
        "examples": []
    }
}

# ============================================================================
# FUNCIONES DE INTELIGENCIA DEL CHATBOT
# ============================================================================

def normalize(text):
    """Normaliza texto para mejor coincidencia."""
    text = text.lower().strip()
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ñ': 'n', 'ü': 'u'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def calculate_relevance(query, keywords):
    """Calcula que tan relevante es una pregunta para un tema."""
    query_norm = normalize(query)
    score = 0
    matched_keywords = []

    for keyword in keywords:
        keyword_norm = normalize(keyword)
        # Coincidencia exacta
        if keyword_norm in query_norm:
            score += 10
            matched_keywords.append(keyword)
        # Coincidencia parcial
        elif any(word in query_norm for word in keyword_norm.split()):
            score += 3
            matched_keywords.append(keyword)

    # Bonus por preguntas directas
    question_words = ["que es", "como", "cuando", "donde", "por que", "cual", "cuales", "explica", "enseña", "muestra", "ejemplo"]
    for word in question_words:
        if word in query_norm:
            score += 1

    return score, matched_keywords

def find_best_match(query):
    """Encuentra el mejor tema para una pregunta."""
    scores = {}

    for topic_id, topic in KNOWLEDGE_BASE.items():
        score, matched = calculate_relevance(query, topic["keywords"])
        if score > 0:
            scores[topic_id] = (score, matched)

    if not scores:
        return None, 0, []

    best_topic_id = max(scores, key=lambda x: scores[x][0])
    best_score, matched_keywords = scores[best_topic_id]
    return best_topic_id, best_score, matched_keywords

def detect_code_request(query):
    """Detecta si el usuario quiere ver codigo de ejemplo."""
    code_words = ["ejemplo", "codigo", "code", "mostrar", "enseña", "demuestra", "como se ve", "syntax", "sintaxis"]
    return any(word in normalize(query) for word in code_words)

def detect_quiz_request(query):
    """Detecta si el usuario quiere un quiz."""
    quiz_words = ["quiz", "examen", "prueba", "test", "evalua", "pregunta", "cuestionario"]
    return any(word in normalize(query) for word in quiz_words)

def generate_quiz(topic_id):
    """Genera un quiz basado en un tema."""
    quizzes = {
        "definir_funciones": {
            "question": "Quiz: Cual es la sintaxis correcta para definir una funcion en Python?",
            "options": [
                "A) function mi_funcion(): pass",
                "B) def mi_funcion(): pass",
                "C) func mi_funcion() pass",
                "D) define mi_funcion(): pass"
            ],
            "correct": "B",
            "explanation": "Correcto! Se usa 'def' seguido del nombre y parentesis. Ejemplo: def mi_funcion():"
        },
        "variables": {
            "question": "Quiz: Cual de estas es una variable valida en Python?",
            "options": [
                "A) 2nombre = 'Ana'",
                "B) mi-nombre = 'Ana'",
                "C) mi_nombre = 'Ana'",
                "D) my name = 'Ana'"
            ],
            "correct": "C",
            "explanation": "Correcto! Python usa snake_case: mi_nombre. No puede empezar con numero ni tener guiones/espacios."
        },
        "if_statements": {
            "question": "Quiz: Como se escribe una condicion 'else if' en Python?",
            "options": [
                "A) elseif",
                "B) else if",
                "C) elif",
                "D) elifse"
            ],
            "correct": "C",
            "explanation": "Correcto! En Python se usa 'elif' (abreviacion de else if)."
        },
        "listas": {
            "question": "Quiz: Como agregas un elemento al final de una lista?",
            "options": [
                "A) lista.add(elemento)",
                "B) lista.append(elemento)",
                "C) lista.insert(elemento)",
                "D) lista.push(elemento)"
            ],
            "correct": "B",
            "explanation": "Correcto! append() agrega al final. insert() requiere posicion."
        },
        "loops": {
            "question": "Quiz: Que imprime 'for i in range(3): print(i)'?",
            "options": [
                "A) 1, 2, 3",
                "B) 0, 1, 2",
                "C) 0, 1, 2, 3",
                "D) 1, 2"
            ],
            "correct": "B",
            "explanation": "Correcto! range(3) genera 0, 1, 2. Python empieza en 0!"
        }
    }

    if topic_id in quizzes:
        return quizzes[topic_id]
    return None

def get_related_topics(current_topic):
    """Sugiere temas relacionados."""
    relations = {
        "definir_funciones": ["parametros", "valores_retorno", "alcance_variables"],
        "parametros": ["definir_funciones", "valores_retorno"],
        "valores_retorno": ["definir_funciones", "parametros"],
        "variables": ["numeros", "cadenas_texto", "booleans"],
        "numeros": ["variables", "operadores"],
        "cadenas_texto": ["variables", "listas"],
        "booleans": ["if_statements", "variables"],
        "if_statements": ["booleans", "loops"],
        "loops": ["if_statements", "listas"],
        "listas": ["diccionarios", "loops", "tuplas"],
        "diccionarios": ["listas", "conjuntos"],
        "clases": ["funciones", "metodos"],
        "manejo_errores": ["funciones", "clases"]
    }

    if current_topic in relations:
        return relations[current_topic]
    return []

def format_response(topic_id):
    """Formatea la respuesta de un tema."""
    topic = KNOWLEDGE_BASE[topic_id]
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

    related = get_related_topics(topic_id)
    if related:
        response.append(f"\n{'─'*60}")
        response.append("  TEMAS RELACIONADOS:")
        for rel_id in related[:3]:
            if rel_id in KNOWLEDGE_BASE:
                response.append(f"    * {KNOWLEDGE_BASE[rel_id]['title']}")

    response.append(f"{'='*60}")
    return "\n".join(response)

def get_help_text():
    """Retorna texto de ayuda."""
    return """
╔══════════════════════════════════════════════════════════════╗
║           PYTHON CHATBOT - CURSO DATALUMINA                ║
╚══════════════════════════════════════════════════════════════╝

  COMANDOS:
    /ayuda     - Muestra esta ayuda
    /temas     - Lista todos los temas disponibles
    /quiz      - Inicia un quiz aleatorio
    /salir     - Sale del chatbot

  PUEDES PREGUNTAR SOBRE:
    * Funciones (def, parametros, return)
    * Variables y tipos de datos
    * Numeros, strings, booleans
    * Listas, diccionarios, tuplas, conjuntos
    * If statements y loops
    * Clases y POO
    * Manejo de errores (try/except)
    * Organizar codigo
    * Tu primer programa
    * Por que aprender Python

  EJEMPLOS DE PREGUNTAS:
    "Que son las funciones?"
    "Como creo una lista?"
    "Enseñame if statements"
    "Dame un ejemplo de loops"
    "Que es un diccionario?"
    "Como manejo errores en Python?"
    "Cual es la diferencia entre print y return?"
    "Como instalo Python?"

  Consejo: Puedes escribir en espanol natural!
"""

def get_topics_list():
    """Retorna lista de temas disponibles."""
    response = "\n  TEMAS DISPONIBLES:\n"
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
            if topic_id in KNOWLEDGE_BASE:
                response += f"    * {KNOWLEDGE_BASE[topic_id]['title']}\n"

    response += "\n  " + "─" * 40
    response += "\n  Escribe cualquier pregunta sobre estos temas!\n"
    return response

# ============================================================================
# ESTADO DE LA CONVERSACION
# ============================================================================

class ChatBotState:
    def __init__(self):
        self.current_topic = None
        self.conversation_history = []
        self.asked_quizzes = set()
        self.total_queries = 0
        self.topics_visited = set()

    def update(self, topic_id):
        self.current_topic = topic_id
        self.topics_visited.add(topic_id)
        self.total_queries += 1

# ============================================================================
# RESPUESTAS GENERALES
# ============================================================================

GENERIC_RESPONSES = {
    "greeting": [
        "Hola! Soy tu asistente de Python basado en el curso de Datalumina. Que te gustaria aprender?",
        "Bienvenido! Puedo ensenarte sobre Python. Que tema te interesa?",
        "Hola! Estoy aqui para ayudarte con Python. Preguntame lo que quieras!"
    ],
    "thanks": [
        "De nada! Si tienes mas preguntas, no dudes en preguntar.",
        "Para eso estoy! Hay algo mas que quieras aprender?",
        "Me alegra poder ayudar! Que mas te gustaria saber?"
    ],
    "goodbye": [
        "Hasta luego! Sigue practicando Python. Tu puedes!",
        "Nos vemos! Recuerda: practica hace al maestro.",
        "Adios! Que tengas un buen dia programando."
    ],
    "confused": [
        "No estoy seguro de entender. Puedes reformular tu pregunta?",
        "Hmm, no encontre un tema relacionado. Intenta preguntar sobre: funciones, variables, listas, loops, etc.",
        "No encontre eso en mi base de conocimiento. Escribe /temas para ver lo que puedo ensenarte."
    ],
    "about": [
        "Soy un chatbot educativo basado en el curso de Python de python.datalumina.com. Puedo ensenarte sobre funciones, variables, estructuras de datos, control de flujo, POO y mas!"
    ]
}

import random

def get_generic_response(category):
    return random.choice(GENERIC_RESPONSES.get(category, GENERIC_RESPONSES["confused"]))

# ============================================================================
# LOOP PRINCIPAL DEL CHATBOT
# ============================================================================

def main():
    state = ChatBotState()

    print("\n" + "╔" + "═"*58 + "╗")
    print("║" + " "*10 + "PYTHON CHATBOT INTELIGENTE" + " "*20 + "║")
    print("║" + " "*8 + "Basado en python.datalumina.com" + " "*19 + "║")
    print("║" + " "*14 + "Escribe /ayuda para comenzar" + " "*16 + "║")
    print("╚" + "═"*58 + "╝")
    print()

    while True:
        try:
            user_input = input("Tu > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n" + get_generic_response("goodbye"))
            break

        if not user_input:
            continue

        # Comandos especiales
        if user_input.lower() in ["/salir", "/exit", "/quit", "salir", "adios", "chao"]:
            print(get_generic_response("goodbye"))
            break

        if user_input.lower() in ["/ayuda", "/help", "ayuda", "help"]:
            print(get_help_text())
            continue

        if user_input.lower() in ["/temas", "/topics", "temas"]:
            print(get_topics_list())
            continue

        if user_input.lower() in ["/quiz", "quiz"]:
            topic_id = random.choice(list(KNOWLEDGE_BASE.keys()))
            quiz = generate_quiz(topic_id)
            if quiz:
                print(f"\n{quiz['question']}\n")
                for option in quiz['options']:
                    print(f"  {option}")
                print()
                answer = input("Tu respuesta (A/B/C/D): > ").strip().upper()
                if answer == quiz['correct']:
                    print(f"\n  ¡Correcto! {quiz['explanation']}")
                else:
                    print(f"\n  Incorrecto. {quiz['explanation']}")
            else:
                print("No hay quiz disponible para este tema.")
            continue

        # Detectar saludos
        greetings = ["hola", "buenas", "hey", "que tal", "como estas", "hi", "hello"]
        if any(greet in normalize(user_input) for greet in greetings):
            print(get_generic_response("greeting"))
            continue

        # Detectar agradecimientos
        thanks = ["gracias", "thanks", "te agradezco", "genial", "perfecto", "excelente"]
        if any(thank in normalize(user_input) for thank in thanks):
            print(get_generic_response("thanks"))
            continue

        # Detectar pregunta sobre el chatbot
        about_words = ["quien eres", "que eres", "que haces", "tu nombre", "sobre ti", "que puedes"]
        if any(word in normalize(user_input) for word in about_words):
            print(get_generic_response("about"))
            continue

        # Buscar mejor coincidencia
        topic_id, score, matched = find_best_match(user_input)

        if topic_id and score >= 5:
            state.update(topic_id)
            print(format_response(topic_id))

            # Detectar si pide quiz despues de ver el tema
            if detect_quiz_request(user_input):
                quiz = generate_quiz(topic_id)
                if quiz:
                    print(f"\n{quiz['question']}\n")
                    for option in quiz['options']:
                        print(f"  {option}")
                    print()
                    answer = input("Tu respuesta (A/B/C/D): > ").strip().upper()
                    if answer == quiz['correct']:
                        print(f"\n  ¡Correcto! {quiz['explanation']}")
                    else:
                        print(f"\n  Incorrecto. {quiz['explanation']}")
        else:
            # Intentar detectar intencion
            if detect_code_request(user_input):
                # Buscar cualquier tema con ejemplos
                for tid, topic in KNOWLEDGE_BASE.items():
                    if topic['examples'] and any(kw in normalize(user_input) for kw in topic['keywords']):
                        print(f"\nAqui tienes ejemplos de {topic['title']}:\n")
                        for i, ex in enumerate(topic['examples'], 1):
                            print(f"  Ejemplo {i}:")
                            print(textwrap.indent(ex, "    "))
                            print()
                        break
                else:
                    print(get_generic_response("confused"))
            else:
                print(get_generic_response("confused"))

if __name__ == "__main__":
    main()
