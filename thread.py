import time
import threading

def do_sth(inp):
    print('You typed: ' + inp)

def wait_for_input(prompt='> '):
    inp = input(prompt)
    do_sth(inp)

def print_stuff(n):
    while x.is_alive():
        n += 1
        print(n, 'Aggressivley Waiting...!')

x = threading.Thread(target=wait_for_input, args=())
x.start()

n = 0
y = threading.Thread(target=print_stuff, args=(n,))
y.start()

#x.join()
