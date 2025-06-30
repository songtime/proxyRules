#!/bin/bash
#根据订阅地址，解析出订阅节点
# 输入参数为 ss:// 节点链接

url="$1"
TEST=0
#ss://YWVzLTEyOC1nY206OTM0ZTQzNmYtMTMyYi00YzM4LWFjY2EtYzJhYjFmMTlhM2Zm@sg01.etonfast.top:31013#%F0%9F%87%B8%F0%9F%87%AC%20SGD%20Gcore%20x0.5

#协议类型
# 用:和/2个字符分隔，取第一个字段
protocol=$(echo $url | awk -F'://' '{print $1}')

# 用/和@2个字符分隔
phrase_e=$(echo $url | awk -F '[//@]' '{print $3}')
#echo "密码：$phrase"

# 检查 base64 是否对齐
# base64 编码后的字符串长度必须是 4 的倍数
# 如果不是，则需要补齐 =

b64=$phrase_e
len=${#b64}

echo "len = $len"
if (( len % 4 == 0 )); then
    echo "✅ base64 已对齐"
else
    pad=$((4 - len % 4))
    echo "❌ base64 未对齐，需要补齐 $pad 个 ="

    # 补齐 base64 编码
    for (( i = 0; i < pad; i++ )); do
        b64+="="
    done
    echo "✅ 补齐后的 base64 编码：$b64"
fi

#将phrase解码
phrase=$(echo ${b64} | base64 -d)

#echo "密码：$phrase"

#根据phrase，提取出密钥和加密方法
key=$(echo $phrase | awk -F':' '{print $2}')
#echo "密钥：$key"
method=$(echo $phrase | awk -F':' '{print $1}')
#echo "加密方法：$method"

#域名
domain=$(echo $url | awk -F'@' '{print $2}' | awk -F':' '{print $1}')
#echo "域名：$domain"

#端口
port=$(echo $url | awk -F':' '{print $3}' | awk -F'#' '{print $1}')
#echo "端口：$port"

#节点说明
description=$(echo $url | awk -F'#' '{print $2}' )
#echo "节点说明：$description"

description=$(python3 -c "import urllib.parse; print(urllib.parse.unquote('$description'))")
#echo "节点说明：$description"
if TEST=1; then
cat <<EOF
"测试节点："
"协议类型：$protocol"
"加密前密钥：$phrase_e"
"密码：$phrase"
"密钥：$key"
"加密方法：$method"
"域名：$domain"
"端口：$port"
"节点说明：$description"


EOF
fi


cat <<EOF
# 由脚本生成的最小 Clash Meta 配置
mixed-port: 1080
allow-lan: false
mode: global
log-level: info

proxies:
  - name: "$description"
    type: ss
    server: $domain
    port: $port
    cipher: "$method"
    password: "$key"
    udp: true

proxy-groups:
  - name: "Proxy"
    type: select
    proxies:
      - "$description"

rules:
  - MATCH,Proxy
EOF


