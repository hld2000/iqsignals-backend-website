import os, time
from tinydb import TinyDB
from data_collector import fetch_ohlcv, add_features
from push_helper import list_subscriptions, send_push
DB_FILE = os.environ.get('AI_DB','ai_signals.json')
db = TinyDB(DB_FILE)
def generate_and_publish(symbol='BTC/USDT', timeframe='5m', auto_execute=False, user='demo', size_pct=0.001, mode='paper'):
    df = add_features(fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=200))
    latest = df.iloc[-1:]
    signal = 'BUY' if latest['sma10'].iloc[-1] > latest['sma50'].iloc[-1] else 'SELL'
    rec = {'symbol':symbol,'signal':signal,'confidence':0.5,'ts':time.time()}
    db.insert(rec)
    try:
        subs = list_subscriptions()
        for s in subs:
            send_push(s, {'title': f'{signal} {symbol}', 'body':'IQSIGNALS AI signal', 'url':'/'})
    except Exception:
        pass
    return rec
