class Shape(object):
    def __init__(self, a, b):
        if a < b:
            a, b = b, a
        self.a = a
        self.b = b
        self.square = a * b
