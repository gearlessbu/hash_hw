import numpy as np
import io
import struct

def left_rotate(n, bits):
    return ((n << bits) | (n >> (32 - bits))) & 0xFFFFFFFF

def cut_32bits(n):
    return n & 0xFFFFFFFF

class SHA1:
    def __init__(self) -> None:
        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476
        self.E = 0xC3D2E1F0

    def process_chunk(self, chunk):
        Ws = []
        for i in range(80):
            if i < 16:
                w_tmp = struct.unpack(b'>I', chunk[i * 4:i * 4 + 4])[0]
                Ws.append(w_tmp)
            else:
                w_tmp = left_rotate(Ws[i - 3] ^ Ws[i - 8] ^ Ws[i - 14] ^ Ws[i - 16], 1)
                Ws.append(w_tmp)
        A_t, B_t, C_t, D_t, E_t = self.A, self.B, self.C, self.D, self.E
        for t in range(80):
            if 0 <= t <= 19:
                ft = (B_t & C_t) | (~B_t & D_t)
                Kt = 0x5A827999
            elif 20 <= t <= 39:
                ft = B_t ^ C_t ^ D_t
                Kt = 0x6ED9EBA1
            elif 40 <= t <= 59:
                ft = (B_t & C_t) | (B_t & D_t) | (C_t & D_t)
                Kt = 0x8F1BBCDC
            else:
                ft = B_t ^ C_t ^ D_t
                Kt = 0xCA62C1D6
            A_t, B_t, C_t, D_t, E_t = cut_32bits(left_rotate(A_t, 5) + ft + E_t + Ws[t] + Kt),\
                                      A_t, left_rotate(B_t, 30), C_t, D_t
        self.A = cut_32bits(A_t + self.A)
        self.B = cut_32bits(B_t + self.B)
        self.C = cut_32bits(C_t + self.C)
        self.D = cut_32bits(D_t + self.D)
        self.E = cut_32bits(E_t + self.E)

    def digest(self, message_str):
        message = message_str.encode('utf-8')
        message = bytes(message_str, encoding='utf-8')
        message_byte_length = len(message)
        print(message, message_byte_length)
        message += b'\x80'
        message += b'\x00' * ((56 - (message_byte_length + 1) % 64) % 64)
        message_bit_length = message_byte_length * 8
        message += struct.pack(b'>Q', message_bit_length)
        chunk_numbers = len(message) // 64
        print(len(message))
        for i in range(chunk_numbers):
            self.process_chunk(message[i * 64 : (i + 1) * 64])
        return '%08x%08x%08x%08x%08x' % (self.A, self.B, self.C, self.D, self.E)
        # return (self.A, self.B, self.C, self.D, self.E)


if __name__ == "__main__":
    sha = SHA1()
    print(sha.digest("abcdef"))