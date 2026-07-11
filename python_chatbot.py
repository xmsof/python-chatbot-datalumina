"""
Chatbot Inteligente by Monica
Busca en internet y da la informacion completa con fuente.
"""

import sys
import textwrap
import random
import requests
import wikipedia
from bs4 import BeautifulSoup
from ddgs import DDGS

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

def search_wikipedia(query, sentences=10):
    """Busca en Wikipedia en espanol."""
    try:
        wikipedia.set_lang("es")
        summary = wikipedia.summary(query, sentences=sentences, auto_suggest=True)
        page = wikipedia.page(query, auto_suggest=True)
        return summary, page.url, page.title
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            summary = wikipedia.summary(e.options[0], sentences=sentences, auto_suggest=False)
            page = wikipedia.page(e.options[0], auto_suggest=False)
            return summary, page.url, page.title
        except:
            return None, None, None
    except wikipedia.exceptions.PageError:
        return None, None, None
    except:
        return None, None, None

def fetch_web_content(url, max_chars=3000):
    """Obtiene el contenido de una pagina web."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "button", "img"]):
            tag.decompose()

        for tag in soup.find_all(["h1", "h2", "h3", "p", "li", "td", "th"]):
            tag.insert_before("\n")
            tag.insert_after("\n")

        text = soup.get_text(separator=" ")
        lines = [line.strip() for line in text.split("\n") if line.strip() and len(line.strip()) > 10]
        text = "\n".join(lines)

        text = " ".join(text.split())

        if len(text) > max_chars:
            sentences = text[:max_chars].rsplit(".", 1)
            if len(sentences) > 1:
                text = sentences[0] + "."
            else:
                text = text[:max_chars] + "..."

        return text
    except:
        return None

def smart_search(query):
    """Busqueda inteligente: Wikipedia primero, luego DuckDuckGo."""
    print("  Buscando...", end="\r")

    summary, url, title = search_wikipedia(query)
    if summary and len(summary) > 50:
        print(" " * 20)
        response = []
        response.append(f"\n{'='*60}")
        response.append(f"  {title}")
        response.append(f"{'='*60}")
        response.append("")
        response.append(textwrap.fill(summary, width=58))
        response.append("")
        response.append(f"  Fuente: {url}")
        response.append(f"{'='*60}")
        return "\n".join(response)

    results = search_internet(query, num_results=5)
    if results:
        print(" " * 20)

        for r in results:
            link = r.get("href", "")
            if link and ("wikipedia" in link.lower() or "wiki" in link.lower()):
                web_content = fetch_web_content(link, max_chars=4000)
                if web_content and len(web_content) > 100:
                    title = r.get("title", query)
                    response = []
                    response.append(f"\n{'='*60}")
                    response.append(f"  {title}")
                    response.append(f"{'='*60}")
                    response.append("")
                    response.append(textwrap.fill(web_content, width=58))
                    response.append("")
                    response.append(f"  Fuente: {link}")
                    response.append(f"{'='*60}")
                    return "\n".join(response)

        all_content = []
        sources = []
        for r in results[:3]:
            link = r.get("href", "")
            if link:
                web_content = fetch_web_content(link, max_chars=2000)
                if web_content and len(web_content) > 50:
                    all_content.append(web_content)
                    sources.append(link)

        if all_content:
            combined = " ".join(all_content)
            title = results[0].get("title", query)
            response = []
            response.append(f"\n{'='*60}")
            response.append(f"  {title}")
            response.append(f"{'='*60}")
            response.append("")
            response.append(textwrap.fill(combined[:4000], width=58))
            response.append("")
            if sources:
                response.append(f"  Fuente: {sources[0]}")
            response.append(f"{'='*60}")
            return "\n".join(response)

    print(" " * 20)
    return None

# ============================================================================
# UTILIDADES
# ============================================================================

def get_help():
    return """
============================================================
            CHATBOT INTELIGENTE BY MONICA
            Pregunta cualquier cosa
============================================================

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
  Te doy la informacion completa con la fuente.
"""

# ============================================================================
# MAIN
# ============================================================================

def main():
    print()
    print("=" * 60)
    print("    CHATBOT INTELIGENTE BY MONICA")
    print("    Pregunta cualquier cosa")
    print("    Busco la respuesta en internet")
    print("=" * 60)
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
