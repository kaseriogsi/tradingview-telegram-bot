import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")   # ej: 123456:ABC...
CHAT_ID        = os.getenv("CHAT_ID")          # tu ID personal (positivo) o @canal o -100...

TG_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.post("/tradingview")
def tradingview():
    data = request.get_json(force=True, silent=True) or {}
    symbol = data.get("symbol", "BTCUSDT")
    side   = data.get("side", "?")
    entry  = data.get("entry")
    sl     = data.get("sl")
    tps    = data.get("tp", [])

    msg = (
        f"⚡ Señal Scalping {symbol}\n"
        f"📈 Dirección: {side}\n"
        f"💰 Entrada: {entry}\n"
        f"🛑 Stop Loss: {sl}\n"
        f"🎯 Take Profits: {', '.join(map(str, tps))}\n"
    )

    r = requests.post(TG_URL, json={"chat_id": CHAT_ID, "text": msg})
    # ⬇⬇ LO IMPORTANTE: verás esto en Logs de Render
    print(">> Telegram status:", r.status_code)
    print(">> Telegram body:", r.text)

    return jsonify({
        "webhook_received": True,
        "telegram_status": r.status_code,
        "telegram_body": r.text
    })

@app.get("/ping")
def ping():
    r = requests.post(TG_URL, json={"chat_id": CHAT_ID, "text": "Ping desde Render ✅"})
    print(">> Ping status:", r.status_code)
    print(">> Ping body:", r.text)
    return {"telegram_status": r.status_code, "telegram_body": r.text}

@app.get("/healthz")
def healthz():
    return {"ok": True}