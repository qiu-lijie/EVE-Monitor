import logging
import json
import requests

from .constants import ESI_URL, TARGETS_JSON, REGIONS_JSON, REGIONS
from .utils import get_module_name, send_notification

MARKET_MONITOR = get_module_name(__name__)


def get_region_info(s=None):
    """
    Get the region info, save to regions.json
    Args:
        s (requests.Session object): Session to use, will create one if none provided
    Returns:
        Returns True when successfully made all requests
    """
    if s == None:
        s = requests.Session()
    r = s.get(ESI_URL + '/universe/regions/')
    if r.status_code != 200:
        return False
    
    res = {}
    for rid in r.json():
        r = s.get(ESI_URL + f'/universe/regions/{rid}/')
        if r.status_code == 200:
            r = r.json()
            res[rid] = {
                'name': r['name'],
                'region_id': r['region_id'],
                'known_space': True if r.get('description') else False,
                }

    json.dump(res, open(REGIONS_JSON, 'w+'), indent=4)
    return True


def get_item_orders_in_region(item, region, s=None, order_type='sell'):
    """
    Get the given item orders in given region
    Args:
        item (int): item type_id
        region (int): region_id
        s (requests.Session object): Session to use, will create one if none provided
        order_type (str): one of buy, sell, all; default to sell
    Returns:
        Returns list of order found, None otherwise
    """
    if s == None:
        s = requests.Session()
    res = None
    r = s.get(
        ESI_URL + f'/markets/{region}/orders/', params = {'type_id': item, 'order_type': order_type})
    if r.status_code == 200:
        res = r.json()
    return res


def get_system_name(system, s=None):
    """Returns the system name of given system id, None otherwise"""
    if s == None:
        s =requests.Session()
    res = None
    r = s.get(ESI_URL + f'/universe/systems/{system}/')
    if r.status_code == 200:
        res = r.json().get('name')
    return res


order_id_seen = [] # TODO perhaps cache/store in file system?
def watch_market(s: requests.Session):
    """watch market orders for items in TARGETS.market_monitor"""
    # load each time to enable hot reload
    targets = json.load(open(TARGETS_JSON))[MARKET_MONITOR]

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
            send_notification(s, msg)
    return
