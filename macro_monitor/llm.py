"""Cliente LLM con dos proveedores: Groq (principal) y Google Gemini (respaldo gratuito con límites holgados).

chat(system, user, max_tokens) -> texto o None. Orden: Groq (120b, 20b) con reintento ante 413/429;
si falla y hay GEMINI_API_KEY, Gemini (gemini-2.5-flash). LLM_PROVIDER=gemini invierte el orden.
"""
import os
import time
import requests

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash"]


def _groq(system, user, max_tokens, temperature, wait_on_limit):
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return None
    for model in GROQ_MODELS:
        for intento in (1, 2):
            try:
                r = requests.post(GROQ_URL, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                                  json={"model": model, "temperature": temperature, "max_tokens": max_tokens, "reasoning_effort": "low",
                                        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]},
                                  timeout=90)
                if r.status_code in (413, 429) and intento == 1 and wait_on_limit:
                    print(f"(groq {model}: {r.status_code} {r.text[:120]!r}; espero {wait_on_limit} s)")
                    time.sleep(wait_on_limit)
                    continue
                r.raise_for_status()
                txt = r.json()["choices"][0]["message"]["content"].strip()
                if txt:
                    print(f"(llm: groq {model})")
                    return txt
                break
            except Exception as e:  # noqa: BLE001
                print(f"(groq {model}: {e})")
                break
    return None


def _gemini(system, user, max_tokens, temperature):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    for model in GEMINI_MODELS:
        try:
            r = requests.post(GEMINI_URL.format(model=model), params={"key": key}, timeout=120,
                              json={"systemInstruction": {"parts": [{"text": system}]},
                                    "contents": [{"role": "user", "parts": [{"text": user}]}],
                                    "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens}})
            r.raise_for_status()
            cands = r.json().get("candidates", [])
            txt = "".join(p.get("text", "") for p in cands[0]["content"]["parts"]).strip() if cands else ""
            if txt:
                print(f"(llm: gemini {model})")
                return txt
        except Exception as e:  # noqa: BLE001
            print(f"(gemini {model}: {e})")
    return None


def chat(system: str, user: str, max_tokens: int = 2000, temperature: float = 0.3, wait_on_limit: int = 65) -> str | None:
    order = ["gemini", "groq"] if os.environ.get("LLM_PROVIDER", "").lower() == "gemini" else ["groq", "gemini"]
    for prov in order:
        txt = _groq(system, user, max_tokens, temperature, wait_on_limit) if prov == "groq" else _gemini(system, user, max_tokens, temperature)
        if txt:
            return txt
    return None
