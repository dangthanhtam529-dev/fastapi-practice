# 依赖注入
from fastapi import FastAPI,Depends

app = FastAPI()

async def get_name():
    return "张三"

@app.get("/")
async def index(name:str=Depends(get_name)):
    return {"name":name}

