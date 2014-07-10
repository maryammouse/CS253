import random
import string
import hashlib

def hash_str(s):
    return hashlib.sha256(s).hexdigest()

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

# implement the function make_pw_hash(name, pw) that returns a hashed password
# of the format:
# HASH(name + pw + salt),salt
# use sha256

def make_pw_hash(name, pw):
    salty = make_salt()
    return hash_str(name + pw + salty) + ',' + salty
