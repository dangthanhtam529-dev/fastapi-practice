# =============================================================================
# FastAPI 请求体 - 使用 Body(embed=True) 嵌入模型示例
# =============================================================================
# 本文件演示了如何使用 Body(embed=True) 将 Pydantic 模型嵌入到请求体中
#
# 【Body(embed=True) 的作用】
# 默认情况下，当路由函数只有一个 Pydantic 模型参数时，
# FastAPI 会直接使用模型字段作为请求体的根级。
# 使用 Body(embed=True) 可以将整个模型作为一个嵌套对象。
#
# 【使用场景】
# 1. API 版本控制：为未来可能添加的字段预留空间
# 2. 明确的数据结构：使请求体结构更加清晰
# 3. 与其他数据组合：将模型与其他简单类型组合


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


# 定义更新路由，使用 embed=True 嵌入模型
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,  # 路径参数
    item: Annotated[
        Item,      # Pydantic 模型
        Body(
            embed=True  # 嵌入到请求体的 "item" 字段中
        )
    ]
):
    """
    更新商品信息（使用嵌入的请求体）

    这个示例展示了如何使用 Body(embed=True) 将 Pydantic 模型
    嵌入到请求体的一个字段中，而不是直接展开。

    Args:
        item_id: 要更新的商品 ID，路径参数
        item: 商品信息，嵌入到请求体的 "item" 字段中

    Returns:
        dict: 包含商品 ID 和商品信息的字典

    Examples:
        # 不使用 embed=True 时的请求体：
        {
            "name": "Widget",
            "price": 19.99
        }

        # 使用 embed=True 时的请求体：
        {
            "item": {
                "name": "Widget",
                "price": 19.99
            }
        }
    """
    # 构建响应
    results = {
        "item_id": item_id,
        "item": item
    }

    return results


# 【embed=True vs 默认行为】
# 默认行为（不使用 embed）：
#   请求体：{"name": "Widget", "price": 19.99, "tax": 1.5}
#   模型：Item(name="Widget", price=19.99, tax=1.5)

# 使用 embed=True：
#   请求体：{"item": {"name": "Widget", "price": 19.99, "tax": 1.5}}
#   模型：Item(name="Widget", price=19.99, tax=1.5)


# 【使用 curl 测试】
# 不使用 embed：
# curl -X PUT "http://localhost:8000/items/123" \
#      -H "Content-Type: application/json" \
#      -d '{"name": "Widget", "price": 19.99}'

# 使用 embed：
# curl -X PUT "http://localhost:8000/items/123" \
#      -H "Content-Type: application/json" \
#      -d '{"item": {"name": "Widget", "price": 19.99}}'


# 【实际应用场景】
# 1. RESTful API：保持一致的请求体结构
# 2. 复杂对象：包含多个相关字段的对象
# 3. 未来扩展：预留添加其他字段的空间


# 【与多模型组合使用】
# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int,
#     item: Annotated[Item, Body(embed=True)],
#     user: Annotated[User, Body(embed=True)]
# ):
#     # 请求体格式：
#     # {
#     #     "item": {...},
#     #     "user": {...}
#     # }


# 【测试方法】
# 1. 运行应用：uvicorn 05:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 查看请求体结构和参数说明
