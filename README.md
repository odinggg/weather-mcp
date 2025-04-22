# 天气 MCP 服务器

这是一个使用 OpenWeather API 获取天气数据和空气质量的 Model Context Protocol (MCP) 服务器。

## 功能

- 获取任何城市的详细天气预报（最多 5 天）
- 获取任何城市的当前空气质量信息

## 安装

### 前提条件

- Python 3.11+
- OpenWeather API 密钥（可在 [OpenWeather](https://openweathermap.org/api) 获取）
- Anthropic Claude Desktop 应用（或其他 MCP 客户端）
- UV 包管理工具（https://github.com/astral-sh/uv）

### 步骤

1. **克隆仓库**

```bash
git clone https://github.com/yourusername/weather-mcp-server.git
cd weather-mcp-server
```

2. **使用 uv 安装依赖**

```bash
uv pip install -e .
```

3. **连接到 MCP 服务器**

将以下 JSON 配置添加到您的 MCP 客户端（例如 Claude Desktop）中：

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/weather-mcp-server",
        "run",
        "main.py",
        "--api-key",
        "your_openweather_api_key_here"
      ]
    }
  }
}
```

对于 **Claude Desktop**，将此保存为 `claude_desktop_config.json`，位置在：

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

## 使用方法

连接后，您可以使用天气 MCP 服务器：

1. **获取天气预报**：
   - 向 Claude 询问任何城市的天气预报
   - 指定预报的天数（最多 5 天）

2. **获取空气质量信息**：
   - 向 Claude 询问任何城市的空气质量

示例提示：
- "未来 3 天北京的天气预报是什么？"
- "现在上海的空气质量如何？"

## 故障排除

- 如果遇到关于 API 密钥的错误，确保您在命令行参数中正确提供了 API 密钥
- 确保您的网络可以访问 OpenWeather API
- 检查您的 MCP 客户端中的服务器配置是否正确

## 技术细节

该服务器使用：
- OpenWeather API 获取天气数据
- FastMCP 框架实现 MCP 协议
- Python 的 requests 库进行 API 交互
