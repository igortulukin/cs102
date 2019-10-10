def encrypt_caesar(plaintext: str) -> str:
    cipher_text = ''
    for i in plaintext:
        if not (65 <= ord(i) <= 90 or 97 <= ord(i) <= 122):
            cipher_text += i
        else:
            encrypt = ord(i)
            if 87 < encrypt < 91 or 119 < encrypt < 123:
                encrypt -= 26
            cipher_text += chr(encrypt + 3)
    return cipher_text


def decrypt_caesar(cipher_text: str) -> str:
    plaintext = ''
    for i in cipher_text:
        if not (65 <= ord(i) <= 90 or 97 <= ord(i) <= 122):
            plaintext += i
        else:
            decrypt = ord(i)
            if 64 < decrypt < 68 or 96 < decrypt < 100:
                decrypt += 26
            plaintext += chr(decrypt - 3)
    return plaintext


a = input('Enter your word: ')
print(encrypt_caesar(a))
decrypt = encrypt_caesar(a)
print(decrypt_caesar(decrypt))
