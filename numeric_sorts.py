# Monkey patch Sublime Text 2 sort commands to sort numeric lines
from functools import cmp_to_key
import Default.sort as sort


def cmp(a, b):
    return (a > b) - (a < b)


def case_insensitive_sort(txt):
    txt.sort(key=cmp_to_key(lambda a, b: cmp(int(a), int(b)) if a.isdigit() and b.isdigit() else cmp(a.lower(), b.lower())))
    return txt


def case_sensitive_sort(txt):
    txt.sort(key=cmp_to_key(lambda a, b: cmp(int(a), int(b)) if a.isdigit() and b.isdigit() else cmp(a, b)))
    return txt


sort.case_insensitive_sort = case_insensitive_sort
sort.case_sensitive_sort = case_sensitive_sort
