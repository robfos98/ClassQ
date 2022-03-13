from decimal import DivisionByZero

def GCDstep(a, b):
    if not b: return a, a, 0
    count = 0
    while a > b:
        a -= b
        count += 1
    return a, b, count

def GCD(a, b):
    def iterator(a, b):
        if a < b: (a, b) = (b, a)
        elif a == b:
            if a: return a
            else: raise ZeroDivisionError
        a, b, *_ = GCDstep(a, b)
        return iterator(a, b)
    a = abs(a)
    b = abs(b)
    return iterator(a, b)

class Q:
    def __init__(self, n = 0, d = 1):
        if not isinstance(n, int) and isinstance(d, int):
            raise ArithmeticError
        if not d:
            raise ZeroDivisionError
        if d < 0:
            n *= -1
            d *= -1
        divis = GCD(n, d)
        self.n = n // divis
        self.d = d // divis
    def __str__(self):
        if self.d > 1: return str(self.n) + '/' + str(self.d)
        else: return str(self.n)

    def __bool__(self):
        return bool(self.n)

    def __add__(self, q):
        if isinstance(q, int): q = Q(q)
        return Q(self.n * q.d + q.n * self.d, self.d * q.d)
    def __radd__(self, q):
        return self + q
    def __mul__(self, q):
        if isinstance(q, int): q = Q(q)
        return Q(self.n * q.n, self.d * q.d)
    def __rmul__(self, q):
        return self * q
    def __pow__(self, q):
        if isinstance(q, Q):
            if q.d > 1: raise NotImplementedError
            else: q = q.n
        if q < 0: return Q(self.d, self.n) ** -q
        elif not q and not self.n: raise ZeroDivisionError
        else:
            ans = Q(1)
            while q:
                ans *= self
                q -= 1
            return ans
    def __rpow__(self, q):
        return Q(q) ** self

    def __pos__(self):
        return self
    def __neg__(self):
        return self * -1
    def __abs__(self):
        return Q(abs(self.n), self.d)

    def __sub__(self, q):
        return self + -q
    def __rsub__(self, q):
        return -self + q
    def __truediv__(self, q):
        if isinstance(q, int): q = Q(q)
        return self * q ** -1
    def __rtruediv__(self, q):
        return self ** -1 * q

    def __eq__(self, q):
        if isinstance(q, int): q = Q(q)
        return self.n == q.n and self.d == q.d
    def __ne__(self, q):
        return not self == q
    def __lt__(self, q):
        if isinstance(q, int): q = Q(q)
        self -= q
        return self.n < 0
    def __gt__(self, q):
        if isinstance(q, int): q = Q(q)
        self -= q
        return self.n > 0
    def __le__(self, q):
        return not self > q
    def __ge__(self, q):
        return not self < q

    def floorer(self, q):
        if isinstance(q, int): q = Q(q)
        if q == 0: raise ZeroDivisionError
        elif q < 0:
            self = -self
            q = -q
        ans = Q()
        while self < 0:
            self += q
            ans -= 1
        while self >= q:
            self -= q
            ans += 1
        return ans, self

    def __floordiv__(self, q):
        return Q.floorer(self, q)[0]
    def __rfloordiv__(self, q):
        return Q(q) // self
    def __mod__(self, q):
        return Q.floorer(self,q)[1]
    def __rmod__(self, q):
        return Q(q) % self

x = Q(2,3)
y = Q(1,6)
print(x // y)
print(1 // y)
print(x // 1)
print(-1 // Q(7))
print(1 % x)
print(y % 1)