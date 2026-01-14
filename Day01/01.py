# 可选的类型提示
# 这种传统式写法你必须调用那个将首字母转换为大写的“那个方法”，不然可能无法触发补全功能
# def get_full_name(first_name, last_name):
#     full_name = first_name.title() + " " + last_name.title()
#     return full_name
#
#
# print(get_full_name("john", "doe"))
#
# print("*" * 20)

# 这里想表达的是，原本你可能忘记了要调用title()方法来处理字符串的大小写，
# 而在形参中添加类型提示，会提示调用者在调用函数时，应该传递字符串类型的参数
def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name

print(get_full_name("john", "doe"))