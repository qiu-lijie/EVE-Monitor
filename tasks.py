import logging
import requests
import time
import traceback

from eve_monitor.constants import SETTINGS
from eve_monitor.market_monitor import watch_market


logging.basicConfig(format='%(asctime)s %(levelname)s\t%(message)s', level=logging.INFO)

s = requests.Session()
while True:
    try:
        if SETTINGS['features_enabled']['market_monitor']:
            watch_market(s)
    except Exception:
        logging.error('Unexpected error occurred during market watch:')
        traceback.print_exc()

    logging.info('----sleep----')
    time.sleep(60*5)
