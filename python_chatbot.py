"""
Chatbot Inteligente by Monica
Busca en internet y responde SOLO en espanol.
"""

import sys
import textwrap
import random
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

# ============================================================================
# BUSQUEDA EN INTERNET
# ============================================================================

def search_web(query, num_results=5):
    """Busca en DuckDuckGo (funciona sin bloqueos)."""
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query + " espanol", max_results=num_results))
    except:
        try:
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=num_results))
        except:
            return []

def fetch_page(url, max_chars=2500):
    """Obtiene el contenido de una pagina web."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "button", "img", "iframe", "noscript"]):
            tag.decompose()

        for tag in soup.find_all(["p", "h1", "h2", "h3", "li", "td"]):
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
    """Busca en internet y retorna la informacion."""
    print("  Buscando...", end="\r")

    results = search_web(query, num_results=5)

    if results:
        for r in results:
            link = r.get("href", "")
            if link and "youtube.com" not in link and "twitter.com" not in link:
                content = fetch_page(link, max_chars=2500)
                if content and len(content) > 100:
                    print(" " * 20)
                    return f"\n{content}\n\n  Fuente: {link}"

    print(" " * 20)
    return None

# ============================================================================
# MAIN
# ============================================================================

def main():
    print()
    print("=" * 60)
    print("    Hola! Soy Monica, tu asistente inteligente")
    print("    Pregunta lo que sea y busco la respuesta")
    print("    Respondo SOLO en espanol")
    print("=" * 60)
    print()

    saludos = ["hola", "buenas", "hey", "que tal", "hi", "hello", "buenos dias", "buenas tardes"]
    despedidas = ["chao", "adios", "bye", "hasta luego", "nos vemos"]
    agradecimientos = ["gracias", "thanks", "genial", "perfecto", "excelente", "bien"]

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
            print("\n  Preguntame lo que quieras, busco la respuesta en internet.")
            print("  Escribe /salir para salir.\n")
            continue

        if any(s in user_lower for s in saludos):
            print(f"  {random.choice(['Hola! Que quieres saber?', 'Hey! Dime, en que te ayudo?', 'Hola! Preguntame lo que quieras.', 'Que tal! En que te puedo ayudar?'])}")
            continue

        if any(t in user_lower for t in agradecimientos):
            print(f"  {random.choice(['De nada! Algo mas?', 'Para eso estoy! Que mas necesitas?', 'Un placer! Algo mas que quieras saber?', 'Listo! Algo mas?'])}")
            continue

        result = smart_search(user_input)
        if result:
            print(result)
        else:
            print("  No encontre resultados. Intenta con otra pregunta.")

if __name__ == "__main__":
    main()
