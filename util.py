from hashlib import sha256

def stringify_attrs(*kargs):
    return " | ".join(kargs)

def sha256_hash(s):
    return sha256(s.encode("utf-8")).hexdigest()

class SessionState:
    def __init__(self, signed_in=False, is_instructor=False, from_dict=None):
        self.signed_in = signed_in
        self.is_instructor = is_instructor
        if from_dict is not None:
            self.signed_in = from_dict["signed_in"]
            self.is_instructor = from_dict["is_instructor"]
    
    def to_dict(self):
        return {"signed_in": self.signed_in, "is_instructor": self.is_instructor}
