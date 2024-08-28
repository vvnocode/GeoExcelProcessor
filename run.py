import pandas as pd
import requests
import time
import configparser

# 读取配置文件
config = configparser.ConfigParser()
# config.read('config.ini')
config.read('config.ini', encoding='utf-8-sig')

api_key = config['settings']['api_key']
address_prefix = config['settings']['address_prefix']
input_file = config['settings']['input_file']
output_file = config['settings']['output_file']


def get_location_and_address(address):
    if address_prefix in address:
        full_address = address
    else:
        full_address = f"{address_prefix}{address}"
    url = f"https://restapi.amap.com/v3/geocode/geo?address={full_address}&output=json&key={api_key}"
    response = requests.get(url)
    data = response.json()
    location, detailed_address = None, None
    if data['status'] == '1' and data['geocodes']:
        if len(data['geocodes']) > 1:
            print(f"地址: {full_address}\n找到多个匹配地址:")
            for idx, geocode in enumerate(data['geocodes']):
                print(f"{idx}. {geocode['formatted_address']}")
            choice = int(input("请输入所需地址的索引: "))
            geocode = data['geocodes'][choice]
        else:
            geocode = data['geocodes'][0]
        location = geocode['location']
        detailed_address = geocode['formatted_address']
    return location, detailed_address


def get_distance_duration(origin, destination):
    url = f"https://restapi.amap.com/v3/distance?origins={origin}&destination={destination}&output=json&key={api_key}"
    response = requests.get(url)
    data = response.json()
    distance, duration = None, None
    if data['status'] == '1' and data.get('results'):
        distance = float(data['results'][0]['distance']) / 1000  # 转换为公里
        duration = float(data['results'][0]['duration']) / 3600  # 转换为小时
    return distance, duration


def process_excel(input_file, output_file):
    df = pd.read_excel(input_file)

    # 处理起点
    df[['起点经纬度', '起点详细地址']] = df['始发地'].apply(lambda x: pd.Series(get_location_and_address(x)))

    # 处理目的地
    df[['目的地经纬度', '目的地详细地址']] = df['目的地'].apply(lambda x: pd.Series(get_location_and_address(x)))

    # 为了避免高德API的流量限制，添加延时
    time.sleep(1)

    # 获取距离和时间
    result = df.apply(lambda row: get_distance_duration(row['起点经纬度'], row['目的地经纬度']), axis=1)
    df['距离（公里）'] = result.apply(lambda x: x[0] if x else None)
    df['行驶时长（小时）'] = result.apply(lambda x: x[1] if x else None)

    df.to_excel(output_file, index=False, engine='openpyxl')


if __name__ == "__main__":
    process_excel(input_file, output_file)
