import json
import hashlib

passwords = ["admin", "password123", "123456"]
credentials = {"admin": "", "test_user": "", "almafa": ""}

i = 0
for user in credentials:
    sha_object = hashlib.sha1(passwords[i].encode())
    credentials[user] = sha_object.hexdigest()
    i += 1

with open("creds.json", "w") as f:
    json.dump(credentials, f)
