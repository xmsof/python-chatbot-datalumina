"""
Chatbot Inteligente by Monica
Respuestas cortas, claras y en espanol.
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

PAGES_TO_SKIP = ["dictionary", "cambridge", "wordreference", "spanishdict",
                 "reverso", "larousse", "wiktionary", "merriam", "oxford",
                 "youtube.com", "twitter.com", "facebook.com", "instagram",
                 "tiktok", "pinterest", "amazon", "mercadolibre"]

def search_web(query):
    """Busca en DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=8))
            filtered = []
            for r in results:
                link = r.get("href", "")
                if not any(skip in link.lower() for skip in PAGES_TO_SKIP):
                    filtered.append(r)
            return filtered
    except:
        return []

def fetch_page(url, max_chars=2000):
    """Obtiene contenido limpio de una pagina."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header",
                         "aside", "form", "button", "img", "iframe",
                         "noscript", "svg", "figure", "figcaption"]):
            tag.decompose()

        paragraphs = []
        for p in soup.find_all(["p", "h2", "h3"]):
            text = p.get_text(strip=True)
            if len(text) > 30:
                paragraphs.append(text)

        content = " ".join(paragraphs)

        if len(content) > max_chars:
            content = content[:max_chars].rsplit(".", 1)[0] + "."

        return content
    except:
        return None

def smart_search(query):
    """Busca y retorna informacion clara."""
    print("  Buscando...", end="\r")

    results = search_web(query)

    for r in results:
        link = r.get("href", "")
        body = r.get("body", "")
        title = r.get("title", "")

        if body and len(body) > 40:
            content = fetch_page(link, max_chars=1500)
            if content and len(content) > 80:
                print(" " * 20)
                clean = clean_response(content, query)
                return f"\n  {clean}\n\n  Fuente: {link}"

    print(" " * 20)
    return None

def clean_response(text, query):
    """Limpia y acorta la respuesta."""
    text = text.replace("[1]", "").replace("[2]", "").replace("[3]", "")
    text = text.replace("[4]", "").replace("[5]", "").replace("[6]", "")
    text = text.replace("[editar]", "").replace("Ir al contenido", "")
    text = text.replace("De Wikipedia, la enciclopedia libre", "")
    text = text.replace("Wikipedia", "").strip()

    sentences = text.split(".")
    relevant = []
    for s in sentences:
        s = s.strip()
        if len(s) > 20:
            relevant.append(s)
        if len(".".join(relevant)) > 800:
            break

    return ". ".join(relevant) + "." if relevant else text[:800]

# ============================================================================
# MAIN
# ============================================================================

def main():
    print()
    print("=" * 60)
    print("  Hola! Soy Monica, tu asistente inteligente")
    print("  Preguntame lo que quieras")
    print("  Respondo SOLO en espanol")
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
            print("  Hasta luego!")
            break

        if user_lower in ["/ayuda", "/help"]:
            print("\n  Preguntame lo que quieras!")
            print("  Escribe /salir para salir.\n")
            continue

        if any(s in user_lower for s in saludos):
            print(f"  {random.choice(['Hola! Que quieres saber?', 'Hey! Dime, en que te ayudo?', 'Hola! Preguntame lo que quieras.', 'Que tal! En que te puedo ayudar?'])}")
            continue

        if any(t in user_lower for t in agradecimientos):
            print(f"  {random.choice(['De nada! Algo mas?', 'Para eso estoy!', 'Un placer!', 'Listo! Algo mas?'])}")
            continue

        result = smart_search(user_input)
        if result:
            print(result)
        else:
            print("  No encontre resultados. Intenta con otra pregunta.")

if __name__ == "__main__":
    main()
