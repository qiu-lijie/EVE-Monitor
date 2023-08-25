import json


TITLE = 'EVE Market Monitor'
ESI_URL = 'https://esi.evetech.net/latest'
PUSHOVER_URL = 'https://api.pushover.net/1/messages.json'

TARGETS_JSON = 'targets.json'
SETTINGS = json.load(open('appsettings.json', 'r', encoding='utf-8'))
APP_TOKEN = SETTINGS['APP_TOKEN']
USER_KEY  = SETTINGS['USER_KEY']
REGIONS = json.load(open('regions.json', 'r', encoding='utf-8'))
