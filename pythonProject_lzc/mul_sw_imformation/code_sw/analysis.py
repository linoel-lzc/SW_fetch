from datetime import datetime
import logging
import re
import time
import threading
from threading import current_thread

from netmiko import ConnectHandler
from ..sw_information1.test import handle
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=f'../log/{timestamp}.log',
    filemode='w'
)



class SW_fetch:
    def __init__(self, device_type, host_ip, username, passwd, secret):

        self.device_info = {
            'device_type': device_type,
            'host': host_ip,
            'username': username,  # Telnet 无用户名
            'password': passwd,
            'secret': secret  # Enable 密码
        }
        try:
            self.connection = ConnectHandler(**self.device_info)
            self.connection.enable()
            print(f'{host_ip}连接成功')
            logging.info(f'{host_ip} telnet connected successful')
        except Exception as e:
            print(e)
            logging.error(f'{host_ip} telnet connected failed')

    def execute_command(self, start, end):
        lab = []
        for i in range(start, end + 1):
            coo = f'show cdp neighbors gi 1/0/{i} detail'
            result = self.connection.send_command(coo)
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
        # logging.info('Cycle command fetch data successful!')
        logging.info(f'{self.device_info["host"]} Cycle command fetch data successful!')
        return lab

    def disconnected(self):
        self.connection.disconnect()
        logging.info(f'{self.device_info["host"]} switch telnet disconnected')
        # logging.info('switch telnet disconnected')
def main(i):
        SW1 = SW_fetch('cisco_ios_telnet', i['ip_address'], i['username'], i['passwd'], i['secret'])
        output1 = SW1.execute_command(1, 10)

        output1.insert(0,
                        {'id': 'id', 'ip_address': 'ip_address', 'mac_address': 'mac_address',
                        'Platform': 'Platform'})
        try:
            with open(f'../phone_information_result/{i["ip_address"]}.txt', 'w') as file:
                for j in output1:
                    a = f'{j["id"]:<15}  {j["ip_address"]:<15}  {j["mac_address"]:<15}  {j["Platform"]:<15}' + "\n"
                    file.write(a)
            logging.info(f'{i["ip_address"]} The data is added to the text file')
        except Exception as E:
            print(E)
            logging.error(E)
            # logging.info('The relevant data is entered into a text file')
        SW1.disconnected()

def mul_thread(file_path):
    list1 = handle(file_path)
    threads = []
    for switch in list1:
        thread = threading.Thread(target=main, args=(switch,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    start = time.time()
    mul_thread('../sw_information1/sw_detail')
    end = time.time()
    print(f'运行时间{end-start}')




