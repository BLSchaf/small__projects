import random
import math

def guess_number(x, arr, lives):
    ''' Guess the numer in sorted array '''

    j = len(arr) // 2
    print(arr[j])
    
    if arr[j] == x:
        return f'Jau, die gesuchte Zahl ist {arr[j]}'
        
    if lives > 0:
        lives -= 1
        if x < arr[j]:
            print('x is smaller')
            arr = arr[:j]
        else:
            print('x is bigger')
            arr = arr[j:]
            
        return guess_number(x, arr, lives)
    
    else:
        return 'Vorbei'


# check input
while True:
    arr_size = input('Search between 1 to ')
    try:
        val = int(arr_size)
        if val <= 0:  # if not a positive int print message and ask for input again
            print("Sorry, input must be a positive integer bigger than 0\n Try again")
            continue
        break
    except ValueError:
        print("That's not an int!")


# settings
x = random.randrange(1, val+1)
arr = [n for n in range(1, val+1 )]
lives = max(1, round(math.log2(len(arr)))) # minimum 1 live
print(f'The number the CPU is looking for is {x}. It has {lives} lives!')

print(guess_number(x, arr, lives))

