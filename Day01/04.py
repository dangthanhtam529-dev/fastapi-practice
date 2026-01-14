# 字典类型的变量
# 当你在定义函数时，需要接受一个字典作为参数，而字典中的键值对可以是任意类型时，
# 你可以使用字典类型的参数来实现。
# 例如，你可以定义一个函数，它接受一个字典作为参数，而字典中的键是字符串类型，值是任意类型。
def process_items(items: dict[str, any]):
    for key, value in items.items():
        print(key.title(), value)

if __name__ == '__main__':
    items = {"apple": 1, "banana": 2, "orange": 3}
    process_items(items)

