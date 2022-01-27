# Simple Singleton design pattern.
#
# 2021 Andre Scheir Johansson
# email: scheir5@hotmail.se
# -----------------------------------------------------------


class Singleton:
    def __init__(self, usrCls):
        self.usrCls = usrCls
    def get_instance(self):
        try:
            return self.instance
        except:
            self.instance = self.usrCls()
            return self.instance
    def __call__(self):
        raise TypeError('Get instance from get_instance')

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, self.usrCls)