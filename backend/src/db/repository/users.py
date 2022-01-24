from hashlib import sha256

fake_users_db = {
    "bob": {
        "username": "bob",
        "bio": "Dummy info about me",
        "email": "bob@example.com",
        "hashed_password": sha256('secret'.encode('utf-8')).hexdigest(),
        "permission": ["right:view"],
    },
    "alice": {
        "username": "alice",
        "bio": "Dummy info about me",
        "email": "alicechains@example.com",
        "hashed_password": sha256('secret'.encode('utf-8')).hexdigest(),
        "permission": "right:full",
    },
}

