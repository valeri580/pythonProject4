import os
import time
import random
import requests
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify

# ==== Пути ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "differ", "templates")

# ==== Flask ====
app = Flask(__name__, template_folder=TEMPLATES_DIR)

# ==== HTTP-сессия с ретраями ====
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(
    total=3,
    backoff_factor=0.7,  # 0.7, 1.4, 2.8 сек
    status_forcelist=[429, 500, 502, 503, 504],
    respect_retry_after_header=True,
)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)
session.headers.update({"User-Agent": "Flask-Quotes/EN-only"})

# ==== Источники цитат ====
API_URL = "https://quoteslate.vercel.app/api/quotes/random"

# ==== Кэш и дебаунс ====
CACHE_TTL = int(os.getenv("CACHE_TTL", "30"))  # сек
CALL_GAP = float(os.getenv("CALL_GAP", "1.2"))  # сек
_last_quote = None
_last_quote_at = None
_last_call_at = None

# ==== Локальные цитаты (фолбэк) ====
LOCAL_QUOTES = [
    ("Life is what happens while you are busy making other plans.", "John Lennon"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("In the middle of difficulty lies opportunity.", "Albert Einstein"),
    ("Stay hungry, stay foolish.", "Steve Jobs"),
    ("The secret of getting ahead is getting started.", "Mark Twain"),
]

# ==== Работа с QuoteSlate ====
def fetch_from_api():
    resp = session.get(API_URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict) and data.get("result"):
        q = data["result"][0]
        quote_text = (q.get("quote") or "").strip()
        author = (q.get("author") or "Unknown").strip()
        return {"quote": quote_text, "author": author, "source": "api"}
    raise RuntimeError("Unexpected API response")

def fetch_random_quote():
    """С кэшем, дебаунсом и фолбэком."""
    global _last_quote, _last_quote_at, _last_call_at

    now = time.monotonic()
    if _last_call_at and (now - _last_call_at) < CALL_GAP:
        if _last_quote and _last_quote_at and (datetime.utcnow() - _last_quote_at) < timedelta(seconds=CACHE_TTL):
            q = dict(_last_quote)
            q["source"] = "cache"
            return q
    _last_call_at = now

    if _last_quote and _last_quote_at and (datetime.utcnow() - _last_quote_at) < timedelta(seconds=CACHE_TTL):
        q = dict(_last_quote)
        q["source"] = "cache"
        return q

    try:
        q = fetch_from_api()
        _last_quote = {k: q[k] for k in ["quote", "author"]}
        _last_quote_at = datetime.utcnow()
        return q
    except requests.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        print("[quotes/api] http error:", status, e)
        if _last_quote:
            q = dict(_last_quote)
            q["source"] = "cache"
            return q
        quote, author = random.choice(LOCAL_QUOTES)
        return {"quote": quote, "author": author, "source": "local"}
    except Exception as e:
        print("[quotes/api] error:", e)
        if _last_quote:
            q = dict(_last_quote)
            q["source"] = "cache"
            return q
        quote, author = random.choice(LOCAL_QUOTES)
        return {"quote": quote, "author": author, "source": "local"}

# ==== Роуты ====
@app.route("/")
def index():
    try:
        first_quote = fetch_random_quote()
    except Exception as e:
        first_quote = {"quote": f"Load error: {e}", "author": "—", "source": "error"}
    return render_template("index.html", q=first_quote)

@app.route("/api/quote")
def api_quote():
    try:
        q = fetch_random_quote()
        return jsonify({"ok": True, "data": q})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 502

# ==== Запуск ====
if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(debug=True, port=port)
