#根据订阅地址，解析出订阅节点
TEST=1
#读取命令行参数
#echo "$1"
#ss://YWVzLTEyOC1nY206OTM0ZTQzNmYtMTMyYi00YzM4LWFjY2EtYzJhYjFmMTlhM2Zm@sg01.etonfast.top:31013#%F0%9F%87%B8%F0%9F%87%AC%20SGD%20Gcore%20x0.5
#url='ss://YWVzLTEyOC1nY206OTM0ZTQzNmYtMTMyYi00YzM4LWFjY2EtYzJhYjFmMTlhM2Zm@sg01.etonfast.top:31013#%F0%9F%87%B8%F0%9F%87%AC%20SGD%20Gcore%20x0.5'
url=$1
echo ""
#协议类型
protocol=$(echo $url | awk -F'://' '{print $1}')
#echo "协议类型：$protocol"

#密码
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
echo "测试节点："
echo "协议类型：$protocol"
echo "加密前密钥：$phrase_e"
echo "密码：$phrase"
echo "密钥：$key"
echo "加密方法：$method"
echo "域名：$domain"
echo "端口：$port"
echo "节点说明：$description"
fi
#使用nc命令测试节点
nc -vz $domain $port > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "NC探测节点可用"
    #使用订阅节点开启代理
    #ss-local -s $domain -p $port -l 1080 -k $key -m $method > /dev/null 2>&1 &

    echo "尝试连接"
    echo "ss-local -s $domain -p $port -k $key -m $method -l 1080 -v "

    ss-local -s $domain -p $port -k $key -m $method -l 1080 -v > /dev/null  &
    PID=$!
    sleep 2

    #使用curl获得代理服务器的IP地址
    server_ip=$(curl -s -x socks5h://127.0.0.1:1080 https://api.ip.sb/ip -A Mozilla)
    echo "代理服务器的IP地址：$server_ip"

    #根据IP查询地址

    server_info=$(curl -s https://api.ip.sb/geoip/{$server_ip} -A Mozilla)
    # | jq -r ".city")

    server_country=$(echo $server_info | jq -r ".country")
    server_city=$(echo $server_info | jq -r ".city")
    #google跳转地址

    google=$(curl -x socks5h://127.0.0.1:1080 -Ls -o /dev/null -w '%{url_effective}\n' https://www.google.com)

    echo "代理服务器地理位置：$server_country:$server_city"
    echo "Google跳转地址：$google"
    
    # echo "按任意键退出"
    # read 
    # #read  

    #关闭代理服务器
    kill -9 $PID

else
    echo "节点不可用"
fi






#等待10秒


#关闭后台进场