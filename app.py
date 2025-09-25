import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")   # tu token de @BotFather
CHAT_ID        = os.getenv("CHAT_ID")          # tu canal/grupo o tu chat personal
TG_URL         = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# ✅ Health check (para probar si el servicio está vivo)
@app.get("/healthz")
def healthz():
    return {"ok": True}

# ✅ Enviar un mensaje de prueba al canal/chat
@app.get("/ping")
def ping():
    r = requests.post(TG_URL, json={"chat_id": CHAT_ID, "text": "Ping desde Render ✅"})
    print(">> Ping status:", r.status_code, "body:", r.text)
    return {"telegram_status": r.status_code, "telegram_body": r.text}

# ✅ Recibir alertas de TradingView y reenviar a Telegram
@app.post("/tradingview")
def tradingview():
    data = request.get_json(force=True, silent=True) or {}
    symbol = data.get("symbol", "BTCUSDT")
    side   = data.get("side", "?")
    entry  = data.get("entry")
    sl     = data.get("sl")
    tps    = data.get("tp", [])

    msg = (
        f"⚡ Señal {symbol}\n"
        f"➡ Dirección: {side}\n"
        f"💰 Entrada: {entry}\n"
        f"🛑 Stop: {sl}\n"
        f"🎯 TPs: {', '.join(map(str, tps))}\n"
    )

    r = requests.post(TG_URL, json={"chat_id": CHAT_ID, "text": msg})
    print(">> TradingView status:", r.status_code, "body:", r.text)
    return jsonify({"webhook_received": True, "telegram_status": r.status_code})

# ✅ Webhook de Telegram (para que el bot responda a /start en privado)
@app.post("/tg-webhook")
def tg_webhook():
    update = request.get_json(force=True, silent=True) or {}
    print("Update recibido:", update)

    msg = update.get("message") or {}
    chat_id = (msg.get("chat") or {}).get("id")
    text = (msg.get("text") or "").strip().lower()

    if not chat_id or not text:
        return jsonify({"ok": True})

    if text == "/start":
        reply = "👋 ¡Hola! Bot activo.\nUsa /help para ver opciones."
    elif text == "/help":
        reply = "🤖 Comandos:\n/start — comprobar que el bot está vivo\n/help — esta ayuda"
    else:
        reply = "Recibido ✅"

    r = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )
    print(">> Reply status:", r.status_code, "body:", r.text)
    return jsonify({"ok": True})

