import numpy as np

from linear_probing import LinearProbingHash


class TabulationHash:
    def __init__(self, hash_tables:list) -> None:
        self.hash_tables = hash_tables
        self.c = len(hash_tables)

    def hash_method(self, key:np.array):
        assert(np.size(key) == self.c)
        hash_val = self.hash_tables[0].hash_method(key[0])
        for i in range(1, self.c):
            hash_val = hash_val ^ self.hash_tables[i].hash_method(key[i])
        return hash_val