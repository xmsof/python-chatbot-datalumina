# Chatbot Inteligente by Monica

Asistente inteligente que responde CUALQUIER pregunta using Groq + Llama 3.1.

## Caracteristicas

- Responde como una IA real (como ChatGPT)
- Busca informacion en internet (Wikipedia, DuckDuckGo)
- Interfaz grafica rosa premium
- 100% gratis

## Como usar

### 1. Instalar Python

Descarga Python desde https://www.python.org/downloads/

### 2. Instalar dependencias

```bash
pip install requests ddgs wikipedia
```

### 3. Obtener API key gratis (Groq)

1. Ve a https://console.groq.com/keys
2. Crea una cuenta gratis
3. Dale a "Create API Key"
4. Copia la key

### 4. Configurar la API key

**Windows (PowerShell):**
```powershell
setx GROQ_API_KEY "tu-api-key-aqui"
```

**Mac/Linux:**
```bash
export GROQ_API_KEY="tu-api-key-aqui"
```

### 5. Ejecutar

**Version consola:**
```bash
python python_chatbot.py
```

**Version grafica (GUI):**
```bash
python python_chatbot_gui.py
```

## Ejemplos de preguntas

```
Que es una pizza?
Que es bitcoin?
Como funciona el internet?
Contame un chiste
Quien creo Python?
Receta de tacos al pastor
```

## Tecnologias

- Python 3.6+
- Groq API (Llama 3.1 8B)
- Wikipedia API
- DuckDuckGo Search
- Tkinter (GUI)

## Licencia

MIT
