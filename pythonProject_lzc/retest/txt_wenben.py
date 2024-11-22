import logging
import time
from datetime import datetime
yu = [{'id': 'gi 1/0/1', 'ip_address': '100.100.10.101', 'mac_address': '845A3EC22539', 'Platform': 'Cisco IP Phone 9861'},
        {'id': 'gi 1/0/2', 'ip_address': '100.100.10.87', 'mac_address': 'F8C65049533C', 'Platform': 'Cisco IP Phone 9851'}
]

yu.insert(0,{'id': 'id', 'ip_address': 'ip_address', 'mac_address': 'mac_address', 'Platform': 'Platform'})
with open('w.txt', 'w') as file:
    for i in yu:
        print(i)
        a = f'{i["id"]:<15}  {i["ip_address"]:<15}  {i["mac_address"]:<15}  {i["Platform"]:<15}'+"\n"
        file.write(a)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=f'./logs/app_{timestamp}.log',
    filemode='w'
)
logging.info('fvadfgkjdnlskafgjv')

