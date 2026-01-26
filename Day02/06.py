# =============================================================================
# FastAPI 路径参数与查询参数组合示例
# =============================================================================
# 本文件演示了如何在同一个路径操作中同时使用路径参数和查询参数
#
# 【路径参数 vs 查询参数】
# 路径参数：
#   - URL 路径的一部分，如 /items/{item_id}
#   - 用于标识主要资源
#   - 通常是必需的
#
# 查询参数：
#   - URL 中 ? 后面的参数，如 ?q=xxx&short=true
#   - 用于过滤、排序、扩展等
#   - 通常是可选的
#
# 【混合使用的优势】
# 1. 路径参数标识主要资源（如商品 ID）
# 2. 查询参数提供可选的过滤和定制选项
# 3. 这种组合使 API 更加灵活和易用


# 导入 FastAPI
from fastapi import FastAPI

# 创建 FastAPI 应用实例
app = FastAPI()


# 同时使用路径参数和查询参数的示例
# 路径参数：item_id - 标识要获取的项目
# 查询参数：q - 可选的搜索关键词
# 查询参数：short - 可选的简短模式开关
@app.get("/items/{item_id}")
async def read_item(
    item_id: str,              # 路径参数：项目 ID
    q: str | None = None,      # 查询参数：可选的搜索关键词
    short: bool = False        # 查询参数：是否返回简短版本，默认 False
):
    """
    根据 ID 获取项目信息

    这个示例展示了路径参数和查询参数如何协同工作：
    - 路径参数 item_id 标识要获取的具体项目
    - 查询参数 q 用于过滤或搜索
    - 查询参数 short 控制返回信息的详细程度

    Args:
        item_id: 项目的唯一标识符，字符串类型
        q: 可选的搜索关键词，用于进一步筛选
        short: 是否返回简短版本，默认为 False（返回详细信息）

    Returns:
        dict: 包含项目信息的字典

    Examples:
        # 基础用法
        GET /items/123
        返回：{"item_id": 123, "description": "This is an amazing item..."}

        # 带查询参数
        GET /items/123?q=keyword
        返回：{"item_id": 123, "q": "keyword", "description": "This is..."}

        # 简短模式
        GET /items/123?short=true
        返回：{"item_id": 123}

        # 组合使用
        GET /items/123?q=test&short=true
        返回：{"item_id": 123, "q": "test"}
    """
    # 创建基础的项目字典
    # 注意：item_id 是字符串类型，这里转换为整数
    # 实际项目中，item_id 本身就可以定义为 int 类型
    item = {"item_id": int(item_id)}

    # 如果提供了查询参数 q，将其添加到响应中
    if q:
        item.update({"q": q})

    # 如果 short 为 False（默认值），添加详细描述
    # 这种设计允许客户端选择获取详细信息或简短信息
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )

    return item


# 【设计模式说明】
# 1. 路径参数标识主要资源
# 2. 查询参数控制响应格式（short 参数控制是否返回详细信息）
# 3. 查询参数提供额外过滤（q 参数）
# 4. 合理使用默认值减少客户端复杂度


# 【测试方法】
# 1. 运行应用：uvicorn 06:app --reload
# 2. 访问 http://localhost:8000/items/42
#    返回包含完整信息的项目
# 3. 访问 http://localhost:8000/items/42?short=true
#    返回简短版本的项目信息
# 4. 访问 http://localhost:8000/items/42&q=search
#    返回包含搜索关键词的项目信息
