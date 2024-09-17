def new_format(string):
    if len(string) <= 3:
        return string

    result = []
    i = len(string) % 3
    if i > 0:
        result.append(string[:i])
    for j in range(i, len(string), 3):
        result.append(string[j:j + 3])
    return ".".join(result)


assert new_format("1000000") == "1.000.000"
assert new_format("100") == "100"
assert new_format("1000") == "1.000"
assert new_format("100000") == "100.000"
assert new_format("10000") == "10.000"
assert new_format("0") == "0"
