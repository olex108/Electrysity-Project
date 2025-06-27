list = [{"a":1, "b":2}, {"a":3, "b":2}]

for index, value in enumerate(list):
    if value["a"] == 1:
        del list[index]

print(list)