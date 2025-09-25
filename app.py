import os, requests
from flask import Flask, request, jsonify

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.post("/tg-webhook")
def tg_webhook():
    update = request.get_json(force=True, silent=True) or {}
    # Logs para Render
    print("Update recibido:", update)

    msg = update.get("message") or {}
    chat_id = (msg.get("chat") or {}).get("id")
    text = (msg.get("text") or "").strip()

    if not chat_id or not text:
        return jsonify({"ok": True})

    if text.lower() == "/start":
        reply = "👋 ¡Hola! Bot activo."
    else:
        reply = "Recibido ✅"

    r = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )
    print("Telegram status:", r.status_code, "body:", r.text)
    return jsonify({"ok": True})

@app.get("/healthz")
def healthz():
    return {"ok": True}
