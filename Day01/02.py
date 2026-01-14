# 当你在形参中使用了类型提示，那么后续你如果在编写代码时出现了错误的类型，
# 那么编辑器就会提示你，你需要传递正确类型的参数
#
# def get_name_with_age(name: str, age: int):
#     name_with_age = name + " is this old: " + age
#     return name_with_age

# 有时候你可能忽略了将整数转换为字符串，导致类型错误，那么通过这种方式，在代码自动补全时就会直接完成类型转换
def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + str(age)
    return name_with_age

# 你也可以定义一个变量可能的几种类型
def get_name_with_age(name: str, age: int | float):
    name_with_age = name + " is this old: " + str(age)
    return name_with_age

# 也可能会出现空值的情况
def get_name_with_age(name: str, age: int | float | None = None):
    if age is None:
        name_with_age = name + " has no age"
    else:
        name_with_age = name + " is this old: " + str(age)
    return name_with_age
