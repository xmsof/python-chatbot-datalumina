"""
Chatbot Inteligente by Monica
Busca en Google, Wikipedia y DuckDuckGo.
Respuestas concisas y conversacionales.
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

def search_google(query, num_results=5):
    """Busca en Google."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(f"https://www.google.com/search?q={query}&hl=es", headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        for g in soup.select("div.BNeawe"):
            text = g.get_text()
            if len(text) > 20 and len(text) < 500:
                results.append({"title": text, "body": text, "href": ""})

        if not results:
            for g in soup.select("div"):
                text = g.get_text(strip=True)
                if len(text) > 30 and len(text) < 300 and query.lower().split()[0] in text.lower():
                    results.append({"title": text[:100], "body": text, "href": ""})

        return results[:num_results]
    except:
        return []

def search_duckduckgo(query, num_results=5):
    """Busca en DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=num_results))
    except:
        return []

def search_wikipedia_es(query, sentences=8):
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
    except:
        return None, None, None

def fetch_page_content(url, max_chars=2500):
    """Obtiene contenido limpio de una pagina web."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "button", "img", "iframe"]):
            tag.decompose()

        for tag in soup.find_all(["p", "h1", "h2", "h3", "li"]):
            tag.insert_before("\n")
            tag.insert_after("\n")

        text = soup.get_text(separator=" ")
        lines = [line.strip() for line in text.split("\n") if line.strip() and len(line.strip()) > 15]
        text = " ".join(lines)

        if len(text) > max_chars:
            text = text[:max_chars].rsplit(".", 1)[0] + "."

        return text
    except:
        return None

def smart_search(query):
    """Busqueda inteligente: Google > Wikipedia > DuckDuckGo."""
    print("  Buscando...", end="\r")

    clean_query = query
    prefixes = ["que es", "que son", "como funciona", "quien es", "quien fue", "cuál es", "cuales son"]
    for prefix in prefixes:
        if clean_query.lower().startswith(prefix):
            clean_query = clean_query[len(prefix):].strip()
            break

    summary, url, title = search_wikipedia_es(clean_query)
    if summary and len(summary) > 80:
        print(" " * 20)
        short = textwrap.fill(summary[:2000], width=58)
        return f"\n  {title}\n\n{short}\n\n  Fuente: {url}"

    summary, url, title = search_wikipedia_es(query)
    if summary and len(summary) > 80:
        print(" " * 20)
        short = textwrap.fill(summary[:2000], width=58)
        return f"\n  {title}\n\n{short}\n\n  Fuente: {url}"

    ddg_results = search_duckduckgo(query, num_results=5)
    for r in ddg_results:
        link = r.get("href", "")
        if link:
            content = fetch_page_content(link, max_chars=2500)
            if content and len(content) > 100:
                t = r.get("title", query)
                short = textwrap.fill(content[:2000], width=58)
                return f"\n  {t}\n\n{short}\n\n  Fuente: {link}"

    print(" " * 20)
    return None

# ============================================================================
# UTILIDADES
# ============================================================================

def get_help():
    return """
============================================================
        CHATBOT INTELIGENTE BY MONICA
============================================================

  Comandos:
    /ayuda    - Ayuda
    /web      - Buscar en internet
    /salir    - Salir

  Pregunta lo que sea, busco la respuesta!
"""

# ============================================================================
# MAIN
# ============================================================================

def main():
    print()
    print("=" * 60)
    print("    Hola! Soy Monica")
    print("    Pregunta lo que sea y busco la respuesta")
    print("=" * 60)
    print()

    saludos = ["hola", "buenas", "hey", "que tal", "hi", "hello"]
    despedidas = ["chao", "adios", "bye", "hasta luego"]

    while True:
        try:
            user_input = input("Tu > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Hasta luego!")
            break

        if not user_input:
            continue

        user_lower = user_input.lower()

        if user_lower in ["/salir", "/exit"] + despedidas:
            print("  Hasta luego! Fue un placer ayudarte.")
            break

        if user_lower in ["/ayuda", "/help", "ayuda", "help"]:
            print(get_help())
            continue

        if any(s in user_lower for s in saludos):
            respuestas = [
                "Hola! Que gustaria saber?",
                "Hey! En que te puedo ayudar?",
                "Hola! Preguntame lo que quieras.",
                "Que tal! Dime, que necesitas?"
            ]
            print(f"  {random.choice(respuestas)}")
            continue

        if any(t in user_lower for t in ["gracias", "thanks", "genial", "perfecto"]):
            respuestas = [
                "De nada! Algo mas?",
                "Para eso estoy! Que mas necesitas?",
                "Un placer ayudarte! Algo mas?",
                "Listo! Algo mas que quieras saber?"
            ]
            print(f"  {random.choice(respuestas)}")
            continue

        if user_lower.startswith("/web "):
            query = user_input[5:].strip()
            if query:
                result = smart_search(query)
                if result:
                    print(result)
                else:
                    print("  No encontre nada. Intenta con otra busqueda.")
            else:
                print("  Usa: /web seguido de lo que buscas")
            continue

        result = smart_search(user_input)
        if result:
            print(result)
        else:
            print("  No encontre resultados.")
            print("  Intenta reformular o usa /web seguido de tu busqueda.")

if __name__ == "__main__":
    main()
