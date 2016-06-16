#!/usr/bin/env python
"""
Used to compare two Sublime Text keymap files to find conflicts.

Use:
    python _sublimegit_keygen.py [email]

"""
import sys
import json
import random


def validate_license(license):
    data, product_key = license
    i = 0
    s1, s2 = (0, 0)

    try:
        c = (int(product_key[-2:], 16) + 8 ^ 255) * 8
    except ValueError:
        return False

    while i <= 1848:
        s1 = (s1 + (ord(data[i]) & 255)) % 65535
        s2 = (s1 + s2) % 65535
        data += '%x' % (s2 << 16 | s1)
        i += 1
        # print i, c, data[-30:]
        if i == c and data[-30:] == product_key[:-2]:
            return True

    return False


def generate_license(email):
    i = 0
    s1, s2 = (0, 0)
    data = email

    choices = []
    while i <= 1848:
        s1 = (s1 + (ord(data[i]) & 255)) % 65535
        s2 = (s1 + s2) % 65535
        data += '%x' % (s2 << 16 | s1)
        i += 1
        cc = (((i / 8) ^ 255) - 8)
        c = (cc + 8 ^ 255) * 8
        if i == c:
            choices.append((data[-30:], cc))

    choice = random.choice(choices)
    product_key = '%s%02x' % (choice[0], choice[1])
    license = email, product_key
    if validate_license(license):
        return license


def register(email):
    license = generate_license(email)
    if not license:
        print("Cannot generate a valid lciense!")
        return
    email, product_key = license
    file = '\n'.join((
        "// This goes into Packages/User/SublimeGit.sublime-settings",
        json.dumps({
            'product_key': product_key,
            'email': email,
        }, indent=4)),
    )
    print(file)


if __name__ == '__main__':
    try:
        email = sys.argv[1]
    except IndexError:
        email = 'some@email.com'
        register(email)
