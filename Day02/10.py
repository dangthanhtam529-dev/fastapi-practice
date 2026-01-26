# =============================================================================
# FastAPI 查询参数 - 列表类型查询参数示例
# =============================================================================
# 本文件演示了如何使用 Query 类处理多个值的查询参数（列表类型）
#
# 【列表类型查询参数】
# 当查询参数可以有多个值时，可以使用列表类型：
#   ?q=apple&q=banana&q=orange
#
# 在 FastAPI 中，这会被解析为：
#   q = ["apple", "banana", "orange"]
#
# 【使用场景】
# 1. 多选过滤：?category=electronics&category=books
# 2. 标签筛选：?tags=python&tags=fastapi
# 3. 包含多个值的搜索：?keywords=fastapi&keywords=tutorial


# 导入必要的模块
from typing import Annotated  # 用于 Annotated 类型

from fastapi import FastAPI, Query  # FastAPI 和 Query 类

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义接受列表类型查询参数的路由
# q: Annotated[list[str] | None, Query()] = None
#   - list[str]: 查询参数 q 是一个字符串列表
#   - | None: 或者 None（不提供时）
#   - Query(): 使用 Query 验证器
#   - = None: 默认值为 None
#
# URL 格式：/items/?q=apple&q=banana&q=orange
# 解析结果：q = ["apple", "banana", "orange"]
@app.get("/items/")
async def read_items(
    q: Annotated[
        list[str] | None,  # 参数类型：字符串列表或 None
        Query()            # 查询参数验证器（可以添加验证规则）
    ] = None
):
    """
    获取商品列表，支持多值查询参数

    Args:
        q: 查询关键词列表，可选参数。
           URL 格式：?q=apple&q=banana
           解析结果：["apple", "banana"]

    Returns:
        dict: 包含商品列表和查询参数（如果有）的字典

    Examples:
        # 不使用查询参数
        GET /items/
        返回：{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}

        # 使用单个查询值
        GET /items/?q=apple
        返回：{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}], "q": ["apple"]}

        # 使用多个查询值
        GET /items/?q=apple&q=banana&q=orange
        返回：{"items": [...], "q": ["apple", "banana", "orange"]}

        # 不提供值（空列表）
        GET /items/?q=
        返回：{"items": [...], "q": []}
    """
    # 基础响应
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}

    # 如果提供了查询参数，添加到响应中
    if q:
        results.update({"q": q})

    return results


# 【使用 curl 测试】
# curl "http://localhost:8000/items/?q=apple&q=banana&q=orange"

# 【前端发送多值查询参数的方式】
# 1. JavaScript (fetch):
#    const params = new URLSearchParams();
#    params.append('q', 'apple');
#    params.append('q', 'banana');
#    fetch(`/items/?${params}`);

# 2. Axios:
#    axios.get('/items/', { params: { q: ['apple', 'banana'] } });

# 3. 表单提交:
#    <input type="checkbox" name="q" value="apple">
#    <input type="checkbox" name="q" value="banana">


# 【Query 类的其他配置】
# 可以为列表参数添加验证规则：
#   q: Annotated[
#       list[str] | None,
#       Query(
#           min_length=1,          # 列表至少有一个元素
#           max_length=10,         # 列表最多有 10 个元素
#           title="搜索关键词",
#           description="可以提供多个搜索关键词"
#       )
#   ] = None


# 【测试方法】
# 1. 运行应用：uvicorn 10:app --reload
# 2. 访问 http://localhost:8000/docs
# 3. 尝试使用多个查询值进行测试
