from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

app = FastAPI()
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/fastapi_test?charset=utf8mb4"
async_engine = create_async_engine(
  ASYNC_DATABASE_URL,echo=True,
  pool_size=10,
  max_overflow=20,
)

# 定义模型类
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(50))

@app.get("/")
async def index():
    return {"name":"张三"}