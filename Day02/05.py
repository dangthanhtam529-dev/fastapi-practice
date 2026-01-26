# =============================================================================
# FastAPI 查询参数 - 基础查询参数示例
# =============================================================================
# 本文件演示了 FastAPI 中查询参数（Query Parameters）的基本用法
#
# 【什么是查询参数？】
# 查询参数是 URL 中 ? 后面的键值对，用于向服务器传递可选参数。
# 格式：/路径?key1=value1&key2=value2
#
# 例如：/items/?skip=0&limit=10
#   - 路径：/items/
#   - 查询参数：skip=0, limit=10
#
# 【查询参数 vs 路径参数】
# 路径参数：URL 路径的一部分，如 /items/{item_id}
# 查询参数：URL 中 ? 后面的参数，如 /items/?skip=0
#
# 【定义查询参数】
# 在路径操作函数中，将参数声明为函数参数即可：
#   @app.get("/items/")
#   async def read_items(skip: int = 0, limit: int = 10):
#
# FastAPI 会自动识别：
#   - skip 和 limit 是查询参数（不在路径中定义）
#   - 它们的默认值分别是 0 和 10
#
# 【查询参数的特点】
# 1. 可选性：可以设置默认值，使参数变为可选
# 2. 类型提示：可以指定类型，FastAPI 会自动验证
# 3. 顺序无关：查询参数的顺序不影响匹配
# 4. 数量灵活：可以定义任意数量的查询参数
#
# 【注意】
# Python 不允许在同一个作用域内定义两个同名的函数。
# 本示例中两个 read_item 函数会冲突，实际使用时应避免。

# 导入 FastAPI
from fastapi import FastAPI

# 创建 FastAPI 应用实例
app = FastAPI()


# 模拟数据库数据
# 在实际应用中，这通常是数据库查询的结果
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]


# 【示例 1】带默认值的查询参数
# skip 和 limit 都有默认值，所以都是可选参数
# 访问 /items/ 等价于 /items/?skip=0&limit=10
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    """
    获取项目列表（支持分页）

    Args:
        skip: 跳过的项目数量，默认值 0
        limit: 返回的最大项目数量，默认值 10

    Returns:
        list: 项目的子列表

    Examples:
        - /items/ -> [{"item_name":"Foo"},{"item_name":"Bar"},{"item_name":"Baz"}]
        - /items/?skip=0&limit=2 -> [{"item_name":"Foo"},{"item_name":"Bar"}]
        - /items/?skip=1&limit=2 -> [{"item_name":"Bar"},{"item_name":"Baz"}]
    """
    # 使用切片从列表中获取指定范围的项目
    # skip : skip + limit 等价于 range(skip, skip + limit)
    return fake_items_db[skip : skip + limit]


# 【示例 2】可选的查询参数
# q 参数使用联合类型 str | None，默认值为 None
# 如果用户没有提供 q 参数，函数仍然可以正常工作
# 注意：这个函数会覆盖上面的 read_items 函数，实际使用时应避免
@app.get("/items/")
async def read_item(q: str | None = None):
    """
    根据查询参数 q 返回结果

    Args:
        q: 可选的查询字符串

    Returns:
        dict: 包含查询结果的字典

    Examples:
        - /items/ -> {"q": "Not found"}
        - /items/?q=hello -> {"q": "hello"}
    """
    if q:
        return {"q": q}
    return {"q": "Not found"}


# 【正确的做法】将两个功能合并到一个函数中
# 下面是一个更实用的示例，演示如何组合多个查询参数：

@app.get("/items/correct/")
async def read_items_correct(
    skip: int = 0,
    limit: int = 10,
    q: str | None = None
):
    """
    获取项目列表（支持分页和搜索）

    Args:
        skip: 跳过的项目数量，默认值 0
        limit: 返回的最大项目数量，默认值 10
        q: 可选的搜索关键词

    Returns:
        list 或 dict: 如果有搜索关键词，返回搜索结果；否则返回项目列表
    """
    items = fake_items_db[skip : skip + limit]

    if q:
        # 过滤包含搜索关键词的项目（不区分大小写）
        items = [
            item for item in items
            if q.lower() in item["item_name"].lower()
        ]
        return {"q": q, "items": items}

    return {"items": items}


# 【测试方法】
# 1. 运行应用：uvicorn 05:app --reload
# 2. 访问 http://localhost:8000/items/
#    返回：所有项目
# 3. 访问 http://localhost:8000/items/?skip=1&limit=2
#    返回：跳过第一个，返回两个项目
# 4. 访问 http://localhost:8000/items/correct/?q=Foo
#    返回：包含 "Foo" 的项目


# 【查询参数的实际应用场景】
# 1. 分页：skip, limit, page, page_size
# 2. 排序：sort_by, order（asc/desc）
# 3. 过滤：q（搜索关键词）, category, status
# 4. 字段选择：fields（只返回指定字段）
# 5. 格式化：format（json/xml）
