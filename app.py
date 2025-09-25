import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")   # lo pones en Render
CHAT_ID        = os.getenv("CHAT_ID")          # lo pones en Render
TG_URL         = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/ping")
def ping():
    """Prueba: envía un mensaje de test al canal."""
    r = requests.post(TG_URL, json={"chat_id": CHAT_ID, "text": "Ping desde Render ✅"})
    return {"telegram_status": r.status_code, "telegram_body": r.text}

@app.post("/tradingview")
def tradingview():
    """Recibe alertas de TradingView y reenvía al canal."""
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
    # Logs útiles en Render
    print(">> Telegram status:", r.status_code)
    print(">> Telegram body:", r.text)
    return jsonify({"webhook_received": True, "telegram_status": r.status_code})
