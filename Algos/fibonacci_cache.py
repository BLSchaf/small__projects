cache = {}

def fib(n, cache=cache):
    if n in cache:
        #print(f'memoization of fib({n})')
        return cache[n]
    
    elif n == 1:
        cache[n] = 1 #{1:1}
        
    elif n == 2:
        cache[n] = 1 #{2:1}

    else:
        cache[n] = fib(n-1) + fib(n-2)
        
    return cache[n]


for i in range(1, 1000000):
    fib(i)
    if i == 999999:
        print(fib(i))
