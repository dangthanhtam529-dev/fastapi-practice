# 查询参数
# 当你的参数不是路径参数时，你可以使用查询参数来传递参数
# 查询参数是指在URL中使用 ?key=value 来传递参数的方式
# 例如 /items/?q=somequery 中的 q 就是一个查询参数
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# 查询参数 skip 和 limit 都是可选的，默认值分别为 0 和 10
# 例如 /items/ 等价于 /items/?skip=0&limit=10
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# 查询参数 q 是可选的，默认值为 None
# 例如 /items/?q=somequery 中的 q 就是一个查询参数
@app.get("/items/")
async def read_item(q: str | None = None):
    if q:
        return {"q": q}
    return {"q": "Not found"}
