"""Your job is to write a function which increments a string, to create a new string.
If the string already ends with a number, the number should be incremented by 1.
If the string does not end with a number. the number 1 should be appended to the new string.
Examples:
foo -> foo1
foobar23 -> foobar24
foo0042 -> foo0043
foo9 -> foo10
foo099 -> foo100
Attention: If the number has leading zeros the amount of digits should be considered."""


def increment_string(strng):
    i = len(strng) - 1
    while i >= 0 and strng[i].isdigit():
        i -= 1
    non_number_part = strng[: i + 1]
    number_part = strng[i + 1:]
    if number_part:
        new_number = str(int(number_part) + 1)
        new_number = new_number.zfill(len(number_part))
        return non_number_part + new_number
    else:
        return strng + "1"
