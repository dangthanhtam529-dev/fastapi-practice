# =============================================================================
# FastAPI 多请求体模型示例
# =============================================================================
# 本文件演示了如何在同一个路由中使用多个 Pydantic 模型作为请求体
#
# 【多请求体使用场景】
# 1. 复杂更新操作：同时更新 item 和 user 信息
# 2. 关联数据创建：创建 item 时同时创建关联的 user
# 3. 批量操作：处理多个相关对象
#
# 【FastAPI 处理多请求体的方式】
# 当路由函数有多个 Pydantic 模型参数时：
#   async def update_item(item_id: int, item: Item, user: User):
#
# FastAPI 会将它们合并为一个请求体：
#   {
#       "item": {...},
#       "user": {...}
#   }
#
# 路径参数 item_id 仍然从 URL 路径中获取


# 导入 Pydantic
from pydantic import BaseModel

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义商品模型
class Item(BaseModel):
    """
    商品数据模型

    Attributes:
        name: 商品名称，必填
        description: 商品描述，可选
        price: 商品价格，必填
        tax: 税费，可选
    """
    name: str                      # 必需字段：商品名称
    description: str | None = None # 可选字段：商品描述
    price: float                   # 必需字段：商品价格
    tax: float | None = None       # 可选字段：商品税费


# 定义用户模型
class User(BaseModel):
    """
    用户数据模型

    Attributes:
        username: 用户名，必填
        full_name: 全名，可选
    """
    username: str                   # 必需字段：用户名
    full_name: str | None = None    # 可选字段：用户全名


# 定义更新路由，使用多个请求体模型
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,  # 路径参数：从 URL 路径中获取
    item: Item,    # 请求体参数：商品信息
    user: User     # 请求体参数：用户信息
):
    """
    更新商品信息（需要用户权限）

    这个示例展示了如何在同一个请求中同时处理：
    - 路径参数：item_id（要更新的商品 ID）
    - 请求体参数 item：商品的新信息
    - 请求体参数 user：执行操作的用户信息

    Args:
        item_id: 要更新的商品 ID，路径参数
        item: 商品信息，请求体
        user: 用户信息，请求体

    Returns:
        dict: 包含商品 ID、商品信息和用户信息的字典

    Examples:
        请求：
        PUT /items/123
        请求体：
        {
            "item": {
                "name": "New Item",
                "description": "Updated description",
                "price": 29.99,
                "tax": 2.99
            },
            "user": {
                "username": "john_doe",
                "full_name": "John Doe"
            }
        }

        响应：
        {
            "item_id": 123,
            "item": {
                "name": "New Item",
                "description": "Updated description",
                "price": 29.99,
                "tax": 2.99
            },
            "user": {
                "username": "john_doe",
                "full_name": "John Doe"
            }
        }
    """
    # 构建响应
    results = {
        "item_id": item_id,  # 路径参数
        "item": item,        # 第一个请求体模型
        "user": user         # 第二个请求体模型
    }

    return results


# 【请求体结构说明】
# 当使用多个 Pydantic 模型时，FastAPI 期望的请求体格式：
#   {
#       "item": { ... },  # Item 模型的数据
#       "user": { ... }   # User 模型的数据
#   }

# 而不是：
#   { ... }  # 单个对象


# 【使用 curl 测试】
# curl -X PUT "http://localhost:8000/items/123" \
#      -H "Content-Type: application/json" \
#      -d '{"item": {"name": "Widget", "price": 19.99}, "user": {"username": "john"}}'


# 【实际应用场景】
# 1. 权限验证：更新操作需要验证操作用户
# 2. 审计日志：记录谁执行了什么操作
# 3. 多表更新：同时更新关联的数据表


# 【测试方法】
# 1. 运行应用：uvicorn 03:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 查看自动生成的 API 文档和请求体示例
