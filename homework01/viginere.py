def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    cipher_text = ''
    i = 0
    while len(keyword) < len(plaintext):
        keyword += keyword[i]
        i += 1
    for i in range(0, len(plaintext)):
        if not (65 <= ord(str(plaintext[i])) <= 90 or 97 <= ord(str(plaintext[i])) <= 122):
            cipher_text += plaintext[i]
        else:
            if 65 <= ord(str(plaintext[i])) <= 90:
                encrypt = ord(str(plaintext[i])) + (ord(str(keyword[i])) - 65)
                if encrypt > 90:
                    encrypt -= 26
            else:
                encrypt = ord(str(plaintext[i])) + (ord(str(keyword[i])) - 97)
                if encrypt > 122:
                    encrypt -= 26
            cipher_text += chr(encrypt)
    return cipher_text


def decrypt_vigenere(cipher_text: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    while len(keyword) < len(cipher_text):
        keyword += keyword
    for i in range(0, len(cipher_text)):
        if not (65 <= ord(str(cipher_text[i])) <= 90 or 97 <= ord(str(cipher_text[i])) <= 122):
            plaintext += cipher_text[i]
        else:
            if 65 <= ord(str(cipher_text[i])) <= 90:
                decrypt = ord(str(cipher_text[i])) - (ord(str(keyword[i])) - 65)
                if decrypt < 65:
                    decrypt += 26
            else:
                decrypt = ord(str(cipher_text[i])) - (ord(str(keyword[i])) - 97)
                if decrypt < 97:
                    decrypt += 26
            plaintext += chr(decrypt)
    return plaintext
