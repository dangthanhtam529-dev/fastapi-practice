# =============================================================================
# FastAPI 数据模型 - 嵌套模型和复杂类型示例
# =============================================================================
# 本文件演示了如何在 Pydantic 模型中使用嵌套模型和复杂类型
#
# 【嵌套模型】
# Pydantic 模型可以包含其他 Pydantic 模型作为字段类型。
# 这使得我们可以构建复杂的数据结构。
#
# 【复杂类型】
# - set[str]: 字符串集合（自动去重，无序）
# - list[str]: 字符串列表（有序，可重复）
# - dict[str, any]: 字典类型
# - Image | None: 可选的嵌套模型


# 导入 Pydantic
from pydantic import BaseModel

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义嵌套模型：图片
class Image(BaseModel):
    """
    图片数据模型

    Attributes:
        url: 图片的 URL 地址
        name: 图片的名称或描述
    """
    url: str   # 必需字段：图片 URL
    name: str  # 必需字段：图片名称


# 定义主模型：商品（包含嵌套模型和复杂类型）
class Item(BaseModel):
    """
    商品数据模型

    展示如何使用嵌套模型和复杂类型：
    - 基本类型：name, price
    - 可选类型：description, tax, image
    - 集合类型：tags（使用 set 去重）
    - 嵌套模型：image（Image 类型的字段）

    Attributes:
        name: 商品名称
        description: 商品描述（可选）
        price: 商品价格
        tax: 税费（可选）
        tags: 商品标签集合（自动去重）
        image: 商品图片（可选的 Image 嵌套模型）
    """
    # 基本类型字段
    name: str           # 必需字段：商品名称
    description: str | None = None  # 可选字段：商品描述

    # 数值类型字段
    price: float        # 必需字段：商品价格
    tax: float | None = None  # 可选字段：商品税费

    # 集合类型字段：使用 set 自动去重
    tags: set[str] = set()  # 可选字段：商品标签集合，默认空集合

    # 嵌套模型字段：商品图片
    image: Image | None = None  # 可选字段：商品图片


# 定义更新路由
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,  # 路径参数
    item: Item     # 请求体：Item 模型
):
    """
    更新商品信息

    展示嵌套模型和复杂类型的实际应用

    Args:
        item_id: 商品 ID，路径参数
        item: 商品信息，请求体

    Returns:
        dict: 包含商品 ID 和商品信息的字典

    Examples:
        简单商品：
        {
            "name": "Widget",
            "price": 19.99
        }

        完整商品（包含标签和图片）：
        {
            "name": "Widget",
            "description": "A wonderful widget",
            "price": 19.99,
            "tax": 1.50,
            "tags": ["sale", "popular", "new"],
            "image": {
                "url": "https://example.com/widget.jpg",
                "name": "Widget Photo"
            }
        }
    """
    results = {"item_id": item_id, "item": item}
    return results


# 【嵌套模型的特点】
# 1. 递归验证：嵌套模型也会自动验证
# 2. 递归序列化：嵌套模型会正确序列化为 JSON
# 3. IDE 支持：嵌套模型也提供完整的代码补全


# 【集合类型的选择】
# set[str] vs list[str]：
# - set：自动去重，无序，不支持索引访问
# - list：保持顺序，支持重复，支持索引访问
#
# 选择建议：
# - 标签、分类等使用 set（需要去重）
# - 有顺序要求的列表使用 list（如排行榜、顺序列表）


# 【使用 curl 测试】
# curl -X PUT "http://localhost:8000/items/123" \
#      -H "Content-Type: application/json" \
#      -d '{
#            "name": "Widget",
#            "price": 19.99,
#            "tags": ["sale", "popular"],
#            "image": {
#                "url": "https://example.com/img.jpg",
#                "name": "Widget Image"
#            }
#          }'


# 【实际应用场景】
# 1. 电商商品：商品信息包含图片、分类、标签
# 2. 用户资料：用户信息包含头像、兴趣标签
# 3. 文章系统：文章包含作者信息、分类标签、配图
# 4. 订单系统：订单包含商品列表、地址信息


# 【测试方法】
# 1. 运行应用：uvicorn 02:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 查看自动生成的 API 文档和嵌套结构
