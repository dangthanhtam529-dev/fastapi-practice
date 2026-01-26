# =============================================================================
# FastAPI 数据模型 - HttpUrl 类型和列表嵌套模型示例
# =============================================================================
# 本文件演示了如何使用 HttpUrl 类型验证 URL，以及如何使用列表嵌套模型
#
# 【HttpUrl 类型】
# HttpUrl 是 Pydantic 提供的特殊类型，用于验证 URL 格式。
# 特点：
# 1. 自动验证 URL 格式
# 2. 自动解析 URL 各部分（scheme, host, path 等）
# 3. 转换为字符串时保持原始格式
#
# 【列表嵌套模型】
# 使用 list[ModelName] 可以定义模型列表。
# FastAPI 会自动验证列表中的每个元素是否符合模型定义。


# 导入 Pydantic
from pydantic import BaseModel, HttpUrl  # BaseModel 和 HttpUrl 类型

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义嵌套模型：图片（使用 HttpUrl）
class Image(BaseModel):
    """
    图片数据模型

    使用 HttpUrl 类型验证 URL 格式。
    HttpUrl 会自动验证 URL 是否符合标准格式，
    并解析 URL 的各个组成部分。

    Attributes:
        url: 图片的 URL 地址，必须是有效的 HTTP/HTTPS URL
        name: 图片的名称或描述
    """
    # 使用 HttpUrl 类型，自动验证 URL 格式
    # 合法的 URL：http://example.com, https://example.com/path
    # 不合法的 URL：not-a-url, ftp://example.com（ftp 不被允许）
    url: HttpUrl  # 必需字段：图片 URL（自动验证格式）
    name: str     # 必需字段：图片名称


# 定义主模型：商品（包含图片列表）
class Item(BaseModel):
    """
    商品数据模型

    展示如何使用 HttpUrl 和列表嵌套模型：
    - HttpUrl：用于验证图片 URL
    - list[Image]：用于存储多张图片

    Attributes:
        name: 商品名称
        description: 商品描述（可选）
        price: 商品价格
        tax: 税费（可选）
        tags: 商品标签集合
        images: 商品图片列表（可选）
    """
    # 基本类型字段
    name: str           # 必需字段：商品名称
    description: str | None = None  # 可选字段：商品描述

    # 数值类型字段
    price: float        # 必需字段：商品价格
    tax: float | None = None  # 可选字段：商品税费

    # 集合类型字段
    tags: set[str] = set()  # 可选字段：商品标签集合

    # 列表嵌套模型：商品图片列表
    images: list[Image] | None = None  # 可选字段：图片列表


# 定义更新路由
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,  # 路径参数
    item: Item     # 请求体：Item 模型
):
    """
    更新商品信息（支持多张图片）

    展示 HttpUrl 验证和列表嵌套模型的实际应用

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

        包含多张图片的商品：
        {
            "name": "Widget",
            "price": 19.99,
            "tags": ["sale", "new"],
            "images": [
                {
                    "url": "https://example.com/img1.jpg",
                    "name": "Front View"
                },
                {
                    "url": "https://example.com/img2.jpg",
                    "name": "Back View"
                }
            ]
        }

        无效 URL（会被拒绝）：
        {
            "url": "not-a-valid-url"
        }
        返回：422 错误
    """
    results = {"item_id": item_id, "item": item}
    return results


# 【HttpUrl 验证示例】
# 有效的 URL：
#   "https://example.com"
#   "https://example.com/path/to/page"
#   "http://localhost:8000"
#   "https://example.com:8000/path"

# 无效的 URL：
#   "not-a-url"
#   "ftp://example.com"（ftp 不被允许）
#   "example.com"（缺少协议）
#   "https://"（不完整）


# 【列表嵌套模型的特点】
# 1. 验证每个元素：列表中的每个元素都会验证
# 2. 递归验证：嵌套的 HttpUrl 也会验证
# 3. 有序列表：保持元素的顺序


# 【使用 curl 测试】
# curl -X PUT "http://localhost:8000/items/123" \
#      -H "Content-Type: application/json" \
#      -d '{
#            "name": "Widget",
#            "price": 19.99,
#            "images": [
#              {"url": "https://example.com/img1.jpg", "name": "Front"},
#              {"url": "https://example.com/img2.jpg", "name": "Back"}
#            ]
#          }'


# 【实际应用场景】
# 1. 电商商品：多张商品图片
# 2. 文章系统：多张配图
# 3. 用户资料：多个社交媒体链接
# 4. 产品展示：多角度图片


# 【测试方法】
# 1. 运行应用：uvicorn 03:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 尝试使用不同格式的 URL 进行测试
