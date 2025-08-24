
import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = [
    'https://api.uouin.com/cloudflare.html',
    'https://ip.164746.xyz'
]

# 正则表达式匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 删除旧文件（如果存在）
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 收集所有IP地址
all_ips = []
for url in urls:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据URL选择解析策略
        elements = soup.find_all('tr') if '164746.xyz' in url else soup.find_all('tr')
        
        for element in elements:
            ip_matches = re.findall(ip_pattern, element.get_text())
            all_ips.extend(ip_matches)
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

# 写入前30个IP到文件
with open('ip.txt', 'w') as file:
    for ip in all_ips[:30]:
        file.write(ip + '\n')

print(f'成功保存{min(30, len(all_ips))}个IP到ip.txt')
