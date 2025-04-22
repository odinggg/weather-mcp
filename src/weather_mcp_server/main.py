#!/usr/bin/env python3
import argparse
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from weather_mcp_server.weather import (
    set_api_key,
    get_weather_forecast as weather_get_forecast,
    get_air_quality as weather_get_air_quality
)

# 解析命令行参数
parser = argparse.ArgumentParser(description="天气 MCP 服务器")
parser.add_argument("--api-key", required=True, help="OpenWeather API 密钥")
args = parser.parse_args()

# 设置 API 密钥
set_api_key(args.api_key)

# 初始化 FastMCP 服务器
mcp = FastMCP("weather", description="提供天气预报和空气质量查询服务")

@mcp.tool(description="获取指定城市未来几天的天气预报")
def get_weather_forecast(city: str, days: int = 5) -> Dict[str, Any]:
    """获取指定城市未来几天的天气预报

    Args:
        city: 城市名称
        days: 预报天数（最多5天）

    Returns:
        包含天气预报信息的字典
    """
    forecast = weather_get_forecast(city, days)
    return forecast

@mcp.tool(description="获取指定城市的空气质量信息")
def get_air_quality(city: str) -> Dict[str, Any]:
    """获取指定城市的空气质量信息

    Args:
        city: 城市名称

    Returns:
        包含空气质量信息的字典
    """
    air_quality = weather_get_air_quality(city)
    return air_quality

def main():
    # 初始化并运行服务器
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
