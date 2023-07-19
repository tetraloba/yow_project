from time import sleep

def delayed_print(text:str = '', end = '\n'):
    for char in text:
        print(char, end='', flush=True)
        sleep(0.0009)
    print(end, end='')
