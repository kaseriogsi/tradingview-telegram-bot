import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")   # lo pones en Render
CHAT_ID        = os.getenv("CHAT_ID")          # lo pones en Render

TG_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.post("/tradingview")
def tradingview():
    data = request.get_json(force=True)

    symbol = data.get("symbol", "BTCUSDT")
    side   = data.get("side", "?")
    entry  = data.get("entry")
    sl     = data.get("sl")
    tps    = data.get("tp", [])

    mensaje = f"""
⚡ Señal Scalping {symbol}
📈 Dirección: {side}
💰 Entrada: {entry}
🛑 Stop Loss: {sl}
🎯 Take Profits: {', '.join([str(tp) for tp in tps])}
"""

    requests.post(TG_URL, json={
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    })

    return jsonify({"ok": True})


@app.post("/tg-webhook")
def tg_webhook():
    update = request.get_json(force=True)
    print("Update recibido:", update)  # aparece en Logs de Render

    msg = update.get("message") or {}
    chat_id = msg.get("chat", {}).get("id")
    text = (msg.get("text") or "").strip().lower()

    if not chat_id or not text:
        return jsonify({"ok": True})

    if text == "/start":
        reply = "👋 ¡Hola! Estoy activo.\nUsa /help para ver opciones."
    elif text == "/help":
        reply = "🤖 Comandos:\n/start — comprobar que el bot está vivo\n/help — esta ayuda"
    else:
        reply = "Recibido ✅"

    r = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )
    print("Telegram status:", r.status_code, "body:", r.text)

    return jsonify({"ok": True})
