# First 32 bits of the fractional parts of the square roots of the first 8
# primes i.e. 2 ... 19
HASH_VALUES = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]
# First 32 bits of the fractional parts of the cube roots of the first 64
# prime numbers i.e. 2 ... 311
ROUND_CONSTANTS = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
    0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
    0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
    0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
    0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]
# All Add operations are done with modulo 2^32
BIT_LIMIT = 2 ** 32


def hash(input_string: str):
    # Pre-processing
    byte_string = input_string.encode('utf-8')
    bit_length = len(byte_string) * 8
    byte_string += b'\x80'
    while len(byte_string) % 64 != 56:
        byte_string += b'\x00'
    byte_string += bit_length.to_bytes(8, 'big')

    h0, h1, h2, h3, h4, h5, h6, h7 = HASH_VALUES
    # Hashing
    for i in range(0, len(byte_string), 64):
        w = [concatenate_binary_ints(byte_string[j:j+4]) for j in range(i, len(byte_string), 4)]
        w += (64 - len(w)) * [0x0000]
        for i in range(16, 64):
            s0 = rr(w[i-15], 7) ^ rr(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = rr(w[i-2], 17) ^ rr(w[i-2], 19) ^ (w[i-2] >> 10)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) % BIT_LIMIT
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
        for i in range(64):
            s1 = rr(e, 6) ^ rr(e, 11) ^ rr(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + s1 + ch + ROUND_CONSTANTS[i] + w[i]) % BIT_LIMIT
            s0 = rr(a, 2) ^ rr(a, 13) ^ rr(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (s0 + maj) % BIT_LIMIT

            h = g
            g = f
            f = e
            e = (d + temp1) % BIT_LIMIT
            d = c
            c = b
            b = a
            a = (temp1 + temp2) % BIT_LIMIT

        h0 = (h0 + a) % BIT_LIMIT
        h1 = (h1 + b) % BIT_LIMIT
        h2 = (h2 + c) % BIT_LIMIT
        h3 = (h3 + d) % BIT_LIMIT
        h4 = (h4 + e) % BIT_LIMIT
        h5 = (h5 + f) % BIT_LIMIT
        h6 = (h6 + g) % BIT_LIMIT
        h7 = (h7 + h) % BIT_LIMIT
    return '%08x%08x%08x%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4, h5, h6, h7)


def concatenate_binary_ints(args):
    result = 0
    for num in args:
        num = num & 0xFF
        result = (result << 8) | num
    return result


def rr(value: int, shift: int):
    return ((value >> shift) | (value << (32 - shift))) & 0xFFFFFFFF
