import json
import os
import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin

# --- 配置参数 ---
MAX_RETRIES = 5
BACKOFF_FACTOR = 2
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 语言配置： 键为网页URL标识，值为生成的文件夹名称
LANG_CONFIG = {
    "apex": "Apex",
    "html": "Html",
    "java": "Java",
    "jsp": "JSP",
    "ecmascript": "JavaScript",
    "kotlin": "Kotlin",
    "pom": "MavenPOM",
    "modelica": "Modelica",
    "plsql": "PLSQL",
    "visualforce": "Salesforce_Visual_force",
    "swift": "Swift",
    "velocity": "VTL",
    "xml": "XML",
    "xsl": "XSL"
}
# 不知道为什么JavaScript在官网的url中是ecmascript，反直觉

BASE_URL = "https://pmd.github.io/pmd/"


def format_table_to_text(table_tag):
    """将 Properties 表格转换为文本"""
    if not table_tag: return ""
    rows = []
    thead = table_tag.find('thead')
    if thead:
        headers = [th.get_text(strip=True) for th in thead.find_all('th')]
        rows.append("\t".join(headers))
    tbody = table_tag.find('tbody')
    if tbody:
        for tr in tbody.find_all('tr'):
            cols = [td.get_text(strip=True) for td in tr.find_all('td')]
            rows.append("\t".join(cols))
    return "\n".join(rows)


def get_soup_with_retry(url):
    """带重试机制的请求函数"""
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, 'html.parser')
        except Exception as e:
            wait = BACKOFF_FACTOR ** attempt
            print(f"  [Retry] 访问 {url} 失败: {e}. {wait}s后重试...")
            time.sleep(wait)
    return None


def scrape_language_index(lang_slug, folder_name):
    """抓取语言首页索引"""
    index_url = f"{BASE_URL}pmd_rules_{lang_slug}.html"
    print(f"\n>>> 正在抓取索引: {folder_name} ({index_url})")

    soup = get_soup_with_retry(index_url)
    if not soup: return None

    rules_index = {}
    content_div = soup.find('div', class_='post-content')
    if not content_div: return None

    toc_div = content_div.find('div', id='toc')
    for li in content_div.find_all('li'):
        if toc_div and toc_div.contains(li): continue

        a_tag = li.find('a')
        if not a_tag or not a_tag.get('href'): continue

        rule_name = a_tag.get_text(strip=True)
        relative_url = a_tag.get('href')
        full_url = urljoin(BASE_URL, relative_url)

        full_text = li.get_text(strip=True)
        description = full_text.split(":", 1)[1].strip() if ":" in full_text else ""

        rules_index[rule_name] = {
            "description": description,
            "url": full_url
        }

    # 保存索引文件
    os.makedirs(folder_name, exist_ok=True)
    index_path = os.path.join(folder_name, f"PMD_{folder_name}Index.json")
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(rules_index, f, ensure_ascii=False, indent=4)

    return rules_index


def enrich_language_details(folder_name, rules_index):
    """补全详情页内容并分拆文件"""
    rules_dir = os.path.join(folder_name, "rules")
    os.makedirs(rules_dir, exist_ok=True)

    # 按组页面分类，减少请求次数
    url_groups = {}
    for name, info in rules_index.items():
        base_page = info['url'].split('#')[0]
        if base_page not in url_groups: url_groups[base_page] = []
        url_groups[base_page].append(name)

    for base_page, rule_names in url_groups.items():
        # 检查是否还有需要抓取的
        if all(os.path.exists(os.path.join(rules_dir, f"{n}.json")) for n in rule_names):
            continue

        print(f"  正在处理组页面: {base_page}")
        soup = get_soup_with_retry(base_page)
        if not soup: continue

        for rule_name in rule_names:
            save_path = os.path.join(rules_dir, f"{rule_name}.json")
            if os.path.exists(save_path): continue

            header = soup.find('h2', id=lambda x: x and x.lower() == rule_name.lower())
            if not header: continue

            desc_parts = []
            options_text = "This rule has no specific options."

            for sibling in header.find_next_siblings():
                if sibling.name == 'h2': break
                if sibling.name == 'p':
                    txt = sibling.get_text(strip=True)
                    if any(txt.startswith(x) for x in ["Since:", "Priority:", "This rule is defined by"]): continue
                    if "following properties" in txt: continue
                    if sibling.find('a', href=re.compile("github\.com")): continue
                    desc_parts.append(txt)
                if sibling.name == 'table':
                    prev = sibling.find_previous_sibling('p')
                    if prev and "properties" in prev.get_text().lower():
                        options_text = format_table_to_text(sibling)

            full_desc = "\n\n".join(desc_parts).strip() or rules_index[rule_name]['description']

            final_data = {
                rule_name: {
                    "description": f"Description\n\n{full_desc}",
                    "option": options_text
                }
            }

            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(final_data, f, ensure_ascii=False, indent=4)

        time.sleep(0.5)


def main():
    print("=== PMD Universal Crawler Starting ===")

    for slug, folder in LANG_CONFIG.items():
        # 1. 抓取索引
        rules_index = scrape_language_index(slug, folder)

        if rules_index:
            # 2. 补全详情并生成规则文件
            print(f"  正在抓取 {folder} 的规则详情...")
            enrich_language_details(folder, rules_index)
            print(f"  {folder} 处理完成。")
        else:
            print(f"  [Warning] 无法获取 {folder} 的索引内容。")

    print("\n=== All Tasks Completed ===")


if __name__ == "__main__":
    main()