from abc import ABCMeta

# --
# ...
# --


class SingletonMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in SingletonMeta._instances:
            SingletonMeta._instances[cls] = super().__call__(*args, **kwargs)

        return SingletonMeta._instances[cls]
