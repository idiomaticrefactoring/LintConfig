import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re

# --- 配置参数 ---
BASE_URL = "https://clang.llvm.org/extra/clang-tidy/checks/"
INDEX_FILE = os.path.join("ClangTidy", "ClangTidyIndex.json")
RULES_DIR = os.path.join("ClangTidy", "rules")
MAX_RETRIES = 5
RETRY_DELAY = 3

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def clean_node_text(node):
    """
    清洗节点文本：移除 Sphinx 的锚点符号 ¶，保留合理的换行。
    """
    if not node:
        return ""
    # 移除所有的 headerlink (即那个 ¶ 符号所在的超链接)
    for link in node.find_all('a', class_='headerlink'):
        link.decompose()

    # 获取文本并移除残留的 ¶
    text = node.get_text(separator="\n", strip=False)
    lines = [line.replace('¶', '').strip() for line in text.split('\n')]
    return "\n".join([l for l in lines if l])


def get_rule_details_and_options(url, rule_name):
    """
    访问 Clang-Tidy 规则详情页，提取 Description 和 Options
    """
    for attempt in range(MAX_RETRIES):
        try:
            time.sleep(0.3)
            resp = requests.get(url, headers=HEADERS, timeout=20)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'html.parser')

            # 1. 定位主容器
            # 现代 Clang-Tidy 文档结构: <section id="rule-name">
            content_area = soup.find('section', id=rule_name)
            if not content_area:
                # 兼容性备选
                content_area = soup.find('div', role='main') or soup.find('div', class_='section')

            if not content_area:
                return None, None

            description_parts = []
            options_parts = []
            found_options_start = False

            # 2. 遍历 content_area 的子节点
            # 注意：新版 Sphinx 会把 Options 放在嵌套的 <section id="options-..."> 里
            for child in content_area.find_all(recursive=False):
                if child.name == 'h1':
                    continue

                # 检测是否进入 Options 区域
                # 逻辑：如果是标题且包含 options，或者是子 section 且 id/标题包含 options
                child_id = child.get('id', '').lower()
                child_text = child.get_text().lower()

                if (child.name in ['h2', 'h3', 'section']) and ('options' in child_id or 'options' in child_text):
                    found_options_start = True
                    # 如果是子 section，其内容都在内部，直接提取
                    if child.name == 'section':
                        options_parts.append(clean_node_text(child))
                        continue

                # 3. 收集内容
                content_text = clean_node_text(child)
                if not content_text:
                    continue

                if found_options_start:
                    options_parts.append(content_text)
                else:
                    # 过滤掉详情页重复的 "Offers fixes" 提示
                    if content_text.lower().startswith("offers fixes"):
                        continue
                    description_parts.append(content_text)

            desc_final = "\n\n".join(description_parts).strip()
            opt_final = "\n\n".join(options_parts).strip()

            return desc_final or "No detailed description found.", opt_final

        except Exception as e:
            wait = RETRY_DELAY * (attempt + 1)
            if attempt < MAX_RETRIES - 1:
                print(f"  [Retry] {rule_name} 失败: {e}. {wait}s 后重试...")
                time.sleep(wait)
            else:
                print(f"  [Fatal] {rule_name} 抓取彻底失败: {e}")

    return None, None


def enrich_clang_tidy():
    if not os.path.exists(RULES_DIR):
        os.makedirs(RULES_DIR)

    if not os.path.exists(INDEX_FILE):
        print(f"错误: 找不到索引文件 {INDEX_FILE}，请先运行索引爬取脚本。")
        return

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_data = json.load(f)

    total = len(index_data)
    print(f"开始爬取 Clang-Tidy 详情，共 {total} 条规则...")

    for i, (rule_name, info) in enumerate(index_data.items()):
        save_path = os.path.join(RULES_DIR, f"{rule_name}.json")

        # 因为你删除了 rules 文件夹，这里会重新抓取所有内容
        if os.path.exists(save_path):
            continue

        print(f"[{i + 1}/{total}] 处理中: {rule_name}")

        desc, opts = get_rule_details_and_options(info['url'], rule_name)

        if desc is None:
            # 这种通常是 404 或 结构完全对不上的规则
            final_desc = "FAILED_TO_FETCH"
            final_opts = ""
        else:
            final_desc = desc
            final_opts = opts

        # 整理 Option 字段内容
        option_field = "Static analysis (Clang-Tidy) options are configured via .clang-tidy file.\n\n"
        if final_opts:
            option_field += final_opts
        else:
            option_field += "This rule has no specific options."

        # 组织最终 JSON
        final_json = {
            rule_name: {
                "description": f"Description\n\n{final_desc}",
                "option": option_field
            }
        }

        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(final_json, f, ensure_ascii=False, indent=4)

    print("\n[Done] 所有规则已重新组织到 ClangTidy/rules/ 目录下。")


if __name__ == "__main__":
    enrich_clang_tidy()