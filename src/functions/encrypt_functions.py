from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet
import os


class EncryptFunc:

    @staticmethod
    def generate_key():
        # key generation
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        # store the private key in a file
        with open('private_key.pem', 'wb') as filekey:
            filekey.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # store the public key in a file
        public_key = key.public_key()
        with open('public_key.pem', 'wb') as filekey:
            filekey.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    @staticmethod
    def encrypt_file():
        # load the public key
        with open('public_key.pem', 'rb') as filekey:
            public_key = serialization.load_pem_public_key(
                filekey.read(),
                backend=default_backend()
            )

        # generate a symmetric key
        symmetric_key = Fernet.generate_key()

        # use the symmetric key to encrypt the file
        cipher_suite = Fernet(symmetric_key)
        with open('log.txt', 'rb') as filekey:
            encrypted_file = cipher_suite.encrypt(filekey.read())

        # use the public key to encrypt the symmetric key
        encrypted_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # write the encrypted symmetric key to a file
        with open('encrypted_key.pem', 'wb') as filekey:
            filekey.write(encrypted_key)

        # overwrite the original file with the encrypted content
        with open('log.txt', 'wb') as filekey:
            filekey.write(encrypted_file)


    @staticmethod
    def decrypt_file():
        # load the private key

        if not os.path.exists('log.txt'):
            print("Log file not found.")
            return

        with open('private_key.pem', 'rb') as filekey:
            private_key = serialization.load_pem_private_key(
                filekey.read(),
                password=None,
                backend=default_backend()
            )

        # load the encrypted symmetric key
        with open('encrypted_key.pem', 'rb') as filekey:
            encrypted_key = filekey.read()

        # use the private key to decrypt the symmetric key
        symmetric_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # use the symmetric key to decrypt the file
        cipher_suite = Fernet(symmetric_key)
        with open('log.txt', 'rb') as filekey:
            decrypted_file = cipher_suite.decrypt(filekey.read())

        # overwrite the original file with the decrypted content
        with open('log.txt', 'wb') as filekey:
            filekey.write(decrypted_file)

    def encrypt_value(value):
        # load the public key
        with open('public_key.pem', 'rb') as filekey:
            public_key = serialization.load_pem_public_key(
                filekey.read(),
                backend=default_backend()
            )

        if isinstance(value, int):
            value = str(value)

        # use the public key to encrypt the value
        encrypted_value = public_key.encrypt(
            value.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_value
    
    def encrypt_int_value(value):
        # load the public key
        with open('public_key.pem', 'rb') as filekey:
            public_key = serialization.load_pem_public_key(
                filekey.read(),
                backend=default_backend()
            )

        # use the public key to encrypt the value
        encrypted_value = public_key.encrypt(
            str(value).encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return encrypted_value
    
    def decrypt_value(value):
        # load the private key
        with open('private_key.pem', 'rb') as filekey:
            private_key = serialization.load_pem_private_key(
                filekey.read(),
                password=None,
                backend=default_backend()
            )


        # use the private key to decrypt the value
        decrypted_value = private_key.decrypt(
            value,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Check if value could be int if so return int
        try:
            return int(decrypted_value.decode())
        except ValueError:
            pass

        return decrypted_value.decode()
