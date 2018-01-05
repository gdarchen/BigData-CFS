import time
import nltk
import numpy as np

def time_and_exception(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        exception = None
        res = None
        try:
            res = func(*args, **kwargs)
        except Exception as err:
            exception = err
        end = time.time()
        elapsed_time = end - start
        return res, elapsed_time, exception
    return wrapper
