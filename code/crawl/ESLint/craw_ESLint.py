import requests
from bs4 import BeautifulSoup
import json
import os


def scrape_eslint_rules():
    url = "https://eslint.org/docs/latest/rules/"
    base_url = "https://eslint.org"

    # 1. 创建 ESLint 文件夹
    output_dir = "ESLint"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print(f"正在访问: {url} ...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        rules_index = {}

        # 2. 查找所有的 <article class="rule">
        # 这涵盖了 Possible Problems, Suggestions, Layout, Deprecated 等所有分类
        articles = soup.find_all('article', class_='rule')

        for article in articles:
            # --- 提取规则名称和 URL ---
            name_wrapper = article.find(class_='rule__name')
            if not name_wrapper:
                # 兼容一些特殊结构的 rule 元素
                name_wrapper = article.find('a', class_='rule__name')

            if not name_wrapper:
                continue

            # 克隆节点以防修改原始 soup，去除内部状态标签（如 "deprecated" 标志）
            import copy
            temp_name_node = copy.copy(name_wrapper)
            status_span = temp_name_node.find('span', class_='rule__status')
            if status_span:
                status_span.decompose()  # 移除 "deprecated" 或 "removed" 文字

            rule_name = temp_name_node.get_text(strip=True)

            # --- 提取 URL ---
            if name_wrapper.name == 'a':
                relative_url = name_wrapper.get('href', '')
            else:
                # 如果 rule__name 是 p 标签（通常见于 deprecated 列表），寻找其内部的链接或手动拼接
                link = name_wrapper.find('a')
                relative_url = link.get('href', '') if link else f"/docs/latest/rules/{rule_name}"

            full_url = f"{base_url}{relative_url}" if relative_url.startswith('/') else relative_url

            # --- 提取描述 ---
            desc_tag = article.find('p', class_='rule__description')
            # 过滤掉描述内部可能存在的 visually-hidden 或多余空白
            description = desc_tag.get_text(strip=True) if desc_tag else ""

            # 3. 填充字典
            rules_index[rule_name] = {
                "description": description,
                "url": full_url
            }

        # 4. 保存为 JSON
        file_path = os.path.join(output_dir, "ESLintIndex.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(rules_index, f, ensure_ascii=False, indent=4)

        print(f"成功抓取 {len(rules_index)} 条规则！")
        print(f"文件已存至: {file_path}")

    except Exception as e:
        print(f"抓取失败: {e}")


if __name__ == "__main__":
    scrape_eslint_rules()