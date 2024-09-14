"""Write an algorithm that takes an array and moves all of the zeros to the end,
preserving the order of the other elements."""


def move_zeros(lst):
    non_zero = [i for i in lst if i != 0]
    zero_count = lst.count(0)
    return non_zero + [0] * zero_count
