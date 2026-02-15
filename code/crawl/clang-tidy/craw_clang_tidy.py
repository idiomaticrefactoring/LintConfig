import requests
from bs4 import BeautifulSoup
import json
import os
import time

# --- 配置 ---
BASE_URL = "https://clang.llvm.org/extra/clang-tidy/checks/"
INDEX_URL = BASE_URL + "list.html"
OUTPUT_DIR = "ClangTidy"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "ClangTidyIndex.json")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_detail_description(url, rule_name):
    """
    访问具体规则页面，提取核心介绍内容
    """
    try:
        # 适当休眠，防止请求过快
        time.sleep(0.1)
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return "No description available."

        detail_soup = BeautifulSoup(resp.text, 'html.parser')

        # 1. 尝试查找新版结构：以规则名为 id 的 section 标签
        # 例如: <section id="abseil-cleanup-ctad">
        content_area = detail_soup.find('section', id=rule_name)

        # 2. 如果没找到，尝试旧版结构：class 为 section 的 div
        if not content_area:
            content_area = detail_soup.find('div', class_='section')

        # 3. 兜底逻辑：查找页面主要内容区域
        if not content_area:
            content_area = detail_soup.find('div', role='main')

        if content_area:
            # 找到 content_area 下的所有段落
            # 我们需要的是第一个非空的、且不是“Offers fixes”提示的段落
            paragraphs = content_area.find_all('p', recursive=True)
            for p in paragraphs:
                text = p.get_text().strip()
                # 移除 Sphinx 可能带入的锚点符号 ¶
                text = text.replace('¶', '')

                # 过滤掉空的段落或自动生成的“修复”提示语
                if text and not text.lower().startswith("offers fixes"):
                    # 返回第一段话
                    return text

        return "No description available."
    except Exception as e:
        print(f"  [Warning] Fetching description failed for {url}: {e}")
        return "Failed to fetch description."


def scrape_clang_tidy_index():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"正在访问 Clang-Tidy 列表页: {INDEX_URL}")
    try:
        response = requests.get(INDEX_URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        index_data = {}
        # 定位 tbody 中的所有 tr
        rows = soup.select('tbody tr')
        total = len(rows)
        print(f"发现 {total} 条规则，开始抓取详细描述...")

        for i, row in enumerate(rows):
            cols = row.find_all('td')
            if not cols:
                continue

            # 提取规则名称和相对 URL
            a_tag = cols[0].find('a')
            if not a_tag:
                continue

            rule_name = a_tag.get_text(strip=True)
            relative_href = a_tag.get('href')

            # 拼接完整 URL
            # 某些链接可能已经是绝对路径或不同格式，这里做个简单兼容
            if relative_href.startswith('http'):
                full_url = relative_href
            else:
                full_url = BASE_URL + relative_href

            # 打印进度
            print(f"[{i + 1}/{total}] 正在抓取描述: {rule_name}")

            # 获取详细描述（传入 rule_name 以便精准定位 ID）
            description = get_detail_description(full_url, rule_name)

            # 组织 JSON 格式
            index_data[rule_name] = {
                "description": description,
                "url": full_url
            }

            # 实时保存，每10个保存一次防止崩掉
            if (i + 1) % 10 == 0:
                with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                    json.dump(index_data, f, ensure_ascii=False, indent=4)

        # 最终保存
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=4)

        print(f"\n抓取完成！索引文件已保存至: {OUTPUT_FILE}")

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    scrape_clang_tidy_index()