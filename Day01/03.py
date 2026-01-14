# 泛型类型的参数
# 当你在定义函数时，需要接受不同类型的参数，而不是固定的一种类型时，
# 你可以使用泛型类型的参数来实现。
# 例如，你可以定义一个函数，它接受一个列表作为参数，而列表中的元素可以是任意类型。
def process_items(items: list[str]):
    for item in items:
        print(item.title())

if __name__ == '__main__':
    items = ["apple", "banana", "orange"]
    process_items(items)
    