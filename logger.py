import logging

def log_action(func):
    def wrapper(*args, **kwargs):
        logging.basicConfig(filename='/root/actions.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} was called and executed successfully.")
        return result
    return wrapper
