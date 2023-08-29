import json
import logging
import os
import requests
import signal
import sys
import time
import traceback

from eve_monitor.constants import SETTINGS
from eve_monitor.contract_sniper import watch_contract
from eve_monitor.market_monitor import MARKET_MONITOR, watch_market


logging.basicConfig(format='%(asctime)s %(levelname)s\t%(message)s', level=logging.INFO)

def dump_cache(cache: {str: [str]}):
    """cleanup then dump cache to file system"""
    CACHE_LIMIT = 100
    for k in cache:
        if len(cache[k]) > CACHE_LIMIT:
            cache[k] = cache[k][-CACHE_LIMIT:]

    json.dump(cache, open(CACHE_JSON, 'w+', encoding='utf-8', newline='\n'), indent=4)
    return

CACHE_JSON = 'cache.json'
if not os.path.exists(CACHE_JSON):
    json.dump({}, open(CACHE_JSON, 'w+', encoding='utf-8', newline='\n'), indent=4)
file_cache = json.load(open(CACHE_JSON, 'r', encoding='utf-8'))

def handle_interrupt(_, __):
    """dump file cache then exist when interrupt"""
    dump_cache(file_cache)
    sys.exit(0)
    return

signal.signal(signal.SIGINT, handle_interrupt)


s = requests.Session()
FEATURES = SETTINGS['features_enabled']
poll_rate = SETTINGS['poll_rate_in_min']
while True:
    try:
        if FEATURES[MARKET_MONITOR]:
            watch_market(s, file_cache)
    except:
        logging.error('Unexpected error occurred during market watch:')
        traceback.print_exc()

    try:
        if FEATURES['contract_sniper']:
            watch_contract(s)
    except:
        logging.error('Unexpected error occurred during contract watch:')
        traceback.print_exc()

    logging.info('----sleep----')
    time.sleep(poll_rate * 60)
