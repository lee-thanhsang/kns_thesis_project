import time
import random
import bcrypt


def generate_cookie():
    time_now_str = str(round(time.time() * 1000))
    rand_str = str(random.randint(0, 1000))
    base_str = time_now_str + rand_str
    cookie = bcrypt.hashpw(base_str.encode('utf-8'), bcrypt.gensalt())
    return str(cookie)
