from flask import Blueprint, request, jsonify
from binance_paper import place_order as paper_place, get_account as paper_account, list_orders as paper_orders

trader = Blueprint('trader', __name__)

@trader.route('/account', methods=['GET'])
def account():
    user = request.args.get('user', 'demo')
    mode = request.args.get('mode', 'paper')
    if mode == 'paper':
        acc = paper_account(user)
        return jsonify({'account': acc})
    else:
        return jsonify({'error':'live_mode_not_configured_in_scaffold'}), 400

@trader.route('/order', methods=['POST'])
def order():
    data = request.json or {}
    user = data.get('user','demo')
    symbol = data.get('symbol','BTC/USDT')
    side = data.get('side','BUY')
    order_type = data.get('type','market')
    quantity = float(data.get('quantity',0))
    mode = data.get('mode','paper')
    if mode == 'paper':
        res = paper_place(user, symbol, side, order_type, quantity, price=None, testnet=False)
        return jsonify(res)
    else:
        return jsonify({'error':'live_mode_not_configured_in_scaffold'}), 400
