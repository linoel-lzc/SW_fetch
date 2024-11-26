import re


def handle(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # 匹配包含目标行及其后续两行
    pattern = r"(SW.*(?:\n.*){0,4})"
    match = re.findall(pattern, content)
    list_all = []
    for i in range(len(match)):
        data = match[i]
        ip_address = re.findall(r'\d+\.\d+\.\d+\.\d+', data)
        username = re.findall(r'username=(.+)', data)
        if len(username) == 0:
            username = ['']
        passwd = re.findall(r'passwd=(.+)', data)
        secret = re.findall(r'secret=(.+)', data)
        var1 = {
            "ip_address": ip_address[0],
            "username": username[0],
            "passwd": passwd[0],
            "secret": secret[0]
        }
        list_all.append(var1)
    return list_all


if __name__ == '__main__':
    list1 = handle('./sw_detail')
    print(list1)
