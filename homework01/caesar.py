def encrypt_caesar(plaintext: str) -> str:
     """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
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
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
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
