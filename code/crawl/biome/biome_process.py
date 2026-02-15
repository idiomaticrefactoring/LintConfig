import os
import json
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# --- 配置 ---
BASE_INDEX_URL = "https://biomejs.dev/linter/javascript/rules/"
BASE_DOMAIN = "https://biomejs.dev"
OUTPUT_DIR = os.path.join("Biome", "JavaScript")
RULES_DIR = os.path.join(OUTPUT_DIR, "rules")
INDEX_FILE = os.path.join(OUTPUT_DIR, "BiomeIndex.json")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


# --- 工具函数：带重试的请求 ---
def fetch_with_retry(url, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code == 429:
                wait = (attempt + 1) * 5
                print(f"  [Wait] 服务器限流 (429)，等待 {wait}s...")
                time.sleep(wait)
                continue
            response.raise_for_status()
            return response.text
        except (requests.exceptions.RequestException, Exception) as e:
            wait = (attempt + 1) * 2
            if attempt < max_retries - 1:
                print(f"  [Retry] 请求失败: {str(e)[:50]}... 正在尝试第 {attempt + 2} 次 (等待{wait}s)")
                time.sleep(wait)
            else:
                print(f"  [Failed] 无法访问: {url}")
                return None


# --- 工具函数：清洗 Options 内容 ---
def clean_biome_options(text):
    if not text or text == "This rule has no specific options.":
        return text

    # 1. 移除特定的噪声模式
    noise_patterns = [
        r"The rule supports the following options:",
        r"Both options.*?\(e\.g\.<Control\.Input>\)\.",
        r"biome\.json"
    ]
    for pattern in noise_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)

    # 2. 移除行号数字 (针对残留的数字进行兜底清洗)
    text = re.sub(r'\d+(?=\s*[\{\}\"\[\]])', '', text)

    # 3. 格式化输出
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return "\n".join(lines)


# --- 核心逻辑 1：爬取索引 ---
def scrape_index():
    print(f"正在获取索引信息: {BASE_INDEX_URL}")
    html = fetch_with_retry(BASE_INDEX_URL)
    if not html: return None

    soup = BeautifulSoup(html, 'html.parser')
    index_map = {}
    tables = soup.find_all('table')

    for table in tables:
        for row in table.find_all('tr')[1:]:  # 跳过表头
            cols = row.find_all('td')
            if len(cols) >= 2:
                a_tag = cols[0].find('a')
                if a_tag:
                    name = a_tag.get_text(strip=True)
                    url = urljoin(BASE_DOMAIN, a_tag.get('href'))
                    # 这里的摘要来自索引页表格
                    summary = cols[1].get_text(strip=True)
                    index_map[name] = {
                        "description": summary,
                        "url": url
                    }
    return index_map


# --- 核心逻辑 2：爬取详情 ---
def get_rule_details(url, rule_name):
    html = fetch_with_retry(url)
    if not html: return None, None

    soup = BeautifulSoup(html, 'html.parser')

    def get_section_text(target_id):
        h2_tag = soup.find('h2', id=target_id)
        if not h2_tag: return None

        # 寻找包装容器
        header_wrapper = h2_tag.find_parent('div', class_='sl-heading-wrapper') or h2_tag
        content_blocks = []

        for sibling in header_wrapper.find_next_siblings():
            # 遇到下一个大标题 level-h2 则停止
            if sibling.name == 'div' and 'level-h2' in sibling.get('class', []):
                break

            # 处理代码块：精准提取 .code 避开行号 .ln
            if sibling.get('class') and 'expressive-code' in sibling.get('class'):
                # 记录文件名如 biome.json
                caption = sibling.find('figcaption')
                if caption: content_blocks.append(caption.get_text().strip())

                # 核心改进：只拿代码行内容
                code_parts = sibling.select('.code')
                if code_parts:
                    content_blocks.append("\n".join([c.get_text() for c in code_parts]))
            elif sibling.name == 'ul':
                for li in sibling.find_all('li'):
                    content_blocks.append(f"- {li.get_text(strip=True)}")
            else:
                txt = sibling.get_text(strip=True)
                if txt: content_blocks.append(txt)

        return "\n\n".join(content_blocks)

    desc = get_section_text("description")
    opts = get_section_text("options")
    return desc, opts


# --- 主函数 ---
def main():
    # 1. 准备目录
    os.makedirs(RULES_DIR, exist_ok=True)

    # 2. 爬取并保存索引
    index_data = scrape_index()
    if not index_data:
        print("无法获取索引数据，程序退出。")
        return

    # 3. 逐条处理详情
    total = len(index_data)
    print(f"开始处理详情，共 {total} 条规则...")

    for i, (name, info) in enumerate(index_data.items()):
        save_path = os.path.join(RULES_DIR, f"{name}.json")

        # 断点续爬检查
        if os.path.exists(save_path):
            continue

        print(f"[{i + 1}/{total}] 正在处理: {name}")
        raw_desc, raw_opts = get_rule_details(info['url'], name)

        if raw_desc is None:
            print(f"  [Skip] 无法获取 {name} 的详细页面")
            continue

        # 清洗 Options
        cleaned_options = clean_biome_options(raw_opts) if raw_opts else "This rule has no specific options."

        # 组织单个规则内容
        rule_file_content = {
            name: {
                "description": f"Description\n\n{raw_desc}",
                "option": cleaned_options
            }
        }

        # 写入详情文件
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(rule_file_content, f, ensure_ascii=False, indent=4)

        # 频率控制
        time.sleep(0.5)

    # 4. 写入最终索引文件 (更新 description 为索引页摘要)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=4)

    print(f"\n任务全部完成！")
    print(f"- 索引文件: {INDEX_FILE}")
    print(f"- 规则详情: {RULES_DIR}")


if __name__ == "__main__":
    main()