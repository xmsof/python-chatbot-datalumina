"""
Chatbot Inteligente by Monica
Potenciado por Groq + Llama 3.1 (gratis).
"""

import os
import sys
import random
import requests
import wikipedia
from ddgs import DDGS

# ============================================================================
# CONFIGURACION
# ============================================================================

SYSTEM_PROMPT = """Eres Monica, una asistente inteligente, amigable y conversacional.

Reglas:
- Responde SOLO en espanol
- Se concisa pero completa (maximo 4-5 oraciones)
- Habla de forma natural y amigable
- Si te preguntan algo, responde directamente
- No des listas largas ni texto crudo
- Incluye datos interesantes cuando sea relevante
- Si no sabes algo, di la verdad pero intenta ayudar
- Usa emojis moderadamente para hacer la conversacion mas amena
- Responde como lo haria ChatGPT o cualquier IA moderna"""

# ============================================================================
# BUSQUEDA EN INTERNET (para contexto)
# ============================================================================

def search_context(query):
    """Busca informacion en internet para dar contexto."""
    try:
        wikipedia.set_lang("es")
        summary = wikipedia.summary(query, sentences=4, auto_suggest=True, redirect=True)
        return summary
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
# GROQ API (Llama 3.1)
# ============================================================================

def ask_ai(query, api_key):
    """Pregunta a Groq (Llama 3.1)."""
    try:
        context = search_context(query)
        if context:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Contexto de internet: {context}\n\nPregunta: {query}"}
            ]
        else:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query}
            ]

        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": "llama-3.1-8b-instant", "messages": messages, "max_tokens": 500},
            timeout=30
        )

        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"Error {r.status_code}: {r.json().get('error', {}).get('message', 'Desconocido')}"
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

    api_key = os.environ.get("GROQ_API_KEY", "")

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
