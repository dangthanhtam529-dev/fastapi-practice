# =============================================================================
# FastAPI 请求头参数 - 列表类型请求头示例
# =============================================================================
# 本文件演示了如何获取包含多个值的请求头参数
#
# 【列表类型的请求头】
# 有些 HTTP 请求头可以包含多个值，使用逗号分隔。
# 例如：
#   X-Token: token1, token2, token3
#
# FastAPI 可以使用 list[类型] 接收这类请求头，
# 自动解析并返回一个列表。


# 导入必要的模块
from typing import Annotated  # 用于 Annotated 类型

from fastapi import FastAPI, Header  # FastAPI 框架和 Header 类

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义获取列表类型请求头的路由
@app.get("/items/")
async def read_items(
    # 获取 X-Token 请求头，支持多个值
    # 请求头格式：X-Token: token1, token2, token3
    # 解析结果：["token1", "token2", "token3"]
    x_token: Annotated[
        list[str] | None,  # 参数类型：字符串列表或 None
        Header(            # 请求头参数验证器
            # 可以添加验证规则，如：
            # min_length=1,  # 每个 token 至少 1 个字符
            # max_length=100  # 每个 token 最多 100 个字符
        )
    ] = None
):
    """
    获取 X-Token 请求头（支持多个值）

    演示如何获取包含多个值的请求头参数

    Args:
        x_token: X-Token 请求头列表，可选

    Returns:
        dict: 包含 X-Token 列表的字典

    Examples:
        请求：
        GET /items/
        请求头：
        X-Token: token1, token2, token3

        响应：
        {
            "X-Token values": ["token1", "token2", "token3"]
        }

        请求（无 X-Token）：
        GET /items/

        响应：
        {
            "X-Token values": null
        }
    """
    return {"X-Token values": x_token}


# 【使用 curl 测试】
# 单个值：
# curl -H "X-Token: single-token" "http://localhost:8000/items/"

# 多个值：
# curl -H "X-Token: token1, token2, token3" "http://localhost:8000/items/"


# 【实际应用场景】
# 1. 多重认证：多个 API Token
# 2. 链式追踪：X-Request-Id 链
# 3. 权限传递：多个权限标识
# 4. 缓存标识：多个缓存标签


# 【注意】
# 有些请求头标准格式是每个值单独一行：
#   X-Token: token1
#   X-Token: token2
#   X-Token: token3
#
# FastAPI 也能正确处理这种格式。


# 【测试方法】
# 1. 运行应用：uvicorn 02:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 尝试发送不同格式的 X-Token 请求头
