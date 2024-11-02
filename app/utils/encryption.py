from cryptography.fernet import Fernet
import os

class Encryption:
    def __init__(self):
        self._key = os.getenv('ENCRYPTION_KEY').encode()
        self._cipher = Fernet(self._key)

    def encrypt(self, data):
        return self._cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted_data):
        return self._cipher.decrypt(encrypted_data).decode()