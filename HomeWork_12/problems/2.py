"""An isogram is a word that has no repeating letters, consecutive or non-consecutive.
Implement a function that determines whether a string that contains only letters is an isogram.
Assume the empty string is an isogram. Ignore letter case."""


def is_isogram(s: str) -> bool:
    s = s.lower().replace(" ", "")
    unique_chars = set()
    for char in s:
        if char in unique_chars:
            return False
        unique_chars.add(char)
    return True
