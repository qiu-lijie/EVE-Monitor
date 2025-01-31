# EVE_Monitor

This is a monitor for the popular MMORPG [EVE Online](https://www.eveonline.com/). Currently it has the capacity to monitor market orders, to help you find the best priced items around.

## Installation

Run the following to install dependencies.

```bash
pip install -r requirements/base.txt
```

This project also requires the use of [Pushover](https://pushover.net/) in order to send real-time push notification. You need to go to their website to sign up for a free trial account and get your own user key and app token. Store them in a file named `appsettings.json`, as shown in `appsettings.json.bak`

You also need a file named `targets.json`, to specify the items you want to look for on the market. You can make this file by following `targets.json.bak`. Note you can edit this file during run time to add/remove items and adjust their price threshold.

## Usage

```bash
python tasks.py
```

## License

[Apache license 2.0](https://choosealicense.com/licenses/apache-2.0/)

tip jars  
isk `0x1343D00`  
xmr `84TJRMZXdqKbe5KnWd572M3TVzVej2kbuBFZktmHt93b7tWX4u9HuYYAtw8QRk4ptfadH8LbeVU8WWcUXR56o4GSC1cJHsZ`
