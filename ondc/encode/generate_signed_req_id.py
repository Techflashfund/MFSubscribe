import base64
from nacl.signing import SigningKey

# Your base64 encoded Ed25519 full private key (private + public)
private_key_base64 = "XqDH+WrscKFZY7YfWU+B/JY3fyC3JFqvtwITfVAJvlOHNyJJVvQSWyP3dR+nt7CMTljYu5F9TfyBS6zm4mhazw=="
unique_key_id = "001"

# Decode and take only the first 32 bytes
private_key_bytes = base64.b64decode(private_key_base64)[:32]

signing_key = SigningKey(private_key_bytes)
signed = signing_key.sign(unique_key_id.encode())

signature_base64 = base64.b64encode(signed.signature).decode()

print("SIGNED_UNIQUE_REQ_ID =", signature_base64)
