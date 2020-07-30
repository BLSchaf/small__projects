
''' visualize sorting algorithms'''
# first, implement some sorting algos (bubble, quick..)

# second, visualize random data, like bars, with angles or len or color to sort
# all of the above as rainbow

# random numbers could also be a sin() or something

import pygame
import random
import time
import math

''' sorting algorithms '''
# test arr
arr = [3, 5, 6, 1, 8, 7, 2, 0, 9, 4, 3, 8, 7, -10, 0.5]
print(arr)

def bubble_sort(arr):
    ''' can be implemented with while or for loop as outer loop
        I like the while loop better '''
    sorted_flag = False
    i = len(arr)
    while not sorted_flag:
        sorted_flag = True
        i -= 1
        for j in range(i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                sorted_flag = False
    return arr

def quick_sort(*args):
    pass

print(bubble_sort(arr))
print(bubble_sort(arr))

''' visualization '''
WIDTH = 800
HEIGHT = 400

# initialize window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # save as variable to draw on
pygame.display.set_caption('Sorting Algorithms')

#time.sleep(5)

# setup - number of bars and their values
bar_width = 5
bar_space = 1
num_bars = WIDTH // (bar_width + bar_space)
bar_heights = [random.randint(1,HEIGHT) for _ in range(num_bars)]

# main loop
i = 0
j = 0
swaps = 0
swap_flag = False
sorted_flag = False

run = True
while run:

    # draw static
    WINDOW.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            run = False
            #break
        
    for n, bar_height in enumerate(bar_heights):
        x = n * (bar_width + bar_space)
        pygame.draw.rect(WINDOW, (255, 255, 255), (x, HEIGHT, bar_width, -bar_height), 0)

    pygame.display.update()
    
    # to not instatnly sort we need to implement bubble sort another way
    # bubble_sort(bar_heights)
    
    # new bubble sort
    if not sorted_flag:
        ''' # draw each outer iteration
        time.sleep(0.1)
        sorted_flag = True
        for j in range(len(bar_heights) - 1 - i):
            if bar_heights[j] > bar_heights[j+1]:
                bar_heights[j], bar_heights[j+1] = bar_heights[j+1], bar_heights[j]
                swaps += 1
                sorted_flag = False
        i += 1
        '''
        #''' # draw each swap
        if bar_heights[j] > bar_heights[j+1]:
            bar_heights[j], bar_heights[j+1] = bar_heights[j+1], bar_heights[j]
            swaps += 1
            swap_flag = True
        j += 1
        
        if j >= len(bar_heights) - 1 - i:
            j = 0
            i += 1
            if swap_flag:
                sorted_flag = False
                swap_flag = False
            else:
                sorted_flag = True
        #'''
    else:
        run = False

