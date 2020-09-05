# EVE-Monitor

This is a monitor for the popular MMORPG [EVE Online](https://www.eveonline.com/). Currently it has the capacity to monitor market orders, in order to help you find the best priced orders around.

## Installation

Run the following to install dependencies.

```bash
pip install -r requirements.txt
```

This project also requires the use of [Pushover](https://pushover.net/) in order to achieve real-time push notification. You need to go to its website to signup for a free trial account and get your own user key and app token. Store them in a file named `keys.py`. Note that the free trial expires in 7 days.

You also need a file named `targets.json`, to specify the items you want to look for on the market. You can make this file by following `targets_template.json`.

## Usage

```bash
python tasks.py
```

Note that you can also run most individual functions in market_monitor.py on the command line directly. 

## License

[Apache license 2.0](https://choosealicense.com/licenses/apache-2.0/)
