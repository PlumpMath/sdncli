from singledispatch import singledispatch


class SnareDrum(object):
    pass


class Cymbal(object):
    pass


class Stick(object):
    pass


class Brushes(object):
    pass


@singledispatch
def play(instrument, accessory):
    raise NotImplementedError("Cannot Play")


@play.register(SnareDrum)
def _(instrument, accessory):
    if isinstance(accessory, Stick):
        print "POC!"
    if isinstance(accessory, Brushes):
        print "SHHH"
    # else:
    #     raise NotImplementedError("cannotplay")


if __name__ == '__main__':
    play(SnareDrum(), Stick())
