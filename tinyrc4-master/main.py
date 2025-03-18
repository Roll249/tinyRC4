#!/usr/bin/env python3


class RC4:
    def __init__(self, key):
        bytekey = str.encode(key)
        self.t_table = [i for i in range(0, 256)]
        t = 0

        for i in range(0, len(self.t_table)):
            t = t + self.t_table[i] + bytekey[i % len(bytekey)]
            t %= 256
            self.t_table[t], self.t_table[i] = self.t_table[i], self.t_table[t]

    def gen_keystream(self, txt):
        self.keystream = []

        p1 = 0
        p2 = 0
        while True:
            p1 += 1
            p1 %= 256

            p2 = p2 + self.t_table[p1]
            p2 %= 256

            self.t_table[p1], self.t_table[p2] = self.t_table[p2], self.t_table[p1]

            t_idx = (self.t_table[p1] + self.t_table[p2]) % 256
            self.keystream.append(self.t_table[t_idx])
            if len(self.keystream) >= len(txt):
                break
            
    def crypt(self, txt):
        bytetxt = str.encode(txt)
        self.outbuf = []
        for i in range(0, len(bytetxt)):
            self.outbuf.append(self.keystream[i] ^ bytetxt[i])        
