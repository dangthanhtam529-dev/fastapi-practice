# 有时候路径顺序会影响到路由的匹配
from fastapi import FastAPI

app = FastAPI()

# 路径参数的顺序很重要
# 先定义 /users/me 路由，再定义 /users/{user_id} 路由
# 否则 /users/me 路由会匹配所有路径，包括 /users/{user_id}
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}