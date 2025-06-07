#%%
import base64
import subprocess
import re
import time
import tempfile
import os
import requests

proxy_providers=[]
proxy_provider = {}
proxy_provider['name']='ETON机场'
proxy_provider['url']="https://happy2025.phantasy.life/api/v1/client/subscribe?token=36f4adb08be578be93565bd41a882dd3"

proxy_providers.append(proxy_provider)
proxy_provider = {}
proxy_provider['name']='TOT机场'
proxy_provider['url']="http://api.xiansws.solutions/api/v1/client/subscribe?token=c31cb62ce6b3e6f40bb99bac42da03df"
url = "https://happy2025.phantasy.life/api/v1/client/subscribe?token=36f4adb08be578be93565bd41a882dd3"

proxy_providers.append(proxy_provider)
#%%

for provider in proxy_providers:
    url=provider['url']
    name=provider['name']
    print(name) 
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text  # 如果是文本（如base64订阅格式）
        msg='成功获取订阅信息'
        print(msg)
        provider['content']=content

        decoded = base64.b64decode(content).decode("utf-8")
        provider['decoded']=decoded


    else:
        print("下载失败:", response.status_code)

# #%%        
# response = requests.get(url)
# if response.status_code == 200:
#     content = response.text  # 如果是文本（如base64订阅格式）
#     msg='成功获取订阅信息'
#     print(msg)
#     print(content[:200])     # 打印前200字符看看
# else:
#     print("下载失败:", response.status_code)


# import base64

# decoded = base64.b64decode(content).decode("utf-8")

#%%

ss_links = []


for line in decoded.splitlines():
    ss_links.append(line)
    

# === 将你的 ss:// 链接粘贴在这里 ===
# ss_links = [
#     "ss://YWVzLTEyOC1nY206OTM0ZTQzNmYtMTMyYi00YzM4LWFjY2EtYzJhYjFmMTlhM2Zm@hk04pro.etonfast.top:31035",
#     # 添加更多...
# ]

# 临时监听端口（每个节点使用不同端口）

#%%
BASE_LOCAL_PORT = 10800

def parse_ss_link(ss_link):
    if not ss_link.startswith("ss://"):
        return None
    body = ss_link[5:]
    try:
        # 去掉 #后面的注释
        if '#' in body:
            body = body.split('#')[0]

        if '@' in body:
            base64_part, address = body.split('@', 1)
            host, port = address.split(':')
            decoded = base64.b64decode(base64_part + '===').decode()
            method, password = decoded.split(':', 1)
            return {
                "method": method,
                "password": password,
                "server": host,
                "port": int(port)
            }
    except Exception as e:
        print(f"解析失败：{ss_link}\n错误：{e}")
        return None

def test_node(config, local_port):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(f"""{{
    "server": "{config['server']}",
    "server_port": {config['port']},
    "local_port": {local_port},
    "password": "{config['password']}",
    "method": "{config['method']}",
    "timeout": 5,
    "mode": "tcp_and_udp"
}}""")
        config_path = f.name

    # 启动 ss-local
    proc = subprocess.Popen(["ss-local", "-c", config_path, "-v"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    time.sleep(2)  # 等待启动

    # 测试出口 IP
    try:
        result = subprocess.run(
            ["curl", "--socks5", f"127.0.0.1:{local_port}", "-m", "5",
             "-A", "Mozilla", "https://api.ip.sb/ip"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=8
        )
        ip = result.stdout.decode().strip()
        success = (result.returncode == 0 and re.match(r"^\d+\.\d+\.\d+\.\d+$", ip))
    except Exception as e:
        success = False
        ip = str(e)

    # 关闭 ss-local
    proc.terminate()
    proc.wait()
    os.remove(config_path)

    return success, ip

def main():
    for idx, link in enumerate(ss_links):
        print(f"\n🧪 正在测试节点 #{idx + 1}")
        config = parse_ss_link(link)
        if not config:
            print("❌ 解析失败")
            continue
        local_port = BASE_LOCAL_PORT + idx
        success, output = test_node(config, local_port)
        if success:
            print(f"✅ 成功，出口 IP：{output}")
        else:
            print(f"❌ 失败，错误信息：{output}")

if __name__ == "__main__":
    main()


#%% 代码学习

import subprocess

#%%
ps = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
grep = subprocess.Popen(["grep", "zsh"], stdin=ps.stdout, stdout=subprocess.PIPE)
#ps.stdout.close()  # 关闭 ps 的 stdout 以通知 EOF
output = grep.communicate()[0].decode()
print(output)
