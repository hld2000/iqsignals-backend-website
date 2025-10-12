import time, random, os
from tinydb import TinyDB, Query
DB_FILE = os.environ.get('PAPER_DB', 'paper_trades.json')
db = TinyDB(DB_FILE)
acct_table = db.table('accounts')
orders_table = db.table('orders')
def ensure_account(username='demo', init_usdt=10000.0):
    acc = acct_table.get(Query().username == username)
    if not acc:
        acc = {'username': username, 'balances': {'USDT': init_usdt, 'BTC': 0.0, 'ETH': 0.0}, 'created': time.time()}
        acct_table.insert(acc)
        return acc
    return acc
def get_market_price(symbol='BTC/USDT'):
    base = 30000 if 'BTC' in symbol else 2000
    return base * (1 + random.uniform(-0.01, 0.01))
def place_order(username, symbol, side, order_type, quantity, price=None, testnet=False):
    ensure_account(username)
    price_exec = price or get_market_price(symbol)
    filled_qty = 0.0
    fee = 0.001
    if order_type == 'market':
        filled_qty = quantity
    else:
        market_price = get_market_price(symbol)
        if (side=='BUY' and price >= market_price) or (side=='SELL' and price <= market_price):
            filled_qty = quantity
        else:
            order = {'id': int(time.time()*1000), 'username': username, 'symbol': symbol, 'side': side, 'type': order_type, 'quantity': quantity, 'price': price, 'status': 'open', 'ts': time.time(), 'testnet': testnet}
            orders_table.insert(order)
            return order
    base, quote = symbol.split('/')
    if side == 'BUY':
        cost = filled_qty * price_exec * (1 + fee)
        acc = acct_table.get(Query().username == username)
        if acc['balances'].get('USDT',0) < cost:
            return {'error': 'insufficient_funds'}
        acc['balances']['USDT'] -= cost
        acc['balances'][base] = acc['balances'].get(base,0) + filled_qty
    else:
        acc = acct_table.get(Query().username == username)
        if acc['balances'].get(base,0) < filled_qty:
            return {'error': 'insufficient_asset'}
        proceeds = filled_qty * price_exec * (1 - fee)
        acc['balances'][base] -= filled_qty
        acc['balances']['USDT'] = acc['balances'].get('USDT',0) + proceeds
    acct_table.update(acc, Query().username==username)
    order = {'id': int(time.time()*1000), 'username': username, 'symbol': symbol, 'side': side, 'type': order_type, 'quantity': filled_qty, 'price': price_exec, 'status': 'filled', 'ts': time.time(), 'testnet': testnet}
    orders_table.insert(order)
    return order
def get_account(username='demo'):
    ensure_account(username)
    return acct_table.get(Query().username==username)
def list_orders(username='demo'):
    return orders_table.search(Query().username==username)
