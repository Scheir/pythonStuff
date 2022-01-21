from singleton import Singleton

@Singleton
class myClass:
    def __init__(self) -> None:
        self.a = 2
    def incr(self):
        self.a += 1
    def __str__(self):
       return f'The singleton has value: {self.a}'


def fun():
    a = myClass.get_instance()
    a.incr()
    print(id(a))

b = myClass.get_instance()
b.incr()
print(b)
