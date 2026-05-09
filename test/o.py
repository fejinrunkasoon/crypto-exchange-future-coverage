from curl_cffi import requests

def fetch_kcex_pro():
    url = "https://www.kcex.com/fapi/v1/contract/kline_24h_all"
    
    # 模拟 Chrome 浏览器指纹
    response = requests.get(
        url, 
        impersonate="chrome110", # 核心：模拟 Chrome 110 的底层指纹
        headers={
            "Referer": "https://www.kcex.com/zh-TW/markets",
            "Accept": "application/json, text/plain, */*",
        },
        timeout=15
    )

    if response.status_code == 200:
        data = response.json()
        symbols = [item['sb'] for item in data['data']]
        print(f"✅ 穿透成功！总合约数: {len(symbols)}")
        return symbols
    else:
        print(f"依然失败，状态码: {response.status_code}")

fetch_kcex_pro()