import secrets
# generate unqiue key for x-api-key once
clients = ["client1", "client2", "client3"]

VALID_API_KEYS = {}

for name in clients:
    key = secrets.token_hex(32)
    VALID_API_KEYS[key] = name

print("Generated API keys:")
for k, v in VALID_API_KEYS.items():
    print(f"Name: {v}, Key: {k}")
