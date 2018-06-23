# Monkey patch Sublime Text sort commands to sort numeric lines
from functools import cmp_to_key

from Default.sort import permute_lines, reverse_list, uniquealise_list, \
    permute_selection, unique_selection, SortLinesCommand, SortSelectionCommand


def common(a, b):
    i = 0
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y or x.isdigit():
            break
    return i


def cmp(a, b):
    return (a > b) - (a < b)


def case_sensitive_cmp(a, b):
    i = common(a, b)
    a = a[i:]
    b = b[i:]
    if a.isdigit() and b.isdigit():
        return cmp(int(a), int(b))
    return cmp(a, b)


def case_insensitive_cmp(a, b):
    return case_sensitive_cmp(a.lower(), b.lower())


def case_sensitive_sort(txt):
    txt.sort(key=cmp_to_key(case_sensitive_cmp))
    return txt


def case_insensitive_sort(txt):
    txt.sort(key=cmp_to_key(case_insensitive_cmp))
    return txt


def SortLinesCommand__run(self, edit, case_sensitive=False, reverse=False, remove_duplicates=False):
    view = self.view

    if case_sensitive:
        permute_lines(case_sensitive_sort, view, edit)
    else:
        permute_lines(case_insensitive_sort, view, edit)

    if reverse:
        permute_lines(reverse_list, view, edit)

    if remove_duplicates:
        permute_lines(uniquealise_list, view, edit)
SortLinesCommand.run = SortLinesCommand__run


def SortSelectionCommand__run(self, edit, case_sensitive=False, reverse=False, remove_duplicates=False):
    view = self.view

    permute_selection(
        case_sensitive_sort if case_sensitive else case_insensitive_sort,
        view, edit)

    if reverse:
        permute_selection(reverse_list, view, edit)

    if remove_duplicates:
        unique_selection(view, edit)
SortSelectionCommand.run = SortSelectionCommand__run
