# 类型转换
from fastapi import FastAPI

app = FastAPI()

# 路径参数 item_id 是一个字符串，但是在函数中被转换为一个整数
# 查询参数 q 是可选的，默认值为 None
# 查询参数 short 是可选的，默认值为 False
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": int(item_id)}  # 路径参数 item_id 是一个字符串，但是在函数中被转换为一个整数
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item