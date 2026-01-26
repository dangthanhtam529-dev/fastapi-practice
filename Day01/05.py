# =============================================================================
# FastAPI 类型提示系统 - 自定义类类型提示示例
# =============================================================================
# 本文件演示了如何对自定义类使用类型提示
#
# 【自定义类的类型提示】
# 在 FastAPI 和 Python 类型提示系统中，我们不仅可以使用内置类型（str, int, list 等），
# 还可以对自定义的类使用类型提示。这使得代码更加清晰，并且编辑器可以提供更好的支持。
#
# 【为什么使用类类型提示？】
# 1. 类型安全：确保传递给函数的参数是正确的对象类型
# 2. 代码提示：编辑器知道对象的属性和方法
# 3. 自动文档：FastAPI 可以根据类定义自动生成 API 文档
# 4. 数据验证：结合 Pydantic，可以自动验证数据
#
# 【在 FastAPI 中的应用】
# 自定义类的类型提示通常与 Pydantic 的 BaseModel 结合使用：
#   from pydantic import BaseModel
#
#   class User(BaseModel):
#       name: str
#       age: int
#
#   @app.post("/users/")
#   async def create_user(user: User):
#       # FastAPI 会自动验证请求体是否符合 User 模型
#       return user


class Person:
    """
    人员类，表示一个人

    Attributes:
        name: 姓名，字符串类型
        age: 年龄，整数类型
    """

    def __init__(self, name: str, age: int):
        """
        初始化人员对象

        Args:
            name: 姓名，字符串类型
            age: 年龄，整数类型
        """
        self.name = name
        self.age = age


def get_age(person: Person) -> int:
    """
    获取人员的年龄

    Args:
        person: Person 对象

    Returns:
        人员的年龄，整数类型
    """
    # 由于类型提示指定了 person 应该是 Person 类型
    # 编辑器知道 person 有 age 属性，可以提供代码补全
    return person.age


# 测试代码
if __name__ == '__main__':
    # 创建 Person 对象
    p1 = Person('john', 20)

    # 调用函数获取年龄
    age = get_age(p1)
    print(age)  # 输出: 20

    # 验证类型
    print(type(p1))  # <class '__main__.Person'>
    print(isinstance(p1, Person))  # True
