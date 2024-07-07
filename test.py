import hashlib
import sha256

test_strings = [
    "hello world",
    "mmmmmmmmmmmmmmmm",
    "",
    "a",
    "abc",
    "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
]

for s in test_strings:
    print(f"Input: {s}")
    print(f"Our SHA-256:     {sha256.hash(s)}")
    print(f"hashlib SHA-256: {hashlib.sha256(s.encode()).hexdigest()}")
    print()
