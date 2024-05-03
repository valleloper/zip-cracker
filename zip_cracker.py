import pyzipper
import itertools
import string
import concurrent.futures
import time

MIN_PASSWORD_LENGTH = 1
MAX_PASSWORD_LENGTH = 8
NUM_OF_WORKER = 8


def crack(zip_file, password):
    try:
        zip_file.extractall(pwd=str.encode(password))
        return password  # Return the successful password
    except:
        return None  # Return None for invalid passwords


def crack_zip(path):
    start = time.time()
    zip_file = pyzipper.AESZipFile(path)
    characters = string.ascii_letters + string.digits + string.punctuation

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_OF_WORKER) as executor:
        for length in range(MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH + 1):
            for password in map("".join, itertools.product(characters, repeat=length)):
                future = executor.submit(crack, zip_file, password)
                if future.result():
                    print("Success: Password is", future.result())
                    end = time.time()
                    print("Time:", end - start)
                    return  # Exit the function once a password is found


if __name__ == "__main__":
    path = "test.zip"
    crack_zip(path)
