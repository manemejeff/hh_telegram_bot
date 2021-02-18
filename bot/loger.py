# logging function
# maybe should try to play with message format


def log_error(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f'Error: {e}')
            raise e

    return inner
