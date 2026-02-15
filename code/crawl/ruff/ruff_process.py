import json
import os

# 获取ruff.json : (其中包含了所有ruff的配置项和描述等信息)
# curl -L https://json.schemastore.org/ruff.json -o ruff.json
# --- 配置 ---
INPUT_FILE = "ruff.json"
BASE_DIR = "Ruff"
RULES_DIR = os.path.join(BASE_DIR, "rules")
INDEX_FILE = os.path.join(BASE_DIR, "RuffIndex.json")


def get_ruff_setting_url(setting_name):
    """生成 Ruff 配置项的官方文档链接"""
    # Ruff 的文档锚点通常是配置项名称
    return f"https://docs.astral.sh/ruff/settings/#{setting_name}"


def extract_type_info(prop_data):
    """从 Schema 属性中提取类型信息"""
    if "type" in prop_data:
        t = prop_data["type"]
        return t if isinstance(t, str) else "/".join([x for x in t if x != "null"])
    if "anyOf" in prop_data:
        types = []
        for item in prop_data["anyOf"]:
            if "type" in item:
                types.append(item["type"])
            elif "$ref" in item:
                types.append(item["$ref"].split("/")[-1])
        return "/".join(filter(None, types))
    return "unknown"


def process_ruff_schema():
    # 1. 初始化目录
    if not os.path.exists(RULES_DIR):
        os.makedirs(RULES_DIR)

    if not os.path.exists(INPUT_FILE):
        print(f"错误: 找不到输入文件 {INPUT_FILE}")
        return

    # 2. 加载 JSON 数据
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    properties = schema.get("properties", {})
    definitions = schema.get("definitions", {})
    index_data = {}

    print(f"开始处理 Ruff 配置项，共 {len(properties)} 个...")

    for setting_name, prop_data in properties.items():
        # --- A. 提取描述 ---
        raw_desc = prop_data.get("description", "No description provided.")
        # 提取第一行作为摘要用于 Index
        summary = raw_desc.split('\n')[0]

        # --- B. 组织 Option 字段 ---
        # 对于 Ruff 配置项，Option 展示其类型、是否废弃以及子项
        opt_parts = []

        # 类型信息
        type_info = extract_type_info(prop_data)
        opt_parts.append(f"Type: {type_info}")

        # 废弃状态
        if prop_data.get("deprecated"):
            opt_parts.append("Status: DEPRECATED")

        # 检查是否有复杂的定义引用 (Definitions)
        ref = None
        if "$ref" in prop_data:
            ref = prop_data["$ref"]
        elif "anyOf" in prop_data:
            for item in prop_data["anyOf"]:
                if "$ref" in item:
                    ref = item["$ref"]
                    break

        if ref:
            def_name = ref.split("/")[-1]
            if def_name in definitions:
                sub_props = definitions[def_name].get("properties", {})
                if sub_props:
                    opt_parts.append("\nAvailable Sub-options:")
                    for sub_name, sub_data in sub_props.items():
                        sub_desc = sub_data.get("description", "").split('\n')[0]
                        opt_parts.append(f"  - {sub_name}: {sub_desc}")

        option_content = "\n".join(opt_parts) if opt_parts else "This setting has no specific sub-options."

        # --- C. 组织 Index 数据 ---
        url = get_ruff_setting_url(setting_name)
        index_data[setting_name] = {
            "description": summary,
            "url": url
        }

        # --- D. 生成详情文件 ---
        rule_content = {
            setting_name: {
                "description": f"Description\n\n{raw_desc}",
                "option": option_content
            }
        }

        # 写入文件
        file_path = os.path.join(RULES_DIR, f"{setting_name}.json")
        with open(file_path, 'w', encoding='utf-8') as rf:
            json.dump(rule_content, rf, ensure_ascii=False, indent=4)

    # 3. 写入 Index 文件
    with open(INDEX_FILE, 'w', encoding='utf-8') as ifile:
        json.dump(index_data, ifile, ensure_ascii=False, indent=4)

    print(f"\n处理完成！")
    print(f"索引文件: {INDEX_FILE}")
    print(f"规则目录: {RULES_DIR}")


if __name__ == "__main__":
    process_ruff_schema()