cache = {}

def fib(n):
    if n in cache:
        return cache[n]
    
    if n == 1:
        cache[n] = 1
    elif n == 2:
        cache[n] = 1
    elif n > 2:
        cache[n] = fib(n-1) + fib(n-2)

    return cache[n]

for n in range(1, 11):
    print(n, ':', fib(n))
        
