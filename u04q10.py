import hashlib

# ASK ABOO ABOUT IT :D
def hash_str(s):
    return hashlib.md5(s).hexdigest()

def make_secure_val(s):
    return "%s,%s" % (s, hash_str(s))

# -----------------
# User Instructions
#
# Implement the function check_secure_val, which takes a string of the format
# s,HASH
# and returns s if hash_str(s) == HASH, otherwise None

def check_secure_val(h):
    s = h.split(',')[0]
    if h == make_secure_val(s):
        return s



string = "5,234i9234289374"

print string.split(',')

print string[2:]
