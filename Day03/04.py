# =============================================================================
# FastAPI 请求体 - 使用 Body() 嵌入简单类型示例
# =============================================================================
# 本文件演示了如何使用 FastAPI 的 Body 类将简单类型嵌入到请求体中
#
# 【Body 类的作用】
# Body 类用于将简单类型（如 int、str、bool）作为请求体的一部分。
# 默认情况下，路径操作函数中的非路径参数、非查询参数、非 Pydantic 模型参数
# 会被当作查询参数。使用 Body() 可以将其改为请求体参数。
#
# 【使用场景】
# 1. 简单值作为请求体：除了复杂模型外，还需要一些简单值
# 2. 嵌套在模型中：importance 的值会出现在请求体的根级
# 3. 与模型混合使用：同时使用 Pydantic 模型和简单类型


# 导入必要的模块
from typing import Annotated  # 用于 Annotated 类型

from fastapi import Body, FastAPI  # FastAPI 框架和 Body 类
from pydantic import BaseModel     # Pydantic 基类

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


# 定义更新路由，使用 Body() 嵌入简单类型
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,                                     # 路径参数
    item: Item,                                       # 请求体模型
    user: User,                                       # 请求体模型
    importance: Annotated[int, Body()]                # 嵌入到请求体的简单类型
):
    """
    更新商品信息（带重要性级别）

    这个示例展示了如何将简单类型（int）通过 Body() 嵌入到请求体中。
    importance 参数不是一个独立的参数，而是请求体的一部分。

    Args:
        item_id: 要更新的商品 ID，路径参数
        item: 商品信息，请求体模型
        user: 用户信息，请求体模型
        importance: 重要性级别，简单类型，通过 Body() 嵌入请求体

    Returns:
        dict: 包含所有参数的字典

    Examples:
        请求：
        PUT /items/123
        请求体：
        {
            "item": {
                "name": "Widget",
                "price": 19.99
            },
            "user": {
                "username": "john_doe"
            },
            "importance": 5
        }

        响应：
        {
            "item_id": 123,
            "item": {...},
            "user": {...},
            "importance": 5
        }
    """
    # 构建响应
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }

    return results


# 【请求体结构说明】
# 使用 Body() 后，请求体格式：
#   {
#       "item": { ... },      # Item 模型
#       "user": { ... },      # User 模型
#       "importance": 5       # 简单类型
#   }

# 如果不使用 Body()，importance 会被当作查询参数


# 【Body 类的其他用法】
# 1. 指定别名：Body(alias="imp")
# 2. 隐藏字段：Body(exclude=True)
# 3. 设置默认值：Body(default=0)


# 【使用 curl 测试】
# curl -X PUT "http://localhost:8000/items/123" \
#      -H "Content-Type: application/json" \
#      -d '{"item": {"name": "Widget", "price": 19.99}, "user": {"username": "john"}, "importance": 5}'


# 【实际应用场景】
# 1. 优先级设置：设置任务的优先级
# 2. 数量限制：指定操作的数量
# 3. 状态标记：添加状态标记


# 【测试方法】
# 1. 运行应用：uvicorn 04:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 查看请求体结构和参数说明
