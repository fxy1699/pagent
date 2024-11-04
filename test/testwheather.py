import requests

def get_realtime_weather(locationid, key):
    # 构建请求URL
    url = f"https://devapi.qweather.com/v7/weather/now?location={locationid}&key={key}"
    
    # 发送GET请求
    response = requests.get(url)
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析JSON数据
        data = response.json()
        
        # 提取并打印天气信息
        if data['code'] == "200":
            now = data['now']
            print(f"观测时间: {now['obsTime']}")
            print(f"温度: {now['temp']}°C")
            print(f"体感温度: {now['feelsLike']}°C")
            print(f"天气状况: {now['text']}")
            print(f"风向: {now['windDir']}，风速: {now['windSpeed']}公里/小时")
            print(f"相对湿度: {now['humidity']}%")
            print(f"大气压强: {now['pressure']}百帕")
            print(f"能见度: {now['vis']}公里")
            print(f"云量: {now['cloud']}%")
            print(f"露点温度: {now['dew']}°C")
        else:
            print(f"请求失败，错误码: {data['code']}")
    else:
        print(f"请求失败，HTTP状态码: {response.status_code}")

def get_city_id(city_name, adm, range,token):
    # 构建请求URL
    url = "https://geoapi.qweather.com/v2/city/lookup"
    
    # 构建请求参数
    params = {
        "location": city_name,
        "adm": adm,
        "range": range,
        "key": token,  # 请替换为你的API密钥
    }
    
    # 发送GET请求
    response = requests.get(url, params=params)
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析JSON数据
        data = response.json()
        
        # 提取并打印城市ID
        if data['code'] == "200" and data['location']:
            for city in data['location']:
                print(f"城市名称: {city['name']}")
                print(f"城市ID: {city['id']}")
                print(f"纬度: {city['lat']}")
                print(f"经度: {city['lon']}")
                print(f"上级行政区划: {city['adm2']}")
                print(f"一级行政区域: {city['adm1']}")
                print(f"国家: {city['country']}")
                print(f"时区: {city['tz']}")
                print(f"UTC偏移量: {city['utcOffset']}")
                print(f"是否夏令时: {city['isDst']}")
                print(f"地区类型: {city['type']}")
                print(f"地区评分: {city['rank']}")
                print(f"天气预报链接: {city['fxLink']}\n")
        else:
            print(f"请求失败，错误码: {data['code']}")
    else:
        print(f"请求失败，HTTP状态码: {response.status_code}")

# 使用示例
# 请替换YOUR_KEY为你的API密钥，以及将location替换为你想查询的地区LocationID或经纬度
locationid = "jizhou"  # 例如，地区名
key = "e2952b171cd8472287584ea4a00c1d63"  # 替换为你的QWeather API密钥
adm = "tianjin"
range = "cn"
get_city_id(locationid,adm,range,key)
# get_realtime_weather(location, key)