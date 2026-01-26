# =============================================================================
# FastAPI 请求头参数 - 使用 Header 类示例
# =============================================================================
# 本文件演示了如何使用 FastAPI 的 Header 类获取 HTTP 请求头参数
#
# 【HTTP 请求头】
# HTTP 请求头是客户端发送给服务器的元数据，
# 例如：User-Agent, Authorization, Content-Type 等。
#
# 【Header 类】
# FastAPI 提供了 Header 类来获取请求头参数。
# 它类似于 Query 和 Path，但专门用于请求头。
#
# 【特点】
# 1. 自动提取请求头参数
# 2. 支持类型验证
# 3. 支持默认值
# 4. 支持别名（默认将参数名中的下划线转换为连字符）


# 导入必要的模块
from typing import Annotated  # 用于 Annotated 类型

from fastapi import FastAPI, Header  # FastAPI 框架和 Header 类

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义获取请求头的路由
@app.get("/items/")
async def read_items(
    # 使用 Header 类获取请求头参数
    # user_agent: Annotated[str | None, Header()] = None
    #
    # 注意：默认情况下，FastAPI 会将参数名中的下划线转换为连字符
    # 例如：user_agent 会对应请求头中的 "user-agent"
    #
    # 如果需要保持原样，可以使用 alias 参数：
    # user_agent: Annotated[str | None, Header(alias="User-Agent")] = None
    user_agent: Annotated[
        str | None,  # 参数类型：字符串或 None
        Header(      # 请求头参数验证器
            # alias="User-Agent",  # 可选：指定请求头名称
            # deprecated=True,     # 可选：标记为废弃
            # include_in_schema=False  # 可选：不显示在文档中
        )
    ] = None
):
    """
    获取客户端的 User-Agent 请求头

    演示如何使用 Header 类获取 HTTP 请求头参数

    Args:
        user_agent: User-Agent 请求头参数，可选

    Returns:
        dict: 包含 User-Agent 的字典

    Examples:
        请求：
        GET /items/
        请求头：
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36

        响应：
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
        }
    """
    return {"User-Agent": user_agent}


# 【常用的 HTTP 请求头】
# 1. User-Agent: 客户端信息
# 2. Authorization: 认证信息
# 3. Content-Type: 内容类型
# 4. Accept: 可接受的响应类型
# 5. Cookie: Cookie 信息
# 6. X-Request-ID: 请求 ID（用于追踪）


# 【使用 curl 测试】
# curl -H "User-Agent: My Custom Agent" "http://localhost:8000/items/"


# 【实际应用场景】
# 1. 客户端识别：根据 User-Agent 识别客户端类型
# 2. 认证授权：获取 Authorization 请求头进行身份验证
# 3. 请求追踪：使用 X-Request-ID 追踪请求
# 4. 限流控制：使用 API-Key 进行限流


# 【测试方法】
# 1. 运行应用：uvicorn 01:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 查看 API 文档中的请求头参数
