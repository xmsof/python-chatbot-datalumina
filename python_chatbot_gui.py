"""
Chatbot Inteligente by Monica - Interfaz Grafica Premium
Potenciado por Groq + Llama 3.1 (gratis).
"""

import os
import sys
import random
import threading
import requests
import wikipedia
import tkinter as tk
from tkinter import font
from ddgs import DDGS

# ============================================================================
# CONFIGURACION
# ============================================================================

API_KEY = os.environ.get("GROQ_API_KEY", "")

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
# COLORES PREMIUM
# ============================================================================

C = {
    "bg_main": "#1a1a2e",
    "bg_header": "#16213e",
    "bg_chat": "#0f0f23",
    "bg_input": "#1a1a2e",
    "pink1": "#ff6b9d",
    "pink2": "#c44569",
    "pink3": "#e84393",
    "pink4": "#fd79a8",
    "pink_glow": "#ff9ff3",
    "user_msg": "#c44569",
    "ai_msg": "#2d2d44",
    "text_white": "#ffffff",
    "text_light": "#d4d4dc",
    "text_pink": "#ff6b9d",
    "border": "#2d2d44",
    "accent": "#e84393",
}

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

def ask_ai(query):
    try:
        context = search_context(query)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Contexto: {context}\nPregunta: {query}" if context else query}
        ]
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.1-8b-instant", "messages": messages, "max_tokens": 500},
            timeout=30
        )
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        return f"Error {r.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================================================
# INTERFAZ GRAFICA PREMIUM
# ============================================================================

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Monica AI")
        self.root.geometry("480x780")
        self.root.configure(bg=C["bg_main"])
        self.root.resizable(False, False)

        self.typing = False
        self.setup_fonts()
        self.create_header()
        self.create_chat_area()
        self.create_input_area()

        self.add_system("Hola! Soy Monica, tu asistente inteligente. Preguntame lo que quieras!")

    def setup_fonts(self):
        self.f_title = font.Font(family="Segoe UI", size=18, weight="bold")
        self.f_sub = font.Font(family="Segoe UI", size=9)
        self.f_chat = font.Font(family="Segoe UI", size=10)
        self.f_input = font.Font(family="Segoe UI", size=11)
        self.f_btn = font.Font(family="Segoe UI", size=12, weight="bold")

    def create_header(self):
        header = tk.Frame(self.root, bg=C["bg_header"], height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        top_line = tk.Frame(header, bg=C["pink1"], height=3)
        top_line.pack(fill="x", side="bottom")

        content = tk.Frame(header, bg=C["bg_header"])
        content.pack(expand=True)

        avatar = tk.Canvas(content, width=55, height=55, bg=C["bg_header"], highlightthickness=0)
        avatar.pack(side="left", padx=(20, 12), pady=10)
        avatar.create_oval(3, 3, 52, 52, fill=C["pink1"], outline=C["pink_glow"], width=2)
        avatar.create_text(28, 28, text="M", fill="white", font=("Segoe UI", 20, "bold"))

        text_frame = tk.Frame(content, bg=C["bg_header"])
        text_frame.pack(side="left", pady=10)

        tk.Label(text_frame, text="Monica", font=self.f_title,
                 bg=C["bg_header"], fg=C["text_white"], anchor="w").pack(anchor="w")
        tk.Label(text_frame, text="Asistente Inteligente", font=self.f_sub,
                 bg=C["bg_header"], fg=C["pink4"], anchor="w").pack(anchor="w")

        status = tk.Frame(content, bg=C["bg_header"])
        status.pack(side="right", padx=20, pady=10)
        dot = tk.Canvas(status, width=10, height=10, bg=C["bg_header"], highlightthickness=0)
        dot.pack(side="left", padx=(0, 5))
        dot.create_oval(1, 1, 9, 9, fill="#00d2d3", outline="")
        tk.Label(status, text="Online", font=("Segoe UI", 8),
                 bg=C["bg_header"], fg="#00d2d3").pack(side="left")

    def create_chat_area(self):
        container = tk.Frame(self.root, bg=C["bg_main"])
        container.pack(fill="both", expand=True, padx=8, pady=(8, 5))

        self.canvas = tk.Canvas(container, bg=C["bg_chat"], highlightthickness=0, bd=0)
        self.canvas.pack(side="left", fill="both", expand=True, padx=(0, 2))

        self.chat_frame = tk.Frame(self.canvas, bg=C["bg_chat"])
        self.window = self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")

        self.canvas.bind("<Configure>", self.on_resize)
        self.chat_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self.on_scroll)

    def on_resize(self, event):
        self.canvas.itemconfig(self.window, width=event.width)

    def on_scroll(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_bubble(self, text, is_user=False):
        wrapper = tk.Frame(self.chat_frame, bg=C["bg_chat"])
        wrapper.pack(fill="x", padx=12, pady=4)

        if is_user:
            bg = C["user_msg"]
            fg = C["text_white"]
            anchor = "e"
            pl, pr = 50, 5
            border_color = C["pink2"]
        else:
            bg = C["ai_msg"]
            fg = C["text_light"]
            anchor = "w"
            pl, pr = 5, 50
            border_color = C["border"]

        outer = tk.Frame(wrapper, bg=border_color, padx=1, pady=1)
        outer.pack(anchor=anchor, padx=(pl, pr))

        bubble = tk.Frame(outer, bg=bg, padx=14, pady=10)
        bubble.pack()

        label = tk.Label(bubble, text=text, font=self.f_chat, bg=bg, fg=fg,
                         wraplength=330, justify="left", anchor="w")
        label.pack()

        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1.0)

    def add_system(self, text):
        wrapper = tk.Frame(self.chat_frame, bg=C["bg_chat"])
        wrapper.pack(fill="x", padx=40, pady=6)

        bubble = tk.Frame(wrapper, bg=C["bg_main"], padx=12, pady=8)
        bubble.pack()

        tk.Label(bubble, text=text, font=("Segoe UI", 9), bg=C["bg_main"],
                 fg=C["pink4"], wraplength=350, justify="center").pack()

        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1.0)

    def show_typing(self):
        self.typing = True
        self.typing_frame = tk.Frame(self.chat_frame, bg=C["bg_chat"])
        self.typing_frame.pack(fill="x", padx=12, pady=4)

        outer = tk.Frame(self.typing_frame, bg=C["border"], padx=1, pady=1)
        outer.pack(anchor="w", padx=(5, 50))

        bubble = tk.Frame(outer, bg=C["ai_msg"], padx=14, pady=10)
        bubble.pack()

        self.typing_dots = []
        for i in range(3):
            dot = tk.Canvas(bubble, width=8, height=8, bg=C["ai_msg"], highlightthickness=0)
            dot.pack(side="left", padx=2)
            dot.create_oval(0, 0, 8, 8, fill=C["pink1"], outline="")
            self.typing_dots.append(dot)

        self.animate_dots(0)

    def animate_dots(self, idx):
        if not self.typing:
            return
        for i, dot in enumerate(self.typing_dots):
            color = C["pink_glow"] if i == idx % 3 else C["pink1"]
            dot.delete("all")
            dot.create_oval(0, 0, 8, 8, fill=color, outline="")
        self.root.after(300, self.animate_dots, idx + 1)

    def hide_typing(self):
        self.typing = False
        if hasattr(self, "typing_frame"):
            self.typing_frame.destroy()

    def create_input_area(self):
        input_frame = tk.Frame(self.root, bg=C["bg_input"], height=80)
        input_frame.pack(fill="x", side="bottom")
        input_frame.pack_propagate(False)

        line = tk.Frame(input_frame, bg=C["pink1"], height=2)
        line.pack(fill="x")

        container = tk.Frame(input_frame, bg=C["bg_input"])
        container.pack(fill="x", padx=12, pady=12)

        self.entry = tk.Entry(container, font=self.f_input, bg=C["bg_main"],
                              fg=C["text_white"], insertbackground=C["pink1"],
                              relief="flat", bd=0)
        self.entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))
        self.entry.bind("<Return>", self.send)
        self.entry.focus()

        btn = tk.Canvas(container, width=50, height=50, bg=C["bg_input"],
                        highlightthickness=0, cursor="hand2")
        btn.pack(side="right")
        btn.create_oval(2, 2, 48, 48, fill=C["pink1"], outline=C["pink3"], width=2)
        btn.create_text(25, 25, text=">", fill="white", font=("Segoe UI", 16, "bold"))
        btn.bind("<Button-1>", self.send)

    def send(self, event=None):
        text = self.entry.get().strip()
        if not text or self.typing:
            return
        self.entry.delete(0, "end")
        self.add_bubble(text, is_user=True)
        self.show_typing()
        threading.Thread(target=self.get_response, args=(text,), daemon=True).start()

    def get_response(self, query):
        response = ask_ai(query)
        self.root.after(0, self.on_response, response)

    def on_response(self, response):
        self.hide_typing()
        self.add_bubble(response, is_user=False)

# ============================================================================
# MAIN
# ============================================================================

def main():
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
