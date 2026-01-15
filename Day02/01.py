from fastapi import FastAPI

app = FastAPI()

# 带类型的路径参数
@app.get("/item/{item_id}")
def read_root(item_id: int):
    return {"item_id": item_id}
