import re
import time
import sys
from logging import exception

from datetime import datetime

from netmiko import ConnectHandler
import logging

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=f'./logs/{timestamp}.log',
    filemode='w'
)
def telnet_to_switch_with_netmiko(host, username, password, enable_password):
    try:
        # 定义设备参数
        device = {
            "device_type": "cisco_ios_telnet",  # 使用 Telnet 连接 Cisco IOS
            "host": host,
            "username": username,
            "password": password,
            "secret": enable_password,  # enable 密码
        }

        # 建立连接
        connection = ConnectHandler(**device)

        # 进入特权模式
        connection.enable()

        logging.info('Switch connected successful!')
        return connection

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return f"An error occurred: {e}"
def test1(c, start, end):
    lab = []
    for i in range(start, end+1):
        coo = f'show cdp neighbors gi 1/0/{i} detail'
        result = c.send_command(coo)
        # print(result)
        if 'Total cdp entries displayed : 0' in result:
            ip_address = ['0']
            mac = ['0']
            Platform = ['0']
            dict_list = {"id": f'gi 1/0/{i}', "ip_address": ip_address[0], "mac_address": mac[0],
                            "Platform": Platform[0]}
            lab.append(dict_list)
        else:
            ip_address = re.findall(r'\d+\.\d+\.\d+\.\d+', result)
            if len(ip_address) == 0:
                ip_address = ['0']

            mac = re.findall(r'SE[A-Z0-9]+', result)
            if len(mac) == 0:
                mac = ['0']

            Platform = re.findall(r'Platform: (.+?),', result)
            if len(Platform) == 0:
                Platform = ['0']


            dict_list = {"id": f'gi 1/0/{i}', "ip_address": ip_address[0], "mac_address": mac[0][3:15],
                            "Platform": Platform[0]}
            lab.append(dict_list)
    logging.info('Cycle add port information!')
    return lab

def all_test():
    start = time.time()
    connection = telnet_to_switch_with_netmiko(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    list1 = test1(connection, 1, 8)
    list1.insert(0,{'id': 'id', 'ip_address': 'ip_address', 'mac_address': 'mac_address', 'Platform': 'Platform'})
    try:
        with open('w.txt', 'w') as file:
            for i in list1:
                a = f'{i["id"]:<15}  {i["ip_address"]:<15}  {i["mac_address"]:<15}  {i["Platform"]:<15}' + "\n"
                file.write(a)
    except exception as f:
        logging.error(f'File open failed,Reason is {f}')
        return f
    logging.info('The relevant data is entered into a text file')
    connection.disconnect()
    logging.info('Switch disconnected')
    end = time.time()
    print(f'运行时间为{end-start}')
if __name__ == "__main__":
    all_test()

