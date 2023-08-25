import requests
import json

ESI_URL = 'https://esi.evetech.net/latest'
# DATASOURCE = 'tranquility'

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
            res[rid] = {'name': r['name'],
                        'region_id': r['region_id'],
                        'known_space': True if r.get('description') else False,
                        }

    json.dump(res, open('regions.json', 'w+'), indent=4)
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
    r = s.get(ESI_URL + f'/markets/{region}/orders/',
              params = {'type_id': item, 'order_type': order_type}
              )
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
