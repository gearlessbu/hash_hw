import numpy as np
import io
import struct

def left_rotate(n, bits):
    return ((n << bits) | (n >> (32 - bits))) & 0xFFFFFFFF

def cut_32bits(n):
    return n & 0xFFFFFFFF

class SHA3:
    def __init__(self, r, c) -> None:
        self.r = r
        self.c = c
        self.b = r + c
        self.w = self.b // 25
        assert(self.b - 25 * self.w == 0)
        self.A = np.zeros((5, 5, self.w))
        S = np.zeros((self.b,))
        for i in range(5):
            for j in range(5):
                for k in range(self.w):
                    self.A[i, j, k] = S[self.w * (5 * j + i) + k]


if __name__ == "__main__":
    sha = SHA3()
    # print(sha.digest("abcdef"))