# 多个值
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

# 可以使用 Query 类来定义多个值
@app.get("/items/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
