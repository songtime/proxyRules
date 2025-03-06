import os
import yaml
import sys

def load_order_list(order_file):
    """读取当前目录下的 order.txt 文件，返回分流类型的新顺序列表"""
    try:
        with open(order_file, 'r', encoding='utf-8') as f:
            order = [line.strip() for line in f if line.strip()]
        return order
    except Exception as e:
        print(f"读取排序文件 {order_file} 出错：{e}")
        sys.exit(1)

def extract_rule_info(rule):
    """
    从规则字符串中提取分流类型和分流域名。
    假设规则格式为：字段1, 字段2, ..., 分流域名, 分流类型
    返回 (分流类型, 分流域名) 元组。
    """
    fields = [field.strip() for field in rule.split(",")]
    if len(fields) < 2:
        return None, None
    routing_type = fields[-1]
    routing_domain = fields[-2]
    return routing_type, routing_domain

def load_yaml_data(yaml_file):
    """通过 PyYAML 加载 YAML 数据，用于提取 rules 列表"""
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data
    except Exception as e:
        print(f"读取 YAML 文件 {yaml_file} 出错：{e}")
        sys.exit(1)

def get_sorted_rules(rules, order_list):
    """
    对 rules 字段列表进行排序：
    1. 按照 order_list 中分流类型的索引排序
    2. 同一分流类型内，再按照分流域名（忽略大小写）的字母顺序排序
    """
    extracted_types = set()
    rule_info_list = []  # 元素为 (原规则字符串, 分流类型, 分流域名)
    for rule in rules:
        if isinstance(rule, str):
            routing_type, routing_domain = extract_rule_info(rule)
            if routing_type is None:
                continue
            extracted_types.add(routing_type)
            rule_info_list.append((rule, routing_type, routing_domain))
        else:
            rule_str = str(rule)
            routing_type, routing_domain = extract_rule_info(rule_str)
            if routing_type is None:
                continue
            extracted_types.add(routing_type)
            rule_info_list.append((rule_str, routing_type, routing_domain))
    missing_types = [t for t in extracted_types if t not in order_list]
    if missing_types:
        print("错误：以下分流类型未在 order.txt 文件中出现，程序终止：")
        for t in missing_types:
            print(t)
        sys.exit(1)
    
    def sort_key(item):
        # item: (rule, routing_type, routing_domain)
        _, routing_type, routing_domain = item
        order_index = order_list.index(routing_type)
        return (order_index, routing_domain.lower())
    
    sorted_rule_info = sorted(rule_info_list, key=sort_key)
    sorted_rules = [item[0] for item in sorted_rule_info]
    return sorted_rules

def main():
    # 获取当前目录
    current_dir = os.getcwd()
    yaml_file = os.path.join(current_dir, "clashRule.yaml")
    order_file = os.path.join(current_dir, "order.txt")
    output_file = os.path.join(current_dir, "sorted_clashRule.yaml")
    
    # 读取 order.txt 与 YAML 文件数据（用于计算排序后的 rules 列表）
    order_list = load_order_list(order_file)
    yaml_data = load_yaml_data(yaml_file)
    original_rules = yaml_data.get("rules", [])
    if not original_rules:
        print("YAML 文件中未找到 rules 字段或其为空。")
        sys.exit(1)
    
    sorted_rules = get_sorted_rules(original_rules, order_list)
    
    # 读取原始文件文本，保留 rules: 字段上方内容不变
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"读取 YAML 文件文本时出错：{e}")
        sys.exit(1)
    
    # 找到 rules: 这一行（忽略前导空格）
    header_end_index = None
    for i, line in enumerate(lines):
        if line.lstrip().startswith("rules:"):
            header_end_index = i
            break
    if header_end_index is None:
        print("未找到 rules: 字段，程序终止。")
        sys.exit(1)
    
    # header 部分保留到 rules: 这一行
    header_lines = lines[:header_end_index+1]
    
    # 生成新的 rules 列表的 YAML 字符串（不包含顶级缩进）
    new_rules_yaml = yaml.dump(sorted_rules, allow_unicode=True, default_flow_style=False)
    # 由于 rules: 后面的列表通常需要一定的缩进，这里我们假设使用两个空格进行缩进
    indent = "  "
    indented_rules = ""
    for line in new_rules_yaml.splitlines():
        # 如果该行非空，则增加缩进
        if line.strip():
            indented_rules += indent + line + "\n"
        else:
            indented_rules += "\n"
    
    # 组装新文件内容：保留 header 部分，后接新的 rules 块
    new_file_content = "".join(header_lines) + "\n" + indented_rules
    
    # 输出到新的 YAML 文件中
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_file_content)
        print(f"排序后的 YAML 已输出到 {output_file}")
    except Exception as e:
        print(f"写入 YAML 文件 {output_file} 出错：{e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
