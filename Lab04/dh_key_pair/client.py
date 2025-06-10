from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Tạo cặp khóa DH từ tham số
def generate_client_key_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

# Tính khóa bí mật chung
def derive_shared_secret(private_key, server_public_key):
    shared_key = private_key.exchange(server_public_key)
    return shared_key

def main():
    # Load khóa công khai của server từ file
    with open("server_public_key.pem", "rb") as f:
        server_public_key = serialization.load_pem_public_key(f.read())

    # Lấy các tham số DH từ public key
    parameters = server_public_key.parameters()

    # Tạo cặp khóa client
    private_key, public_key = generate_client_key_pair(parameters)

    # Tính khóa chung
    shared_secret = derive_shared_secret(private_key, server_public_key)
    print("Shared Secret:", shared_secret.hex())

if __name__ == "__main__":
    main()