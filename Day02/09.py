from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

# 可以使用Annotated添加更多的条件
@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results