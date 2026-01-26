# =============================================================================
# FastAPI 请求体 - 列表类型请求体示例
# =============================================================================
# 本文件演示了如何使用列表类型的请求体
#
# 【列表类型请求体】
# 当请求体是一个对象列表时，可以使用 list[Model] 定义。
# FastAPI 会自动验证列表中的每个对象是否符合模型定义。
#
# 【使用场景】
# 1. 批量创建：一次创建多个商品、用户等
# 2. 批量更新：一次更新多个记录
# 3. 导入数据：从外部导入多个对象


# 导入 Pydantic
from pydantic import BaseModel, HttpUrl  # BaseModel 和 HttpUrl 类型

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义图片模型
class Image(BaseModel):
    """
    图片数据模型

    Attributes:
        url: 图片的 URL 地址，必须是有效的 HTTP/HTTPS URL
        name: 图片的名称或描述
    """
    url: HttpUrl  # 使用 HttpUrl 类型验证 URL 格式
    name: str     # 图片名称


# 定义批量创建图片的路由
@app.post("/images/multiple/")
async def create_multiple_images(
    images: list[Image]  # 请求体是 Image 对象列表
):
    """
    批量创建图片

    接收一个图片列表，一次性创建多张图片

    Args:
        images: 图片列表，请求体

    Returns:
        list: 创建的图片列表

    Examples:
        请求：
        POST /images/multiple/
        请求体：
        [
            {
                "url": "https://example.com/img1.jpg",
                "name": "Image 1"
            },
            {
                "url": "https://example.com/img2.jpg",
                "name": "Image 2"
            }
        ]

        响应：
        [
            {
                "url": "https://example.com/img1.jpg",
                "name": "Image 1"
            },
            {
                "url": "https://example.com/img2.jpg",
                "name": "Image 2"
            }
        ]
    """
    return images


# 【列表类型请求体的特点】
# 1. 验证每个元素：列表中的每个 Image 对象都会被验证
# 2. 保持顺序：列表的顺序会被保留
# 3. 类型安全：每个元素都必须是有效的 Image 对象


# 【使用 curl 测试】
# curl -X POST "http://localhost:8000/images/multiple/" \
#      -H "Content-Type: application/json" \
#      -d '[
#            {"url": "https://example.com/img1.jpg", "name": "Image 1"},
#            {"url": "https://example.com/img2.jpg", "name": "Image 2"}
#          ]'


# 【实际应用场景】
# 1. 批量导入：导入多个商品、用户、文章等
# 2. 批量更新：更新多个记录
# 3. 关联数据：创建主对象时同时创建多个关联对象


# 【结合数据库的示例】
# @app.post("/images/multiple/")
# async def create_multiple_images(images: list[Image]):
#     created_images = []
#     for image in images:
#         # 保存到数据库
#         saved = await db.save_image(image)
#         created_images.append(saved)
#     return created_images


# 【测试方法】
# 1. 运行应用：uvicorn 04:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 尝试发送图片列表进行测试
