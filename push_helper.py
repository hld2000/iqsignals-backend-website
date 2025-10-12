import os, json
from pywebpush import webpush, WebPushException
from tinydb import TinyDB, Query
DB_FILE = os.environ.get('SUBS_DB', 'subscriptions.json')
VAPID_FILE = os.environ.get('VAPID_FILE', 'vapid_keys.json')
db = TinyDB(DB_FILE)
subs_table = db.table('subs')
def load_vapid():
    if not os.path.exists(VAPID_FILE):
        raise RuntimeError('VAPID file not found at ' + VAPID_FILE)
    with open(VAPID_FILE, 'r') as f:
        return json.load(f)
def add_subscription(sub):
    if subs_table.search(Query().endpoint == sub.get('endpoint')):
        return False
    subs_table.insert(sub)
    return True
def list_subscriptions():
    return subs_table.all()
def send_push(subscription_info, payload):
    vapid = load_vapid()
    private_pem = vapid.get('private_pem')
    try:
        resp = webpush(subscription_info, payload=json.dumps(payload), vapid_private_key=private_pem, vapid_claims={"sub": "mailto:admin@example.com"})
        return True, getattr(resp, 'status_code', 200)
    except WebPushException as ex:
        return False, str(ex)
