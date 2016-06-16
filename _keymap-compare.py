#!/usr/bin/env python
"""
Used to compare two Sublime Text keymap files to find conflicts.

Use:
    python _keymap-compare.py <first.sublime-keymap> <second.sublime-keymap>

"""
import re
import json
import sys


def main():
    def get_keys(l):
        keymap = {}
        for i, x in enumerate(l):
            k = x.get('keys', [])
            for k in k:
                keymap[k] = x
        return keymap
    first_filename = sys.argv[1]
    second_filename = sys.argv[2]
    first_file = open(first_filename).read()
    second_file = open(second_filename).read()
    first_file = re.sub(r'(?<=\n)\s*//.*|/\*[\s\S]*?\*/', '', first_file)
    second_file = re.sub(r'(?<=\n)\s*//.*|/\*[\s\S]*?\*/', '', second_file)
    first_file = re.sub(r'([\]}]\s*),(\s*[\]}])', r'\1\2', first_file)
    second_file = re.sub(r'([\]}]\s*),(\s*[\]}])', r'\1\2', second_file)
    first_file = first_file.replace('//', '')
    second_file = second_file.replace('//', '')
    first = json.loads(first_file)
    second = json.loads(second_file)
    first_map = get_keys(first)
    second_map = get_keys(second)
    print("'%s' vs '%s'" % (first_filename, second_filename))
    n = 0
    for k, x in second_map.items():
        if k in first_map:
            print("Conflict in %s ('%s' vs '%s')" % (k, first_map[k].get('command'), x.get('command')))
            n += 1
    print("%s conflicts" % n)
if __name__ == '__main__':
    main()
