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
        
        if not os.path.exists('private_key.pem'):
            # store the private key in a file
            with open('private_key.pem', 'wb') as filekey:
                filekey.write(key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))

        if not os.path.exists('public_key.pem'):
            # store the public key in a file
            public_key = key.public_key()
            with open('public_key.pem', 'wb') as filekey:
                filekey.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))

        # generate a symmetric key if it doesn't exist
        if not os.path.exists('symmetric_key.pem'):
            symmetric_key = Fernet.generate_key()

            # write the symmetric key to a file
            with open('symmetric_key.pem', 'wb') as filekey:
                filekey.write(symmetric_key)

    @staticmethod
    def encrypt_file():
        # load the public key
        with open('public_key.pem', 'rb') as filekey:
            public_key = serialization.load_pem_public_key(
                filekey.read(),
                backend=default_backend()
            )

        # generate a symmetric key
        with open('symmetric_key.pem', 'rb') as filekey:
            symmetric_key = filekey.read()

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
        # check if the necessary files exist
        if not os.path.exists('log.txt'):
            print("Log file not found.")
            return

        if not os.path.exists('private_key.pem'):
            print("Private key file not found.")
            return

        if not os.path.exists('encrypted_key.pem'):
            print("Encrypted symmetric key file not found.")
            return

        # load the private key
        with open('private_key.pem', 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        # load the encrypted symmetric key
        with open('encrypted_key.pem', 'rb') as filekey:
            encrypted_key = filekey.read()

        # decrypt the symmetric key using the private key
        try:
            symmetric_key = private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except ValueError:
            print("Failed to decrypt the symmetric key. Please ensure the correct private key is used.")
            return

        # use the symmetric key to decrypt the file content
        cipher_suite = Fernet(symmetric_key)
        with open('log.txt', 'rb') as file:
            encrypted_data = file.read()

        try:
            decrypted_data = cipher_suite.decrypt(encrypted_data)
        except ValueError:
            print("Failed to decrypt the file content. Please ensure the encrypted data is not corrupted.")
            return

        # overwrite the original file with the decrypted content
        with open('log.txt', 'wb') as file:
            file.write(decrypted_data)

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
