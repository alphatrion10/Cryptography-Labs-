#!/usr/bin/env python3
import math
import sys


FREQ = {
    ' ': 18.0, 'e': 10.2, 't': 7.5, 'a': 6.5, 'o': 6.2, 'i': 5.7, 'n': 5.7,
    's': 5.3, 'h': 5.0, 'r': 4.9, 'd': 3.5, 'l': 3.3, 'u': 2.3, 'c': 2.2,
    'm': 2.0, 'w': 1.9, 'f': 1.8, 'g': 1.7, 'y': 1.6, 'p': 1.5, 'b': 1.2,
    'v': 0.8, 'k': 0.6, 'x': 0.15, 'j': 0.15, 'q': 0.1, 'z': 0.07,
    ',': 1.0, '.': 0.9, '-': 0.2, "'": 0.3,
}


def char_score(ch):
    """Log-likelihood style score of one plaintext character."""
    if ch in FREQ:
        return math.log(FREQ[ch])
    if ch.isupper() and ch.lower() in FREQ:
        return math.log(FREQ[ch.lower()] * 0.25)
    if 32 <= ord(ch) < 127:     
        return -8.0
    return -30.0                 

def load(path):
    cts = {}
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        num, hexstr = line.split(":", 1)
        hexstr = "".join(hexstr.split())          
        if len(hexstr) % 2:                        
            print(f"warning: message {num} has odd hex length, dropping last digit")
            hexstr = hexstr[:-1]
        cts[int(num)] = bytes.fromhex(hexstr)
    return cts


def recover_key(cts, min_cover=3):
    longest = max(len(c) for c in cts.values())
    key = [None] * longest
    for i in range(longest):
        column = [c[i] for c in cts.values() if i < len(c)]   
        if len(column) < min_cover:                            
            continue

        key[i] = max(range(256),
                     key=lambda k: sum(char_score(chr(b ^ k)) for b in column))
    return key



def decrypt(ct, key):
    out = []
    for i, b in enumerate(ct):
        if key[i] is None:
            out.append("_")
        else:
            ch = chr(b ^ key[i])
            out.append(ch if 32 <= ord(ch) < 127 else "?")
    return "".join(out)


def apply_guess(cts, key, msg, pos, guess):
    ct = cts[msg]
    for offset, ch in enumerate(guess):
        key[pos + offset] = ct[pos + offset] ^ ord(ch)


GUESSES = [
    # (message number, start position, guessed text)
    (13, 0, "The Web as I envisaged it"),  
    (13, 99, "Tim Berners-Lee"),            
]


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "ciphertexts.txt"
    cts = load(path)
    key = recover_key(cts)

    for msg, pos, text in GUESSES:
        apply_guess(cts, key, msg, pos, text)

    for n in sorted(cts):
        print(f"M{n:<2} ({len(cts[n])} bytes): {decrypt(cts[n], key)}\n")


if __name__ == "__main__":
    main()
