# Chatbot Inteligente by Monica

Asistente de Python potenciado por DeepSeek API. Basado en el curso de [python.datalumina.com](https://python.datalumina.com).

## Caracteristicas

- **Potenciado por DeepSeek API** - Responde CUALQUIER pregunta de Python
- **Base de conocimiento local** - Temas del curso de Datalumina
- **Quiz interactivo** para practicar
- **Historial de conversacion** - Recuerda el contexto
- **Sin API** - Funciona con temas basicos sin API key

## Temas del curso

| Categoria | Temas |
|-----------|-------|
| Funciones | Definir funciones, Parametros, Valores de retorno |
| Variables | Variables, Numeros, Strings, Booleans |
| Estructuras | Listas, Diccionarios, Tuplas, Conjuntos |
| Control | If statements, Loops |
| POO | Clases |
| Errores | Try/Except |

## Requisitos

- Python 3.6 o superior
- requests (`pip install requests`)
- API key de DeepSeek (opcional pero recomendado)

## Obtener API Key de DeepSeek

1. Ve a [platform.deepseek.com](https://platform.deepseek.com/)
2. Crea una cuenta gratis
3. Ve a "API Keys" y crea una nueva clave
4. Copia la clave

## Configurar API Key

### Opcion 1: Variable de entorno (recomendado)

```powershell
# Windows
setx DEEPSEEK_API_KEY "tu-api-key-aqui"

# Mac/Linux
export DEEPSEEK_API_KEY="tu-api-key-aqui"
```

### Opcion 2: Ingresa al iniciar

El chatbot te pedira la API key si no esta configurada.

## Instalar dependencias

```bash
pip install requests
```

## Uso

```bash
python python_chatbot.py
```

## Comandos

| Comando | Descripcion |
|---------|-------------|
| `/ayuda` | Muestra ayuda |
| `/temas` | Lista todos los temas |
| `/quiz` | Quiz aleatorio |
| `/limpiar` | Limpia historial |
| `/salir` | Sale del chatbot |

## Ejemplos de preguntas

```
Que son las funciones?
Como creo una lista?
Enseñame if statements
Que es un diccionario?
Dame un ejemplo de loops
Como manejo errores en Python?
Explicame decoradores
Que son las list comprehension?
Como uso la API de requests?
```

## Licencia

MIT
