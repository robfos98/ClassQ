from decimal import DivisionByZero
import math

def GCD(a, b):
    def iterator(a, b):
        if a < b: (a, b) = (b, a)
        if not b: return a
        return iterator(a % b, b)
    a = abs(a)
    b = abs(b)
    if not a and not b: raise ZeroDivisionError
    return iterator(a, b)

class Q:
    def __init__(self, n = 0, d = 1):
        if isinstance(n, (float, Q)) or isinstance(d, (float, Q)):
            ans = Q.sink(n)/Q.sink(d)
            self.n = ans.n
            self.d = ans.d
        else:
            if not isinstance(n, int) and isinstance(d, int): raise ArithmeticError
            if not d: raise ZeroDivisionError
            if d < 0:
                n *= -1
                d *= -1
            divis = GCD(n, d)
            self.n = n // divis
            self.d = d // divis

    def __repr__(self):
        return str(self.n) + '/' + str(self.d)
    def __str__(self):
        if self.d > 1: return str(self.n) + '/' + str(self.d)
        else: return str(self.n)
    def __float__(self):
        return self.n / self.d
    def __bool__(self):
        return bool(self.n)

    def __add__(self, q):
        if isinstance(q, int): q = Q(q)
        if isinstance(q, float): q = Q.sink(q)
        return Q(self.n * q.d + q.n * self.d, self.d * q.d)
    def __radd__(self, q):
        return self + q
    def __mul__(self, q):
        if isinstance(q, int): q = Q(q)
        if isinstance(q, float): q = Q.sink(q)
        return Q(self.n * q.n, self.d * q.d)
    def __rmul__(self, q):
        return self * q
    def __pow__(self, q):
        if isinstance(q, float): q = Q.sink(q)
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
        if isinstance(q, float): q = Q.sink(q)
        return self * q ** -1
    def __rtruediv__(self, q):
        return self ** -1 * q

    def __eq__(self, q):
        if isinstance(q, int): q = Q(q)
        if isinstance(q, float): q = Q.sink(q)
        return self.n == q.n and self.d == q.d
    def __ne__(self, q):
        return not self == q
    def __lt__(self, q):
        if isinstance(q, int): q = Q(q)
        if isinstance(q, float): q = Q.sink(q)
        self -= q
        return self.n < 0
    def __gt__(self, q):
        if isinstance(q, int): q = Q(q)
        if isinstance(q, float): q = Q.sink(q)
        self -= q
        return self.n > 0
    def __le__(self, q):
        return not self > q
    def __ge__(self, q):
        return not self < q

    def __divmod__(self, q):
        if isinstance(q, int): q = Q(q)
        if isinstance(q, float): q = Q.sink(q)
        if q == 0: raise ZeroDivisionError
        elif q < 0:
            self = -self
            q = -q
        ans = Q()
        about = int(float(self/q))
        self -= about * q
        ans += about
        while self < 0:
            self += q
            ans -= 1
        while self >= q:
            self -= q
            ans += 1
        return ans, self
    def __rdivmod__(self, q):
        return divmod(Q(q), self)
    def __floordiv__(self, q):
        return divmod(self, q)[0]
    def __rfloordiv__(self, q):
        return divmod(Q(q), self)[0]
    def __mod__(self, q):
        return divmod(self, q)[1]
    def __rmod__(self, q):
        return divmod(Q(q), self)[1]

    def __floor__(self):
        return self // 1
    def __ceil__(self):
        return -math.floor(-self)
    def __int__(self):
        return math.floor(self).n if self >= 0 else math.ceil(self).n

    def SCF(list):
        for num in list: num = int(num)
        ans = Q()
        while list:
            if ans: ans **= -1
            ans += list[-1]
            list = list[:-1]
        return ans

    def sink(q, acc = 1000000):
        if isinstance(q, (int, Q)): return q
        elif not isinstance(q, float): raise ArithmeticError
        elif q < 0: return -Q.sink(-q)
        elif q == 0: return Q()
        else:
            if q * acc < 100:
                acc = math.ceil(100/q)
            ans = []
            while Q.SCF(ans).d < acc:
                (count, q) = divmod(q, 1)
                ans += [Q(int(count))]
                if q <= 1/acc: break
                q **= -1
            return Q.SCF(ans)