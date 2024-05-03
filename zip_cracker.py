import pyzipper
import itertools
import string
from threading import Thread
import time

MIN_PASSWORD_LENGTH = 1
MAX_PASSWORD_LENGTH = 8
succes = False
succes_pwd = None


def crack(zip, pwd):
    global succes, succes_pwd
    try:
        zip.extractall(pwd=str.encode(pwd))
        succes = True
        succes_pwd = pwd
        print("Success: Password is " + succes_pwd)
    except:
        pass


def crack_zip(path):
    start = time.time()
    zip_file = pyzipper.AESZipFile(path)
    characters = string.ascii_letters + string.digits + string.punctuation

    for length in range(MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH + 1):
        for password in map("".join, itertools.product(characters, repeat=length)):
            if succes:
                break
            t = Thread(target=crack, args=(zip_file, password))
            t.start()

    end = time.time()
    print("Time: " + str(end - start))


if __name__ == "__main__":
    path = "test.zip"
    crack_zip(path)
