import bcrypt
import random as rd

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8') , bcrypt.gensalt())



def check_password(password, hash_password):
    return bcrypt.checkpw(password.encode("utf-8"), hash_password)


def generate_token():
    return str(rd.random()).split(".")[1][0:5]