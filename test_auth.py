from auth import hash_password, verify_password

# Test hash
password = "123456"
hashed = hash_password(password)
print(f"Original: {password}")
print(f"Hashed: {hashed}")

# Test verify
is_correct = verify_password("123456", hashed)
print(f"Password correct: {is_correct}")

is_wrong = verify_password("wrong", hashed)
print(f"Wrong password: {is_wrong}")
