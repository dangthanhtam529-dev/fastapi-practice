# 多个路径和查询参数
from fastapi import FastAPI

app = FastAPI()

# 你不需要用特定的顺序来定义路径参数和查询参数
# 例如 /users/{user_id}/items/{item_id} 中的 user_id 和 item_id 都是路径参数
# 查询参数 q 是可选的，默认值为 None
# 查询参数 short 是可选的，默认值为 False
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item