import os
import json
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import time
# 获取cppcheck.xml :
# 指令cppcheck --errorlist --xml > cppcheck_rules.xml
# --- 配置参数 ---
INPUT_FILE = 'cppcheck_rules.xml'
BASE_DIR = 'Cppcheck'
RULES_DIR = os.path.join(BASE_DIR, 'rules')
MAX_RETRIES = 5  # 最大重试次数
RETRY_DELAY = 2  # 基础重试延迟（秒）

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_cwe_url(cwe_id):
    """生成 CWE 链接"""
    if cwe_id:
        return f"https://cwe.mitre.org/data/definitions/{cwe_id}.html"
    return "https://sourceforge.net/p/cppcheck/wiki/ListOfChecks/"


def fetch_detailed_description(url, fallback_msg, rule_id):
    """
    访问网页爬取详细描述。包含重试逻辑。
    """
    if "cwe.mitre.org" not in url:
        return fallback_msg

    for attempt in range(MAX_RETRIES):
        try:
            # 基础礼貌延迟，避免请求过频
            time.sleep(0.5)

            resp = requests.get(url, headers=HEADERS, timeout=15)

            # 如果服务器返回 429 或其他非 200 状态，抛出异常进入重试
            resp.raise_for_status()

            soup = BeautifulSoup(resp.content, 'html.parser')

            # 定位 CWE 页面中的 Description 部分
            desc_div = soup.find('div', id='Description')
            if desc_div:
                detail_text = desc_div.find('div', class_='detail')
                if detail_text:
                    return detail_text.get_text(strip=True)

            # 如果解析不到特定的 div，返回 fallback
            return fallback_msg

        except (requests.exceptions.RequestException, Exception) as e:
            wait_time = RETRY_DELAY * (2 ** attempt)  # 指数退避：2, 4, 8...
            if attempt < MAX_RETRIES - 1:
                print(f"  [Retry] {rule_id} 访问失败: {e}. {wait_time}s 后进行第 {attempt + 2} 次尝试...")
                time.sleep(wait_time)
            else:
                print(f"  [Error] {rule_id} 达到最大重试次数，使用本地描述。错误原因: {e}")
                return fallback_msg


def process_cppcheck():
    if not os.path.exists(RULES_DIR):
        os.makedirs(RULES_DIR)

    if not os.path.exists(INPUT_FILE):
        print(f"错误: 找不到输入文件 {INPUT_FILE}")
        return

    try:
        tree = ET.parse(INPUT_FILE)
        root = tree.getroot()
        errors_node = root.find('errors')
        errors = errors_node.findall('error') if errors_node is not None else root.findall('error')

        index_data = {}
        total = len(errors)
        print(f"开始处理 Cppcheck 规则，共 {total} 条...")

        for i, error in enumerate(errors):
            rule_id = error.get('id')
            if not rule_id: continue

            # --- 断点续爬：如果文件已存在，则加载它并填充索引，然后跳过网络请求 ---
            save_path = os.path.join(RULES_DIR, f"{rule_id}.json")

            msg = error.get('msg', '')
            verbose = error.get('verbose', '')
            severity = error.get('severity', 'unknown')
            cwe = error.get('cwe', '')
            inconclusive = error.get('inconclusive', 'false')
            url = get_cwe_url(cwe)

            # 无论文件是否存在，都先填充索引数据
            index_data[rule_id] = {
                "description": msg,
                "url": url
            }

            if os.path.exists(save_path):
                # print(f"[{i + 1}/{total}] 跳过已存在: {rule_id}")
                continue

            print(f"[{i + 1}/{total}] 正在处理: {rule_id}")

            # 1. 爬取更详细的 Description
            detailed_desc = fetch_detailed_description(url, verbose if verbose else msg, rule_id)

            # 2. 组织 Option 字段
            option_info = (
                "Static analysis does not have options.\n\n"
                f"Severity: {severity}\n"
                f"CWE: {cwe if cwe else 'N/A'}\n"
                f"Inconclusive: {inconclusive}"
            )

            symbols = [s.text for s in error.findall('symbol') if s.text]
            if symbols:
                option_info += f"\nRelated Symbols: {', '.join(symbols)}"

            # 3. 组织最终内容
            rule_content = {
                rule_id: {
                    "description": f"Description\n\n{detailed_desc}",
                    "option": option_info
                }
            }

            # 4. 写入规则文件
            with open(save_path, 'w', encoding='utf-8') as rf:
                json.dump(rule_content, rf, ensure_ascii=False, indent=4)

        # 5. 写入索引文件
        with open(os.path.join(BASE_DIR, "cppcheckIndex.json"), 'w', encoding='utf-8') as ifile:
            json.dump(index_data, ifile, ensure_ascii=False, indent=4)

        print(f"\n全部处理完成！文件存放在 '{BASE_DIR}' 目录下。")

    except Exception as e:
        print(f"解析过程中发生崩溃: {e}")


if __name__ == "__main__":
    process_cppcheck()