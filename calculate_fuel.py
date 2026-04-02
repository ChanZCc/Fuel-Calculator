# 计算油费脚本 - 支持自动获取当地油价
import requests
from bs4 import BeautifulSoup
import json

def get_fuel_price_from_qukuaiyouhua():
    """
    从 http://www.qiyoujiage.com/guangdong.shtml 获取广东省最新油价（92号汽油）
    :return: 92号汽油价格（元/升）
    """
    try:
        url = "http://www.qiyoujiage.com/guangdong.shtml"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)   # 设置超时时间，避免长时间等待
        response.encoding = 'utf-8'  # 确保正确解析中文页面
        soup = BeautifulSoup(response.text, 'html.parser')  # 解析页面内容
        # 直接查找92号汽油价格
        dls = soup.find_all('dl')   # 92号汽油价格通常在dl标签中，dt标签包含油品名称，dd标签包含价格
        for dl in dls:
            dt = dl.find('dt')
            dd = dl.find('dd')
            if dt and dd and '92#汽油' in dt.get_text():
                price_text = dd.get_text().strip()
                try:
                    price = float(price_text)
                    return price
                except Exception:
                    continue
        print("未能在页面中找到92号汽油价格")
    except Exception as e:
        print(f"爬虫获取油价失败: {e}")
    return None


def calculate_fuel_cost(distance, fuel_efficiency, fuel_price):
    """
    计算油费
    distance: 行驶距离（公里）
    fuel_efficiency: 油耗（L/100km）
    fuel_price: 燃油价格（元/升）
    :return: 油费总成本（元）
    """
    # 计算所需燃油量
    fuel_needed = (distance * fuel_efficiency) / 100
    # 计算总油费
    total_cost = fuel_needed * fuel_price
    return total_cost

# 示例使用
if __name__ == "__main__":
    distance = 120  # 行驶距离（公里）
    fuel_efficiency = 6.2  # 油耗（L/100km）

    # 方案1: 爬取广东92号汽油油价
    fuel_price = get_fuel_price_from_qukuaiyouhua()
    if fuel_price:
        print(f"获取到的广东92号汽油油价: {fuel_price} 元/升")
    else:
        print("未能获取到广东92号汽油油价，使用本地默认油价。")
        fuel_price = 7.59

    cost = calculate_fuel_cost(distance, fuel_efficiency, fuel_price)
    print(f"行驶 {distance} 公里需要的油费总成本为: {cost:.2f} 元")
