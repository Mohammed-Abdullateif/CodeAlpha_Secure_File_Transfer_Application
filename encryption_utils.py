# في ملف `encryption_utils.py`

from Crypto.Cipher import AES # type: ignore
from Crypto.Protocol.KDF import scrypt # type: ignore
from Crypto.Random import get_random_bytes # type: ignore

def generate_key(password):
    salt = get_random_bytes(AES.block_size)
    key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)
    return key

def encrypt_file(file_path, key):
    cipher = AES.new(key, AES.MODE_EAX)
    with open(file_path, 'rb') as file:
        data = file.read()
        ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(file_path + '.enc', 'wb') as file_encrypted:
        [file_encrypted.write(x) for x in (cipher.nonce, tag, ciphertext)]

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file_encrypted:
        nonce, tag, ciphertext = [file_encrypted.read(x) for x in (16, 16, -1)]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
    with open(file_path[:-4], 'wb') as file:
        file.write(data)
