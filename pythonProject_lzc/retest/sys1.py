from netmiko import ConnectHandler



def common(sw_type, ip, username, passwd, secret):
    device = {
        'device_type': sw_type,  # 使用 telnet 登录
        'host': ip,  # 交换机的 IP 地址
        'username': username,  # 空字符串，因为没有用户名
        'password': passwd,  # 交换机的 telnet 密码
        'secret': secret,  # Enable 模式密码（可选，若需要进入特权模式）
    }
    try:
        connection = ConnectHandler(**device)
        connection.enable()

        return connection
    except Exception as e:
        print(e)
        return 0

if __name__ == '__main__':
    SW1 = common('cisco_ios_telnet','10.74.19.88','','Cisco1234!','Cisco1234!')
    output = SW1.send_command('show cdp neighbors gi 1/0/1 detail')
    print(output)
