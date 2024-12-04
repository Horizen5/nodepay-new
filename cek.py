from curl_cffi import requests as curl_requests
from colorama import Fore, Style, init
from datetime import datetime
import time


init(autoreset=True)

# 打印标题
print(f"{Fore.YELLOW}===========================")
print(f"{Fore.YELLOW} NODEPAY IP账号有效性检查 ")
print(f"{Fore.YELLOW}===========================\n")

# 从文件读取令牌
with open('tokens.txt', 'r') as file:
    tokens = file.readlines()

# 清理令牌中的空白字符
tokens = [token.strip() for token in tokens]

# 显示账户总数
print(f"{Fore.MAGENTA}账户总数: {len(tokens)}\n")

# API端点
url = "https://api.nodepay.org/api/network/device-networks"

# 请求头设置
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Origin": "https://app.nodepay.ai",
    "Referer": "https://app.nodepay.ai/",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Sec-CH-UA": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "Sec-CH-UA-Mobile": "?1",
    "Sec-CH-UA-Platform": "\"Android\""
}

# 查询参数
params = {
    "page": 0,
    "limit": 10,
    "active": "true"
}

line_count = 0

# 遍历处理每个令牌
for index, token in enumerate(tokens):
    # 部分隐藏令牌显示
    token_display = token[:4] + '*' * 10 + token[-4:]
    
    # 打印处理进度
    print(f"{Fore.CYAN}{'='*20}")
    print(f"{Fore.GREEN}正在处理账号: {token_display} ({index + 1}/{len(tokens)})")
    print(f"{Fore.CYAN}{'='*20}")
    
    # 设置认证令牌
    headers["Authorization"] = f"Bearer {token}"
    
    # 发送GET请求
    response = curl_requests.get(url, headers=headers, params=params, impersonate="chrome110")
    
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 处理响应
    if response.status_code == 200:
        data = response.json()
        
        if data["success"]:
            devices = data["data"]
            print(f"{current_time} - 设备总数: {len(devices)}")
            line_count += 1
            
            # 显示每个设备的详细信息
            for device in devices:
                ip_address = device.get("ip_address")
                ip_score = device.get("ip_score", 0)
                total_points = device.get("total_points", 0)
                
                print(f"{current_time} - IP地址: {ip_address}, IP评分: {ip_score}, 总积分: {total_points}")
                line_count += 1
        else:
            print(f"{current_time} - {Fore.RED}请求失败: {data.get('msg')}")
            line_count += 1
    else:
        print(f"{current_time} - {Fore.RED}获取数据失败, 状态码: {response.status_code}")
        line_count += 1
    
    # 发送POST请求
    response = curl_requests.post(url, json=data, headers=headers, impersonate="chrome110")
    
    # 延迟5秒后继续下一个处理
    time.sleep(5)
