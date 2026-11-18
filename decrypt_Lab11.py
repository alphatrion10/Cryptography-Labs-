
import string
import base64

def reverse_step3(text):
    alphabet = string.ascii_lowercase
    shifted = alphabet[4:] + alphabet[:4]
    table = str.maketrans(shifted, alphabet)
    return text.translate(table)

def reverse_step1(text):
    original = "zyxwvutsrqponZYXWVUTSRQPONmlkjihgfedcbaMLKJIHGFEDCBA"
    substituted = "mlkjihgfedcbaMLKJIHGFEDCBAzyxwvutsrqponZYXWVUTSRQPON"
    table = str.maketrans(substituted, original)
    return text.translate(table)

def reverse_step2(text):
    return base64.b64decode(text, validate=True).decode('ascii')

with open("intercepted.txt", "r") as f:
    ciphertext = f.read().strip()

result = ciphertext
layer = 0

while result:
    identifier = result[0]
    payload = result[1:]

    if identifier == '1':
        result = reverse_step1(payload)

    elif identifier == '2':
        result = reverse_step2(payload)

    elif identifier == '3':
        result = reverse_step3(payload)

    else:
        print("Unexpected identifier:", identifier)
        break

    layer += 1
    print(f"Layer {layer}: reversed step {identifier}")
    print("Preview:", repr(result[:60]))

    if result and result[0] not in '123':
        print("\nPossible decoded message:")
        print(result)
        break

print("\nTotal layers reversed:", layer)
