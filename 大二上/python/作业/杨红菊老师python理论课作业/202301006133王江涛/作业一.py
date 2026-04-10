class Rational:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        if self.b == 1:
            return str(self.a)
        g = self.gcd(abs(self.a), abs(self.b))
        if g > 1:
            return str(self.a // g) + '/' + str(self.b // g)
        else:
            return str(self.a) + '/' + str(self.b)

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def __add__(self, other):
        a = self.a * other.b + self.b * other.a
        b = self.b * other.b
        return Rational(a, b)

    def __sub__(self, other):
        a = self.a * other.b - self.b * other.a
        b = self.b * other.b
        return Rational(a, b)

    def __mul__(self, other):
        a = self.a * other.a
        b = self.b * other.b
        return Rational(a, b)

    def __eq__(self, other):
        return self.a * other.b == self.b * other.a
    def __ge__(self, other):
        return self.a * other.b >= self.b * other.a

# 测试
r1 = Rational(1, 2)
r2 = Rational(3, 4)
print(r1 + r2)
print(r1 - r2)
print(r1 * r2)
print(r1 == r2)
print(bool(r1 >= r2))