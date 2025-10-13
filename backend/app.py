from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="IQSIGNALS API")

# Permitem accesul de oriunde (pentru frontend-ul mobil)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "IQSIGNALS backend is running 🚀"}

@app.get("/api/signal")
def get_signal():
    coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT"]
    actions = ["BUY", "SELL", "HOLD"]
    return {
        "pair": random.choice(coins),
        "signal": random.choice(actions),
        "confidence": round(random.uniform(0.6, 0.95), 2)
    }

@app.get("/api/status")
def status():
    return {"status": "online", "version": "1.0.0"}
