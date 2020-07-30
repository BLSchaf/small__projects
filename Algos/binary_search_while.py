import random
import math

def guess_number(x, arr):
    ''' Guess the numer in sorted array '''
    lives = max(1, round(math.log2(len(arr)))) # minimum 1 live
    print(f'The number the CPU is looking for is {x}. It has {lives} lives!')

    i = 0 # start index
    j = (len(arr) - 1) // 2 # mid index
    k = len(arr) - 1 # end index
    
    while arr[j] != x and lives > 0: # try again
        lives -= 1
        print(f'Guessed: {arr[j]}')
        if x < arr[j]:
            print('x is smaller')
            k = j
            j -= math.ceil((j - i) / 2)
        else:
            print('x is bigger')
            i = j
            j += math.ceil((k - j) / 2)
            
    if lives == 0:
            print('No tries left... Bad CPU!')
    else:
        return f'Jau, die gesuchte Zahl ist {arr[j]}'


while True:
    arr_size = input('Search between 1 to ')
    try:
        val = int(arr_size)
        if val < 0:  # if not a positive int print message and ask for input again
            print("Sorry, input must be a positive integer, try again")
            continue
        break
    except ValueError:
        print("That's not an int!")
        
x = random.randrange(1, val+1)
arr = [n for n in range(1, val+1 )]
print(guess_number(x, arr))
