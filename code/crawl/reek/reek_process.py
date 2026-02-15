import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
import markdown  # 如果没有请执行 pip install markdown

# --- 配置（使用 Raw 链接避免被封） ---
RAW_BASE_URL = "https://raw.githubusercontent.com/troessner/reek/master/docs/"
INDEX_RAW_URL = RAW_BASE_URL + "Code-Smells.md"
BASE_DIR = "Reek"
RULES_DIR = os.path.join(BASE_DIR, "rules")
INDEX_FILE = os.path.join(BASE_DIR, "ReekIndex.json")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ReekRuleCrawler/1.0'
}


def get_content_with_retry(url):
    """带重试的获取 Raw 内容函数"""
    for attempt in range(5):
        try:
            # 即使是 Raw 链接，也稍微停顿一下
            time.sleep(0.3)
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                return resp.text
            elif resp.status_code == 429:
                wait = 5 * (attempt + 1)
                print(f"  [Wait] 触发频率限制，等待 {wait} 秒...")
                time.sleep(wait)
            else:
                print(f"  [Error] HTTP {resp.status_code} for {url}")
        except Exception as e:
            print(f"  [Retry] 错误: {e}")
            time.sleep(2)
    return None


def scrape_reek():
    if not os.path.exists(RULES_DIR):
        os.makedirs(RULES_DIR)

    print(f"正在抓取 Reek 规则索引 (Raw): {INDEX_RAW_URL}")
    raw_md = get_content_with_retry(INDEX_RAW_URL)
    if not raw_md:
        print("无法获取索引内容，请检查网络或代理设置。")
        return

    # 1. 提取索引页中的规则列表
    # 正则寻找形如 [Attribute-Check](Attribute-Check.md) 的链接
    rule_matches = re.findall(r'\[(.*?)\]\((.*?\.md)\)', raw_md)

    rules_index = {}
    rule_tasks = []

    for name, filename in rule_matches:
        if name in ["Code Smells", "README", "Configuration"]: continue
        full_raw_url = RAW_BASE_URL + filename
        # 记录用于展示的 Github UI 链接（而非 Raw 链接）
        display_url = f"https://github.com/troessner/reek/blob/master/docs/{filename}"
        rule_tasks.append((name, full_raw_url, display_url))

    print(f"共发现 {len(rule_tasks)} 条规则。开始抓取详情...")

    for name, raw_url, display_url in rule_tasks:
        save_path = os.path.join(RULES_DIR, f"{name}.json")
        if os.path.exists(save_path):
            continue

        print(f"处理中: {name}")
        md_text = get_content_with_retry(raw_url)
        if not md_text: continue

        # 将 Markdown 转为 HTML 方便解析
        html_content = markdown.markdown(md_text)
        soup = BeautifulSoup(html_content, 'html.parser')

        description_parts = []
        options_parts = []
        in_config_section = False

        # 2. 遍历解析
        for child in soup.find_all(recursive=False):
            # 判定配置部分的开始
            text = child.get_text().strip()
            if child.name in ['h2', 'h3'] and ('configuration' in text.lower() or 'parameters' in text.lower()):
                in_config_section = True
                continue

            if in_config_section:
                options_parts.append(text)
            else:
                # 过滤掉一级标题
                if child.name == 'h1': continue
                description_parts.append(text)

        # 3. 整合数据
        desc_text = "\n\n".join(description_parts).strip()
        opt_text = "\n\n".join(options_parts).strip() if options_parts else "This rule has no specific options."

        summary = description_parts[0] if description_parts else ""

        rules_index[name] = {
            "description": summary,
            "url": display_url
        }

        # 4. 写入独立 JSON
        final_rule_content = {
            name: {
                "description": f"Description\n\n{desc_text}",
                "option": opt_text
            }
        }

        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(final_rule_content, f, ensure_ascii=False, indent=4)

    # 5. 保存索引
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(rules_index, f, ensure_ascii=False, indent=4)

    print(f"\n全部完成！结果已保存在 '{BASE_DIR}' 目录下。")


if __name__ == "__main__":
    scrape_reek()