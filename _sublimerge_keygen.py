def register():
    from sublimerge.sublimerge_commands import SublimergeDifferencer

    o = SublimergeDifferencer()

    # Get a Unique ID:
    import random
    u = '-'.join(''.join('%X' % random.randint(0, 15) for i in range(4)) for i in range(5))

    # Sign and join key:
    # types = ['y', 'm', 'f'] (sublimerge_commands.SublimergeDifferencer().types)
    k = '-'.join((u, o.mk(u, 'f')))

    # Register:
    o.rr(k)
