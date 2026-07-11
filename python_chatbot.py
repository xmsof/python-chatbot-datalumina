"""
Chatbot Inteligente by Monica
Responde CUALQUIER pregunta buscando en internet.
"""

import sys
import textwrap
import random
import wikipedia
from duckduckgo_search import DDGS

# ============================================================================
# BUSQUEDA EN INTERNET
# ============================================================================

def search_internet(query, num_results=5):
    """Busca en DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=num_results))
    except:
        return []

def search_wikipedia(query, sentences=4):
    """Busca en Wikipedia en espanol."""
    try:
        wikipedia.set_lang("es")
        summary = wikipedia.summary(query, sentences=sentences, auto_suggest=True)
        page = wikipedia.page(query, auto_suggest=True)
        return summary, page.url
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            summary = wikipedia.summary(e.options[0], sentences=sentences, auto_suggest=False)
            page = wikipedia.page(e.options[0], auto_suggest=False)
            return summary, page.url
        except:
            return None, None
    except:
        return None, None

def smart_search(query):
    """Busqueda inteligente: Wikipedia primero, luego DuckDuckGo."""
    print("  Buscando...", end="\r")

    summary, url = search_wikipedia(query)
    if summary and len(summary) > 50:
        print(" " * 20)
        response = []
        response.append(f"\n{'='*60}")
        response.append(f"  {query.title()}")
        response.append(f"{'='*60}")
        response.append("")
        response.append(textwrap.fill(summary, width=58))
        response.append("")
        if url:
            response.append(f"  Mas info: {url}")
        response.append(f"{'='*60}")
        return "\n".join(response)

    results = search_internet(query, num_results=5)
    if results:
        print(" " * 20)
        response = []
        response.append(f"\n{'='*60}")
        response.append(f"  Resultados para: {query}")
        response.append(f"{'='*60}")

        for i, r in enumerate(results[:5], 1):
            title = r.get("title", "Sin titulo")
            body = r.get("body", "Sin descripcion")
            link = r.get("href", "")
            response.append(f"\n  {i}. {title}")
            if len(body) > 250:
                body = body[:250] + "..."
            response.append(f"     {body}")
            if link:
                response.append(f"     {link}")

        response.append(f"\n{'='*60}")
        return "\n".join(response)

    print(" " * 20)
    return None

# ============================================================================
# UTILIDADES
# ============================================================================

def get_help():
    return """
╔══════════════════════════════════════════════════════════════╗
║            CHATBOT INTELIGENTE BY MONICA                     ║
║            Pregunta cualquier cosa                           ║
╚══════════════════════════════════════════════════════════════╝

  COMANDOS:
    /ayuda    - Muestra esta ayuda
    /web      - Busqueda directa en internet
    /salir    - Salir

  EJEMPLOS:
    "Que es la inteligencia artificial?"
    "Quien creo Python?"
    "Como funciona el blockchain?"
    "Cual es la capital de Japon?"
    "Explicame la relatividad"
    "Mejores peliculas de 2024"
    "Receta de tacos al pastor"
    /web noticias de hoy
    /web programacion en python

  Puedes preguntar LO QUE SEA!
"""

# ============================================================================
# MAIN
# ============================================================================

def main():
    print()
    print("╔" + "═"*58 + "╗")
    print("║" + " "*12 + "CHATBOT INTELIGENTE BY MONICA" + " "*16 + "║")
    print("║" + " "*14 + "Pregunta cualquier cosa" + " "*20 + "║")
    print("║" + " "*12 + "Busco la respuesta en internet" + " "*15 + "║")
    print("╚" + "═"*58 + "╝")
    print()
    print("  Escribe tu pregunta y buscare la respuesta.")
    print("  Escribe /ayuda para ver los comandos.")
    print()

    while True:
        try:
            user_input = input("Tu > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Hasta luego!")
            break

        if not user_input:
            continue

        if user_input.lower() in ["/salir", "/exit", "salir", "adios", "chao"]:
            print("  Hasta luego!")
            break

        if user_input.lower() in ["/ayuda", "/help", "ayuda", "help"]:
            print(get_help())
            continue

        if user_input.lower().startswith("/web "):
            query = user_input[5:].strip()
            if query:
                result = smart_search(query)
                if result:
                    print(result)
                else:
                    print("  No encontre nada. Intenta con otra busqueda.")
            else:
                print("  Usa: /web seguido de lo que quieras buscar")
            continue

        result = smart_search(user_input)
        if result:
            print(result)
        else:
            print("  No encontre resultados para esa pregunta.")
            print("  Intenta reformular o usa /web seguido de tu busqueda.")

if __name__ == "__main__":
    main()
