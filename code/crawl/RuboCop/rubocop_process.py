import yaml
import json
import os

# 获取default.yml :
# curl -L https://raw.githubusercontent.com/rubocop/rubocop/master/config/default.yml -o default.yml
# --- 配置 ---
INPUT_FILE = "default.yml"
BASE_DIR = "RuboCop"
RULES_DIR = os.path.join(BASE_DIR, "rules")


# --- 处理 Ruby 特有标签 ---
def ruby_constructor(loader, node):
    return loader.construct_scalar(node)


yaml.SafeLoader.add_constructor('!ruby/regexp', ruby_constructor)
yaml.SafeLoader.add_constructor('!ruby/symbol', ruby_constructor)


def sanitize_filename(name):
    """将 Style/Alias 转换为 Style_Alias"""
    return name.replace('/', '_').replace(':', '').replace('*', 'Any')


def get_rubocop_doc_url(cop_name):
    """根据 Cop 名字生成官方文档链接"""
    if '/' in cop_name:
        dept, name = cop_name.split('/')
        # 官方文档锚点通常是部门+名称，且全小写无斜杠
        anchor = cop_name.replace('/', '').lower()
        return f"https://docs.rubocop.org/rubocop/cops_{dept.lower()}.html#{anchor}"
    return "https://docs.rubocop.org/rubocop/cops.html"


def process_rubocop():
    # 1. 初始化目录
    if not os.path.exists(RULES_DIR):
        os.makedirs(RULES_DIR)

    if not os.path.exists(INPUT_FILE):
        print(f"错误: 找不到 {INPUT_FILE}")
        return

    # 2. 加载 YAML
    print(f"正在加载并解析 {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            raw_data = yaml.load(f, Loader=yaml.SafeLoader)
    except Exception as e:
        print(f"解析失败: {e}")
        return

    # 定义哪些键是“元数据”，不属于 Options
    meta_keys = {
        'Description', 'Enabled', 'StyleGuide', 'Reference', 'Safe',
        'SafeAutoCorrect', 'VersionAdded', 'VersionChanged',
        'Exclude', 'Include', 'Details', 'InheritEnv'
    }

    index_data = {}

    print("开始组织文件结构...")
    for cop_name, config in raw_data.items():
        # 过滤全局配置项
        if cop_name == 'AllCops' or not isinstance(config, dict):
            continue

        # --- A. 提取描述 ---
        # 结合 Description 和 Details (详情)
        desc_main = config.get('Description', 'No description provided.')
        details = config.get('Details', '')

        full_description = f"Description\n\n{desc_main}"
        if details:
            full_description += f"\n\nDetails:\n{details}"

        # --- B. 提取 Options ---
        options_list = []
        for key, value in config.items():
            if key not in meta_keys:
                # 格式化选项：名字 (默认值)
                options_list.append(f"{key}: {value} (type: {type(value).__name__})")

        if options_list:
            option_field = "This rule supports the following parameters in your configuration:\n\n" + "\n".join(
                options_list)
        else:
            option_field = "This rule has no specific options."

        # --- C. 组织 Index 数据 ---
        url = get_rubocop_doc_url(cop_name)
        index_data[cop_name] = {
            "description": desc_main,
            "url": url
        }

        # --- D. 生成规则文件 ---
        rule_content = {
            cop_name: {
                "description": full_description,
                "option": option_field
            }
        }

        # 写入文件，注意文件名处理
        filename = f"{sanitize_filename(cop_name)}.json"
        with open(os.path.join(RULES_DIR, filename), 'w', encoding='utf-8') as rf:
            json.dump(rule_content, rf, ensure_ascii=False, indent=4)

    # 3. 写入 Index 文件
    index_file_path = os.path.join(BASE_DIR, "RuboCopIndex.json")
    with open(index_file_path, 'w', encoding='utf-8') as ifile:
        json.dump(index_data, ifile, ensure_ascii=False, indent=4)

    print(f"\n处理完成！")
    print(f"索引文件: {index_file_path}")
    print(f"规则总数: {len(index_data)}")


if __name__ == "__main__":
    process_rubocop()