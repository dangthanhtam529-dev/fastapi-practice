# =============================================================================
# FastAPI Cookie 参数 - 使用 Cookie 类示例
# =============================================================================
# 本文件演示了如何使用 FastAPI 的 Cookie 类获取 HTTP Cookie 参数
#
# 【HTTP Cookie】
# Cookie 是服务器存储在客户端的小型数据文件，
# 用于保持用户状态、跟踪用户行为等。
#
# 【Cookie 类】
# FastAPI 提供了 Cookie 类来获取请求中的 Cookie 参数。
# 它类似于 Query 和 Header，但专门用于 Cookie。
#
# 【使用 Pydantic 模型接收 Cookie】
# 也可以使用 Pydantic 模型来接收多个 Cookie 参数，
# 实现更复杂的数据结构验证。


# 导入必要的模块
from typing import Annotated  # 用于 Annotated 类型

from fastapi import Cookie, FastAPI  # FastAPI 框架和 Cookie 类
from pydantic import BaseModel       # Pydantic 基类

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义 Cookie 数据模型
class Cookies(BaseModel):
    """
    Cookie 数据模型

    用于接收多个 Cookie 参数，并进行类型验证

    Attributes:
        session_id: 会话 ID，必需
        fatebook_tracker: Fatebook 追踪器，可选
        googall_tracker: Google 追踪器，可选
    """
    session_id: str                    # 必需：会话 ID
    fatebook_tracker: str | None = None  # 可选：Fatebook 追踪器
    googall_tracker: str | None = None   # 可选：Google 追踪器


# 定义获取 Cookie 的路由
@app.get("/items/")
async def read_items(
    # 使用 Cookie 类获取 Cookie 参数
    # 当使用 Pydantic 模型时，FastAPI 会自动提取对应的 Cookie
    cookies: Annotated[
        Cookies,  # Cookie 数据模型
        Cookie()  # Cookie 参数验证器
    ]
):
    """
    获取客户端的 Cookie 信息

    演示如何使用 Pydantic 模型和 Cookie 类接收 Cookie 参数

    Args:
        cookies: Cookie 数据模型，包含所有 Cookie 参数

    Returns:
        Cookies: 返回接收到的 Cookie 信息

    Examples:
        请求：
        GET /items/
        Cookie:
        session_id=abc123; fatebook_tracker=xyz789

        响应：
        {
            "session_id": "abc123",
            "fatebook_tracker": "xyz789",
            "googall_tracker": null
        }
    """
    return cookies


# 【使用 curl 测试】
# curl -H "Cookie: session_id=abc123; fatebook_tracker=xyz789" \
#      "http://localhost:8000/items/"


# 【实际应用场景】
# 1. 会话管理：session_id 用于用户身份识别
# 2. 用户追踪：analytics trackers 用于分析用户行为
# 3. 个性化设置：保存用户偏好设置
# 4. 购物车：保存购物车信息


# 【Cookie 的特点】
# 1. 自动验证：Pydantic 模型会验证所有 Cookie 参数
# 2. 类型安全：获得完整的类型检查支持
# 3. 易于扩展：可以轻松添加新的 Cookie 字段
# 4. 清晰的文档：自动生成 API 文档


# 【测试方法】
# 1. 运行应用：uvicorn 03:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 使用浏览器开发者工具或 curl 测试 Cookie 传递
