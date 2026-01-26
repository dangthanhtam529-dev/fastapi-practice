# =============================================================================
# FastAPI 多路径参数与查询参数组合示例
# =============================================================================
# 本文件演示了如何在同一个路径操作中同时使用多个路径参数和查询参数
#
# 【多路径参数】
# FastAPI 支持在同一个路径中定义多个路径参数：
#   /users/{user_id}/items/{item_id}
#   - user_id：用户 ID
#   - item_id：项目 ID
#
# 【参数顺序】
# 路径参数的顺序不影响函数参数的顺序：
#   @app.get("/users/{user_id}/items/{item_id}")
#   async def read_user_item(item_id: str, user_id: int, q: str | None = None):
#
# FastAPI 会根据参数名称自动匹配，而不是根据定义顺序。
#
# 【路径参数 vs 查询参数】
# 路径参数（必须）：
#   - user_id: int - 必需的用户 ID
#   - item_id: str - 必需的项目 ID
#
# 查询参数（可选）：
#   - q: str | None = None - 可选的搜索关键词
#   - short: bool = False - 是否返回简短版本


# 导入 FastAPI
from fastapi import FastAPI

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义包含多个路径参数的路由
# /users/{user_id}/items/{item_id} 匹配如 /users/123/items/456 的 URL
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int,              # 路径参数：用户 ID（必需）
    item_id: str,              # 路径参数：项目 ID（必需）
    q: str | None = None,      # 查询参数：可选的搜索关键词
    short: bool = False        # 查询参数：是否返回简短版本
):
    """
    获取指定用户的指定项目信息

    这个示例展示了多层资源嵌套的 API 设计：
    - /users/{user_id} - 访问特定用户
    - /users/{user_id}/items - 访问该用户的项目列表
    - /users/{user_id}/items/{item_id} - 访问该用户的特定项目

    Args:
        user_id: 用户的唯一标识符，整数类型
        item_id: 项目的唯一标识符，字符串类型
        q: 可选的搜索关键词，用于进一步筛选
        short: 是否返回简短版本，默认为 False

    Returns:
        dict: 包含项目和用户信息的字典

    Examples:
        # 获取用户123的项目456的完整信息
        GET /users/123/items/456
        返回：{"item_id": "456", "owner_id": 123, "description": "..."}

        # 获取简短版本
        GET /users/123/items/456?short=true
        返回：{"item_id": "456", "owner_id": 123}

        # 带搜索关键词
        GET /users/123/items/456?q=keyword
        返回：{"item_id": "456", "owner_id": 123, "q": "keyword", "description": "..."}
    """
    # 构建项目信息字典
    item = {
        "item_id": item_id,       # 项目 ID
        "owner_id": user_id       # 所有者 ID（用户 ID）
    }

    # 如果提供了查询参数 q，添加到响应中
    if q:
        item.update({"q": q})

    # 如果不是简短模式，添加详细描述
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )

    return item


# 【RESTful API 设计模式】
# 这种多层嵌套的 URL 结构反映了资源的层级关系：
# - /users/ - 用户集合
# - /users/{user_id} - 特定用户
# - /users/{user_id}/items - 该用户的项目集合
# - /users/{user_id}/items/{item_id} - 特定项目

# 【参数顺序的说明】
# 函数参数的顺序可以任意，因为 FastAPI 通过参数名称匹配：
#   async def read_user_item(
#       item_id: str,              # 可以放在前面
#       user_id: int,              # 可以放在后面
#       q: str | None = None,      # 查询参数
#       short: bool = False        # 查询参数
#   ):
#
# FastAPI 会自动识别：
#   - user_id 和 item_id 是路径参数（路径中有 {user_id} 和 {item_id}）
#   - q 和 short 是查询参数（没有在路径中定义）


# 【测试方法】
# 1. 运行应用：uvicorn 07:app --reload
# 2. 访问 http://localhost:8000/users/1/items/abc
#    返回完整信息
# 3. 访问 http://localhost:8000/users/1/items/abc?short=true
#    返回简短信息
# 4. 访问 http://localhost:8000/users/1/items/abc?q=test
#    返回带搜索关键词的信息
