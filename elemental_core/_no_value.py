class NoValue(object):
    def __bool__(self) -> bool:
        # Python 3.x
        return False

    def __nonzero__(self) -> bool:
        # Python 2.x
        return False


NO_VALUE = NoValue()