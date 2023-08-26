import logging
import requests
import time
import traceback

from eve_monitor.constants import SETTINGS
from eve_monitor.contract_sniper import watch_contract
from eve_monitor.market_monitor import watch_market


logging.basicConfig(format='%(asctime)s %(levelname)s\t%(message)s', level=logging.INFO)

s = requests.Session()
FEATURES = SETTINGS['features_enabled']
poll_rate = SETTINGS['poll_rate_in_min']
while True:
    try:
        if FEATURES['market_monitor']:
            watch_market(s)
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
