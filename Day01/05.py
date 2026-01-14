# 有时候变量的类型也可能是类
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

def get_age(person: Person):
    return person.age

if __name__ == '__main__':
    p1 = Person('john', 20)
    print(get_age(p1))

