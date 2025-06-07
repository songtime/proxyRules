url=$1
#原始订阅地址是windwos 格式，需要转换为linux格式
#此处忽略
curl -s "$url" | base64 -d 