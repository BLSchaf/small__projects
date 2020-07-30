from stairs_input_check import N, X

def num_ways(N, X, solution):
    '''return how many ways there are to climb the stair'''
    print(N, X, solution)
    
    for i in X:
        if N - i == 0:
            print(solution, '+1')
            return True
        elif N - i > 0:
            print('next level')
            if num_ways(N-i, X, solution):
                solution += 1
        else:
            continue
    
    return solution

solution = 0
print(num_ways(N, X, solution))

'''
idea: breadth first
check all valid options
add to solution when last step reached
if path gives no valid solutions, do nothing?

optimization idea: memoization, steps left repeats..
'''
