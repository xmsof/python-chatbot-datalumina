# Chatbot Inteligente by Monica

Asistente que busca informacion en internet para responder cualquier pregunta. Con base de conocimiento de Python de [python.datalumina.com](https://python.datalumina.com).

## Caracteristicas

- **Busqueda en internet** - Usa DuckDuckGo y Wikipedia para responder cualquier pregunta
- **Conocimiento local** - Base de datos completa de Python (19 temas)
- **Sin API keys** - Funciona gratis sin configuracion
- **Quiz interactivo** de Python
- **Busqueda directa** con comando /web

## Como funciona

1. Si la pregunta es sobre Python → responde con su base de conocimiento local
2. Si no es Python → busca en Wikipedia y DuckDuckGo
3. Tambien puedes usar `/web` para busquedas directas

## Requisitos

- Python 3.6 o superior
- Dependencias: `pip install requests duckduckgo-search wikipedia`

## Instalar dependencias

```bash
pip install requests duckduckgo-search wikipedia
```

## Uso

```bash
python python_chatbot.py
```

## Comandos

| Comando | Descripcion |
|---------|-------------|
| `/ayuda` | Muestra ayuda |
| `/temas` | Lista temas de Python |
| `/quiz` | Quiz aleatorio de Python |
| `/web` | Buscar algo en internet |
| `/salir` | Sale del chatbot |

## Ejemplos de preguntas

```
Que son las funciones?
Como creo una lista?
Que es la inteligencia artificial?
Quien es Elon Musk?
Como funciona Bitcoin?
Cual es la capital de Francia?
Explicame la fisica cuantica
/web mejores libros de programacion
```

## Licencia

MIT
