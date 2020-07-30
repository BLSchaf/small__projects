# check input
while True:
    stair_size = input("How many steps does the stair have? ")
    
    try:
        N = int(stair_size)
        if N <= 0:  # if not a positive int print message and ask for input again
            print("Sorry, input must be a positive integer bigger than 0\n Try again")
            continue
        
        break
    except ValueError:
        print("That's not an int!")


while True:
    redo = False
    step_size = input("What are possible step sizes? (e.g. 1, 2) ")
    try:
        X = list(map(int, step_size.split(',')))
        for i in X:
            if i <= 0:
                redo = True
                print("Sorry, input must be a positive integer bigger than 0\n Try again")
                break
        if redo:
            continue
        else:
            break
    except ValueError:
        print("Please use this format: int, int, ...")
