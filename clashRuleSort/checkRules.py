import yaml

def extract_routing_types(yaml_file):
    # 打开并解析 YAML 文件
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # 获取 rules 字段列表
    rules = data.get("rules", [])
    routing_types = set()

    for rule in rules:
        # 确保规则为字符串类型（有的规则可能包含引号，但解析后通常为字符串）
        if isinstance(rule, str):
            # 按逗号分割，取最后一项并去掉前后空白字符
            fields = rule.split(",")
            if fields:
                routing_type = fields[-1].strip()
                routing_types.add(routing_type)
        else:
            # 如果不是字符串，则转换为字符串再处理
            rule_str = str(rule)
            fields = rule_str.split(",")
            if fields:
                routing_type = fields[-1].strip()
                routing_types.add(routing_type)
    return routing_types

if __name__ == '__main__':
    yaml_file = "/Users/mac/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/profiles/LgxPf2lSfTty.yaml"
  # 请确保文件路径正确
    routing_types = extract_routing_types(yaml_file)
    
    print("提取到的分流规则类型如下：")
    for r in routing_types:
        print(r)
