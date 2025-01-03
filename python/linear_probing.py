import numpy as np
from sympy import isprime

def int_to_base_recursive(n:int, base:int):
    if n < 0:
        return [-b for b in int_to_base_recursive(-n, base)]
    if n < base:
        return [n]
    return int_to_base_recursive(n // base, base) + [n % base]

class LinearProbingHash:
    def __init__(self, p:int, r=None) -> None:
        assert(isprime(p))
        self.p = p
        self.r = r
        self.slots_load = np.ones((self.p,), dtype=int)

    def insert(self, key:int, val=None):
        if val is None:
            self.slots_load[self.hash_method(key)] += 1

    def hash_method(self, key:int):
        return np.sum(int_to_base_recursive(key, self.p)) % self.p