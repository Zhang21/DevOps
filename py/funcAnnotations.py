def f(name: str, age: int = 18) -> str:
    print("Annotations: ", f.__annotations__)
    print("Arguments: ", name, age)
    return name + 'and' + str(age)

f('Zhang21')
