import requests
from bs4 import BeautifulSoup
import json
import os
import time


def scrape_eslint_rules_details():
    index_file = os.path.join("ESLint", "ESLintIndex.json")
    rules_dir = os.path.join("ESLint", "rules")

    # 1. 创建 rules 目录
    if not os.path.exists(rules_dir):
        os.makedirs(rules_dir)

    # 2. 读取索引文件
    if not os.path.exists(index_file):
        print(f"错误: 找不到索引文件 {index_file}")
        return

    with open(index_file, 'r', encoding='utf-8') as f:
        rules_index = json.load(f)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"开始爬取详情页，共 {len(rules_index)} 个配置项...")

    for rule_name, info in rules_index.items():
        url = info['url']
        save_path = os.path.join(rules_dir, f"{rule_name}.json")

        # 断点续爬：如果文件已存在则跳过
        if os.path.exists(save_path):
            continue

        print(f"正在抓取: {rule_name} ...")

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')

            def get_section_content(section_id):
                header = soup.find('h2', id=section_id)
                if not header:
                    return None

                parts = []
                # 遍历 h2 之后的所有兄弟节点
                for sibling in header.find_next_siblings():
                    if sibling.name == 'h2':  # 遇到下一个大标题停止
                        break

                    # 过滤掉代码块中的按钮文字和行号
                    if sibling.name == 'div' and (
                            'code-wrapper' in sibling.get('class', []) or 'incorrect' in sibling.get('class',
                                                                                                     []) or 'correct' in sibling.get(
                            'class', [])):
                        # 找到 pre 标签
                        pre = sibling.find('pre')
                        if pre:
                            # 移除内部的 line-numbers-wrapper（行号）
                            ln = pre.find('div', class_='line-numbers-wrapper')
                            if ln: ln.decompose()
                            parts.append(pre.get_text().strip())
                    elif sibling.name == 'ul' or sibling.name == 'ol':
                        # 处理列表
                        items = [f"- {li.get_text(strip=True)}" for li in sibling.find_all('li')]
                        parts.append("\n".join(items))
                    else:
                        # 处理普通段落
                        txt = sibling.get_text(strip=True)
                        # 排除掉 "Open in Playground" 这种按钮文字
                        if txt and txt != "Open in Playground":
                            parts.append(txt)

                return "\n\n".join(parts).strip()

            # 3. 提取 Rule Details 和 Options
            rule_details = get_section_content("rule-details")
            options_content = get_section_content("options")

            # 4. 组织内容格式
            # 按照要求：description 包含 "Description\n\n" 前缀
            # 如果没有 Options，则置为指定字符串
            final_data = {
                rule_name: {
                    "description": f"Description\n\n{rule_details if rule_details else info['description']}",
                    "option": options_content if options_content else "This rule has no specific options."
                }
            }

            # 5. 保存单个 JSON 文件
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, ensure_ascii=False, indent=4)

            # 适当休眠，避免请求过快
            time.sleep(0.3)

        except Exception as e:
            print(f"抓取 {rule_name} 失败: {e}")

    print("详情页抓取完成！")


if __name__ == "__main__":
    scrape_eslint_rules_details()