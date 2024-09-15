"""Given an integer n, find the sum of all odd numbers from 1 to n."""


def sum_of_odds(n):
    return sum(i for i in range(1, n + 1) if i % 2 != 0)
