import requests
from typing import Dict, Any

# 全局 API 密钥变量
API_KEY = None

def set_api_key(api_key: str) -> None:
    """设置 OpenWeather API 密钥
    
    Args:
        api_key: OpenWeather API 密钥
    """
    global API_KEY
    API_KEY = api_key
    
    if not API_KEY:
        raise ValueError("请提供有效的 OpenWeather API 密钥")

def get_city_coordinates(city_name: str) -> Dict[str, float]:
    """获取城市的地理坐标
    
    Args:
        city_name: 城市名称
        
    Returns:
        包含纬度和经度的字典
        
    Raises:
        ValueError: 如果城市未找到
    """
    if API_KEY is None:
        raise ValueError("API 密钥未设置，请使用 set_api_key 函数设置")
    
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city_name,
        "limit": 1,
        "appid": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if not data:
        raise ValueError(f"未找到城市: {city_name}")
    
    return {
        "lat": data[0]["lat"],
        "lon": data[0]["lon"]
    }

def get_weather_forecast(city: str, days: int = 5) -> Dict[str, Any]:
    """获取指定城市未来几天的天气预报
    
    Args:
        city: 城市名称
        days: 预报天数（最多5天）
    
    Returns:
        包含天气预报信息的字典
    
    Raises:
        ValueError: 如果天数大于5
    """
    if days > 5:
        raise ValueError("最多只能查询5天的天气预报")
    
    # 获取城市坐标
    coords = get_city_coordinates(city)
    
    # 发送 API 请求到 OpenWeather
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": coords["lat"],
        "lon": coords["lon"],
        "appid": API_KEY,
        "units": "metric",
        "lang": "zh_cn"  # 使用中文
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # 处理返回数据
    forecast = []
    for item in data["list"][:days*8]:  # 每天8个数据点（每3小时一个）
        forecast.append({
            "datetime": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "feels_like": item["main"]["feels_like"],
            "humidity": item["main"]["humidity"],
            "weather": item["weather"][0]["description"],
            "wind_speed": item["wind"]["speed"]
        })
    
    return {
        "city": city,
        "forecast": forecast
    }

def get_air_quality(city: str) -> Dict[str, Any]:
    """获取指定城市的空气质量信息
    
    Args:
        city: 城市名称
    
    Returns:
        包含空气质量信息的字典
    """
    # 获取城市坐标
    coords = get_city_coordinates(city)
    
    # 发送 API 请求到 OpenWeather
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": coords["lat"],
        "lon": coords["lon"],
        "appid": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # 空气质量指数映射
    aqi_map = {
        1: "优",
        2: "良",
        3: "轻度污染",
        4: "中度污染",
        5: "重度污染"
    }
    
    return {
        "city": city,
        "aqi": aqi_map[data["list"][0]["main"]["aqi"]],
        "components": data["list"][0]["components"]
    }
