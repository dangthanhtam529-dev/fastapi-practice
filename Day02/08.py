# 创建数据模型
from fastapi import FastAPI
from pydantic import BaseModel

# 数据模型 Item 定义了一个 JSON 模式，用于验证和文档化请求体
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item