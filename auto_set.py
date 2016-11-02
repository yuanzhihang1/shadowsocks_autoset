# coding=utf-8
import json
import urllib
import re
import os

server_name = '服务器地址:'
url = 'http://www.ishadowsocks.net/'
code = 'utf-8'

u = urllib.urlopen(url)
lines = u.readlines()

def find_pass(lines):
    result_list = []
    ok = 0
    passwd = 0
    port = 0
    host_name = ''
    for line in lines:
        if not re.search(server_name, line) and ok == 0:
            continue
        if host_name == '':
            host_name = re.findall(':([\w\.]*)<', line)[0]
            print("host name:%s" % host_name)
        ok = 1
        if '端口' in line:
            rst = re.findall(':(\d*)', line)
            print('port:%s' % rst[0])
            port = rst[0]
        if '密码' in line:
            rst = re.findall(':(\d*)', line)
            print('passwd:%s' % rst[0])
            passwd = rst[0]
        if passwd and port:
            result_list.append((host_name, passwd, port))
            ok = 0
            host_name = ''
    return result_list

result_list = find_pass(lines)
assert len(result_list) != 0, 'cannot get config'
f = open('gui-config.json').read()
data = json.loads(f)
for host_name, passwd, port in result_list:
    is_init = 0
    for i in data['configs']:
        if i['server'] == host_name:
            is_init = 1
            i['password'] = passwd
            i['server_port'] = port

    if not is_init:
        new_conf = {'server': host_name,
                    'server_port': int(port),
                    'password': passwd,
                    'method': "aes-256-cfb",
                    }
        data['configs'].append(new_conf)
s = json.dumps(data,indent=3)
f = open('gui-config.json', 'w')
f.write(s)
f.close()
os.systemtem('Shadowsocks.exe')
