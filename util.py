from hashlib import sha256

def stringify_attrs(*kargs):
    return " | ".join(kargs)

def sha256_hash(s):
    return sha256(s.encode("utf-8")).hexdigest()
