import requests
from bs4 import BeautifulSoup
#from selenium import webdriver

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"网页获取失败: {str(e)}")
        return None

def parse_html(html):
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 根据实际网页结构调整选择器
    table = soup.find('tbody')  # 可能需要修改类名
    if not table:
        print("未找到数据表格！请检查网页结构")
        return []
    
    results = []
    for row in table.select('tr'):  # 跳过表头
        cols = row.find_all('td')
        if len(cols) < 6:
            continue
        
        # 提取各字段（根据实际列顺序调整）
        line_name = cols[0].text.strip()
        ip_address = cols[1].text.strip()
        data_center = cols[-2].text.strip()  # 假设数据中心在倒数第二列
        
        results.append(f"{ip_address} #{line_name}-{data_center}")
    
    return results

def save_to_file(data):
    with open('ipv4.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(set(data))))
    print(f"成功保存 {len(data)} 条数据到 ipv4.txt")

if __name__ == '__main__':
    url = "https://www.wetest.vip/page/cloudflare/address_v4.html"
    html = get_html(url)
    data = parse_html(html)
    
    if data:
        save_to_file(data)
    else:
        print("无有效数据可保存")