import requests
import json
import time
import logging
import datetime
from plyer import notification

from market_monitor import get_item_orders_in_region, get_system_name
import keys as k

APP_TOKEN = k.APP_TOKEN
USER_KEY  = k.USER_KEY
# GROUP_KEY = k.GROUP_KEY

REGIONS_LST = 'regions.json'
TARGETS_LST = 'targets.json'

logging.basicConfig(format='%(asctime)s %(levelname)s\t%(message)s', level=logging.INFO)
order_id_seen = [] # TODO perhaps cache/store in file system?
regions = json.load(open(REGIONS_LST))

while True:
    # load targets each iteration to allow changes
    targets = json.load(open(TARGETS_LST))['market_monitor']
    s = requests.Session()

    for t in targets:
        order_seen = 0
        res = []
        tid = t
        name = targets[t]['name']
        tres = targets[t]['threshold']
        logging.info(f'Looking for {name} below {tres:,} isk')

        for r in regions:
            if not regions[r]['known_space']: continue
            rid = regions[r]['region_id']
            orders = get_item_orders_in_region(tid, rid, s)
            if not orders: continue
            order_seen += len(orders)
            for o in orders:
                if o['price'] <= tres and o['order_id'] not in order_id_seen:
                    order_id_seen.append(o['order_id'])
                    system = get_system_name(o['system_id'], s)
                    out = f"{name} selling for {o['price']:,.0f} isk in {system}, {regions[r]['name']}, {o['volume_remain']}/{o['volume_total']}"
                    logging.info(out)
                    res.append(out)

        if order_seen == 0:
            logging.warning(f'Done looking for {name}, no order found')

        title = 'EVE Market Monitor'
        for msg in res:
            # desktop notification
            notification.notify(title=title, message=msg, app_name=title,)
            
            # pushover notification
            data = {
                'token' : APP_TOKEN,
                'user' : USER_KEY,
                'title': 'EVE Market Monitor',
                'message': msg,
                'priority': 0,
            }
            r = s.post('https://api.pushover.net/1/messages.json', data=data)
            if r.status_code != 200:
                logging.error('Notification failed to send')
                break

    logging.info('----sleep----')
    s.close()
    time.sleep(60*5)
