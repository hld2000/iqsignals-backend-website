from flask import Blueprint, jsonify
import datetime

# Creeăm blueprintul Flask pentru ruta /api/trader
trader = Blueprint('trader', __name__)

@trader.route('/', methods=['GET'])
def get_signals():
    """Returnează semnale demo generate automat"""
    now = datetime.datetime.utcnow().isoformat() + "Z"
    signals = [
        {"symbol": "BTC/USDT", "signal": "BUY", "price": 67890, "time": now},
        {"symbol": "ETH/USDT", "signal": "SELL", "price": 3520, "time": now},
        {"symbol": "BNB/USDT", "signal": "BUY", "price": 578, "time": now},
    ]
    return jsonify(signals)


