import secrets
import string

# Generate a secure random 256-bit JWT signing key (32 bytes * 8 = 256 bits)
def generate_jwt_secret_key():
    # Create a random key of 32 bytes (256 bits)
    random_bytes = secrets.token_bytes(32)
    
    # Optionally, encode it in hexadecimal or base64 (for storage purposes)
    hex_key = random_bytes.hex()  # Hexadecimal encoding
    return hex_key

# Example usage
jwt_secret_key = generate_jwt_secret_key()
print("Generated JWT Secret Key (Hex):", jwt_secret_key)