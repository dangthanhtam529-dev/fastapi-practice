# =============================================================================
# FastAPI 路径参数 - 路径参数顺序的重要性
# =============================================================================
# 本文件演示了定义路径参数时的顺序问题
#
# 【为什么路径参数顺序很重要？】
# FastAPI 按定义顺序匹配路由。如果将动态路由放在静态路由之前，
# 动态路由会"抢占"所有匹配的 URL，包括原本应该匹配静态路由的 URL。
#
# 【错误示例（顺序颠倒）】
# 如果先定义 /users/{user_id}，再定义 /users/me：
#   @app.get("/users/{user_id}")
#   async def read_user(user_id: str):
#       return {"user_id": user_id}
#
#   @app.get("/users/me")
#   async def read_user_me():
#       return {"user_id": "the current user"}
#
# 访问 /users/me 时：
#   - FastAPI 会将 "me" 解析为 user_id 的值
#   - 调用 read_user("me")，返回 {"user_id": "me"}
#   - 而不会调用 read_user_me()
#
# 【正确示例（静态路由在前）】
# 应该先定义具体的静态路由，再定义动态路由：
#   @app.get("/users/me")        # 先定义静态路由
#   async def read_user_me():
#       return {"user_id": "the current user"}
#
#   @app.get("/users/{user_id}") # 后定义动态路由
#   async def read_user(user_id: str):
#       return {"user_id": user_id}
#
# 访问 /users/me 时：
#   - FastAPI 先尝试匹配 /users/me
#   - 匹配成功，调用 read_user_me()
#
# 访问 /users/123 时：
#   - /users/me 不匹配
#   - FastAPI 尝试匹配 /users/{user_id}
#   - 匹配成功，调用 read_user("123")


# 导入 FastAPI
from fastapi import FastAPI

# 创建 FastAPI 应用实例
app = FastAPI()


# 【重要】静态路由必须定义在动态路由之前
# /users/me 是一个具体的、静态的路由
# 它匹配 URL: /users/me
@app.get("/users/me")
async def read_user_me():
    """
    获取当前登录用户的信息

    Returns:
        dict: 包含当前用户标识的字典

    Note:
        这个路由必须在 /users/{user_id} 之前定义，
        否则 "me" 会被解析为 user_id 参数。
    """
    return {"user_id": "the current user"}


# 动态路由，匹配 /users/ 后面的任意值
# 例如：/users/123、/users/abc、/users/me 等
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    """
    根据用户 ID 获取用户信息

    Args:
        user_id: 用户 ID，字符串类型

    Returns:
        dict: 包含用户 ID 的字典

    Examples:
        - /users/123 -> {"user_id": "123"}
        - /users/abc -> {"user_id": "abc"}
    """
    return {"user_id": user_id}


# 【总结】
# 1. 静态路由（具体路径）应该定义在动态路由之前
# 2. 动态路由（包含参数的路径）应该定义在静态路由之后
# 3. 这条规则适用于所有需要同时存在静态和动态路由的场景


# 【实际应用建议】
# 在设计 API 时，应该考虑路由的逻辑层次和具体程度：
# - 更具体的路由放在前面（/users/me）
# - 更通用的路由放在后面（/users/{user_id}）
# - 这样可以确保具体路由不会被通用路由"抢占"
