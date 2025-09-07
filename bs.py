class A:
    def foo(self):
        print("A", self, self.x)


class B(A):
    def __init__(self, x):
        self.x = x

    def foo(self):
        print("B")


b = B(3)
super(B, b).foo()
