# MCP Atlassian

Model Context Protocol (MCP) server for Confluence & Jira Server/Data Center deployments.

### Compatibility

| Product        | Deployment Type    | Support Status              |
|----------------|--------------------|-----------------------------|
| **Confluence** | Server/Data Center | ✅ Supported (version 6.0+)  |
| **Jira**       | Server/Data Center | ✅ Supported (version 8.14+) |

# 在 MCP Factory 调试

在 MCP Factory 调试 MCP Server 非常简单，找到 main.py 即可一键实现单步调试, 以避免频繁的部署, 提升开发效率。

## 调试方法

首选要创建本地 Python 虚拟环境, 在 requirements.txt 添加依赖, 并且执行以下命令安装依赖

```bash
# 创建本地 Python 虚拟环境, 如果通过 IDE GUI 工具创建过则跳过
uv venv

# 安装依赖
uv pip install -r requirements.txt
```

然后启动 main.py 的 __name__ 函数入口即可.



