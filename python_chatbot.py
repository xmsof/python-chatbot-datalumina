"""
Chatbot Inteligente by Monica - Consola
Potenciado por Groq + Llama 3.1 (gratis).
"""

import os
import sys
import json
import random
import requests
import wikipedia
from ddgs import DDGS

# ============================================================================
# CONFIGURACION
# ============================================================================

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_api_key():
    key = os.environ.get("GROQ_API_KEY", "")
    if key:
        return key
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("api_key", "")
    return ""

def save_api_key(key):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"api_key": key}, f)

SYSTEM_PROMPT = """Eres Monica, una asistente inteligente, amigable y conversacional.

Reglas:
- Responde SOLO en espanol
- Se concisa pero completa (maximo 4-5 oraciones)
- Habla de forma natural y amigable
- Si te preguntan algo, responde directamente
- No des listas largas ni texto crudo
- Incluye datos interesantes cuando sea relevante
- Si no sabes algo, di la verdad pero intenta ayudar
- Usa emojis moderadamente
- Responde como lo haria ChatGPT o cualquier IA moderna"""

# ============================================================================
# BUSQUEDA EN INTERNET
# ============================================================================

def search_context(query):
    try:
        wikipedia.set_lang("es")
        return wikipedia.summary(query, sentences=4, auto_suggest=True, redirect=True)
    except:
        pass
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            for r in results:
                body = r.get("body", "")
                if body and len(body) > 50:
                    return body
    except:
        pass
    return None

# ============================================================================
# GROQ API
# ============================================================================

def ask_ai(query, api_key):
    try:
        context = search_context(query)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Contexto: {context}\nPregunta: {query}" if context else query}
        ]
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "llama-3.1-8b-instant", "messages": messages, "max_tokens": 500},
            timeout=30
        )
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        return f"Error {r.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================================================
# MAIN
# ============================================================================

def main():
    print()
    print("=" * 60)
    print("  Hola! Soy Monica, tu asistente inteligente")
    print("  Preguntame lo que quieras")
    print("=" * 60)
    print()

    api_key = load_api_key() or "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"

    if not api_key:
        print("  Necesitas una API key gratis de Groq.")
        print("  Ve a: https://console.groq.com/keys")
        print()
        api_key = input("  Ingresa tu API key: > ").strip()
        if not api_key:
            print("\n  Saliendo...")
            return
        save_api_key(api_key)
        print("  Key guardada! Ya no te la pedire otra vez.")
        print()

    print("  Listo! Preguntame lo que quieras.")
    print()

    saludos = ["hola", "buenas", "hey", "que tal", "hi", "hello"]
    despedidas = ["chao", "adios", "bye", "hasta luego"]
    gracias = ["gracias", "thanks", "genial", "perfecto"]

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

        if any(s in user_lower for s in saludos):
            print(f"  {random.choice(['Hola! Que quieres saber?', 'Hey! Dime, en que te ayudo?', 'Hola! Preguntame lo que quieras.'])}")
            continue

        if any(t in user_lower for t in gracias):
            print(f"  {random.choice(['De nada! Algo mas?', 'Para eso estoy!', 'Un placer!'])}")
            continue

        print("  Pensando...", end="\r")
        response = ask_ai(user_input, api_key)
        print(" " * 20)
        print(f"\n  Monica > {response}\n")

if __name__ == "__main__":
    main()
