import json
import logging
import requests
import sys
import time
import traceback
from plyer import notification

from market_monitor import get_item_orders_in_region, get_system_name


TITLE = 'EVE Market Monitor'
TARGETS_LST = 'targets.json'
PUSHOVER_URL = 'https://api.pushover.net/1/messages.json'
SETTINGS = json.load(open('appsettings.json', 'r', encoding='utf-8'))
APP_TOKEN = SETTINGS['APP_TOKEN']
USER_KEY  = SETTINGS['USER_KEY']
REGIONS = json.load(open('regions.json', 'r', encoding='utf-8'))

logging.basicConfig(format='%(asctime)s %(levelname)s\t%(message)s', level=logging.INFO)


s = requests.Session()
order_id_seen = [] # TODO perhaps cache/store in file system?

def watch_market():
    """watch market orders for items in TARGET_LIST.market_monitor"""
    targets = json.load(open(TARGETS_LST))['market_monitor']

    for type_id, type_info in targets.items():
        order_seen = 0
        res = []
        name = type_info['name']
        tres = type_info['threshold']
        logging.info(f'Looking for {name} below {tres:,} isk')

        for r in REGIONS:
            if not REGIONS[r]['known_space']: continue
            rid = REGIONS[r]['region_id']
            orders = get_item_orders_in_region(type_id, rid, s)
            if not orders: continue
            order_seen += len(orders)
            for o in orders:
                if o['price'] <= tres and o['order_id'] not in order_id_seen:
                    order_id_seen.append(o['order_id'])
                    system = get_system_name(o['system_id'], s)
                    out = f"{name} selling for {o['price']:,.0f} isk in {system}, {REGIONS[r]['name']}, {o['volume_remain']}/{o['volume_total']}"
                    logging.info(out)
                    res.append(out)

        if order_seen == 0:
            logging.warning(f'Done looking for {name}, no order found')

        for msg in res:
            # desktop notification
            try:
                if sys.platform.startswith('win'):
                    notification.notify(title=TITLE, message=msg, app_name=TITLE,)
                # TODO add mac support
                else:
                    logging.warning('No supported desktop notification implementation found')
            except:
                logging.error('Unable to send desktop notification')
                traceback.print_exc()

            # pushover notification
            try:
                data = {
                    'token' : APP_TOKEN,
                    'user' : USER_KEY,
                    'title': TITLE,
                    'message': msg,
                    'priority': 0,
                }
                r = s.post(PUSHOVER_URL, data=data)
                if r.status_code != 200:
                    raise Exception(f'Status code {r.status_code}, {r.content}')
            except:
                logging.error('Unable to send pushover notification')
                traceback.print_exc()
    return


while True:
    try:
        if SETTINGS['features_enabled']['market_monitor']:
            watch_market()
    except Exception:
        logging.error('Unexpected error occurred during market watch:')
        traceback.print_exc()

    logging.info('----sleep----')
    time.sleep(60*5)
