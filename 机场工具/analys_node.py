#%%
import requests

url = "https://happy2025.phantasy.life/api/v1/client/subscribe?token=36f4adb08be578be93565bd41a882dd3"

url = "http://api.xiansws.solutions/api/v1/client/subscribe?token=c31cb62ce6b3e6f40bb99bac42da03df"
response = requests.get(url)
if response.status_code == 200:
    content = response.text  # 如果是文本（如base64订阅格式）
    print(content[:200])     # 打印前200字符看看
else:
    print("下载失败:", response.status_code)


import base64

decoded = base64.b64decode(content).decode("utf-8")

#%%

ss_links = []


for line in decoded.splitlines():
    ss_links.append(line)
    print(line)

# %% 根据节点
