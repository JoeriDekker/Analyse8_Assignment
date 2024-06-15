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
        # Create a private key
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        # Create a private key if none exists
        if not os.path.exists('private_key.pem'):
            with open('private_key.pem', 'wb') as filekey:
                filekey.write(key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))

        # Create a public key if none exists
        if not os.path.exists('public_key.pem'):
            public_key = key.public_key()
            with open('public_key.pem', 'wb') as filekey:
                filekey.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))

        # Create a symmetric key if none exists
        if not os.path.exists('symmetric_key.pem'):
            symmetric_key = Fernet.generate_key()

            # Write the symmetric key to file
            with open('symmetric_key.pem', 'wb') as filekey:
                filekey.write(symmetric_key)

    @staticmethod
    def encrypt_file():
        #  Load the public key
        with open('public_key.pem', 'rb') as filekey:
            public_key = serialization.load_pem_public_key(
                filekey.read(),
                backend=default_backend()
            )

        # Load the symmetric key
        with open('symmetric_key.pem', 'rb') as filekey:
            symmetric_key = filekey.read()

        # Encrypt the file with the symmetric key
        cipher_suite = Fernet(symmetric_key)
        with open('log.txt', 'rb') as filekey:
            encrypted_file = cipher_suite.encrypt(filekey.read())

        # Encrypt the symmetric key with the public key
        encrypted_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Set the encrypted symmetric key to the file
        with open('encrypted_key.pem', 'wb') as filekey:
            filekey.write(encrypted_key)

        # Write encrypted data to log
        with open('log.txt', 'wb') as filekey:
            filekey.write(encrypted_file)


    @staticmethod
    def decrypt_file():
        # Chek if files exist
        if not os.path.exists('log.txt'):
            print("Log file not found.")
            return

        if not os.path.exists('private_key.pem'):
            print("Private key file not found.")
            return

        if not os.path.exists('encrypted_key.pem'):
            print("Encrypted symmetric key file not found.")
            return

        # Load the private key
        with open('private_key.pem', 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        # Load the encrypted symmetric key
        with open('encrypted_key.pem', 'rb') as filekey:
            encrypted_key = filekey.read()

        # Use the private key to decrypt the symmetric key
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

        # Use the symmetric key to decrypt the file content
        cipher_suite = Fernet(symmetric_key)
        with open('log.txt', 'rb') as file:
            encrypted_data = file.read()

        try:
            decrypted_data = cipher_suite.decrypt(encrypted_data)
        except ValueError:
            print("Failed to decrypt the file content. Please ensure the encrypted data is not corrupted.")
            return

        # Write the dycrypted data to the log
        with open('log.txt', 'wb') as file:
            file.write(decrypted_data)

    def encrypt_value(value):
        # Load the public key
        with open('public_key.pem', 'rb') as filekey:
            public_key = serialization.load_pem_public_key(
                filekey.read(),
                backend=default_backend()
            )

        # Convert value to sting if int
        if isinstance(value, int):
            value = str(value)

        # Use the public key to encrypt the value
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
        # Load the public key
        with open('public_key.pem', 'rb') as filekey:
            public_key = serialization.load_pem_public_key(
                filekey.read(),
                backend=default_backend()
            )

        # Encrypt the value with the public key
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
        # Load the private key
        with open('private_key.pem', 'rb') as filekey:
            private_key = serialization.load_pem_private_key(
                filekey.read(),
                password=None,
                backend=default_backend()
            )


        # Decrypt the value with the private key
        decrypted_value = private_key.decrypt(
            value,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # Return int if value is int
        try:
            return int(decrypted_value.decode())
        except ValueError:
            pass

        return decrypted_value.decode()
