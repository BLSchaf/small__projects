import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption('A* Path Finding Algorithm')

RED = (220, 50, 20)
GREEN = (20, 220, 50)
Blue = (20, 50, 220)
YELLOW = (220, 200, 20)
WHITE = (240, 240, 240)
BLACK  = (40, 40, 40)
PURPLE = (128, 20, 100)
ORANGE = (220, 150, 20)
GREY = (128, 128, 128)
TURQUOISE = (60, 220, 200)

ROWS = 20
NODE_WIDTH = WIDTH // ROWS

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y =row * width
        self.width = width
        self.total_rows = total_rows
        self.color = WHITE
        #self.neighbours = []
        
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self):
        pygame.draw.rect(WINDOW, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        '''Updates list of valid neighbours'''
        self.neighbours = []
        # Check node on top
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])
        # Check node below
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])
        # Check node left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])
        # Check node right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        '''used nowhere'''
        return False


def reconstruct_path(came_from, current):
    while current in came_from: # current is the key of the dict came_from
        current = came_from[current]
        current.make_path()


def h(p1, p2):
    ''' shortest distance to get from node to end'''
    col1, row1 = p1
    col2, row2 = p2
    return abs(col1-col2) + abs(row1-row2)

def a_star(grid, start, end):
    count = 0
    open_set = PriorityQueue() #get smallest element out of it (uses heap sort algo?)
    open_set.put((0, count, start))
    came_from = {}
    
    # g_score -> distance to arrive at this node
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0 # whats start?
    
    # f_score -> distance to arrive at this node + distance to end node
    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start} # dict to check if node is alrdy opened

    while not open_set.empty():
        # Since a while loop is running, make exit available again
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                                    
                if event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    GRID = make_grid()
                    break

        current = open_set.get()[2] # [2] is the node (at first, the start node) -> empties the queue
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end)
            end.make_end()
            start.make_start()
            draw_grid(grid)
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1 # all steps are 1
            
            if temp_g_score < g_score[neighbour]:
                # if this is a better way to that node than any way before
                # update its values
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set_hash: # this is what the hash is used for
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open() # change color (is to be explored)

        draw_grid(grid)

        if current != start:
            current.make_closed() # change color (was explored)
                
    return False

def make_grid():
    grid = []
    
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            node = Node(i, j, NODE_WIDTH, ROWS)
            grid[i].append(node)
    return grid

def draw_lines():
    
    for i in range(ROWS):
        pygame.draw.line(WINDOW, GREY, (0, i*NODE_WIDTH), (WIDTH, i*NODE_WIDTH))
    for j in range(ROWS):
        pygame.draw.line(WINDOW, GREY, (j*NODE_WIDTH, 0), (j*NODE_WIDTH, WIDTH))

def draw_grid(grid):
    WINDOW.fill(BLACK)

    for row in grid:
        for node in row:
            node.draw()

    draw_lines()
    pygame.display.update()


#draw(WINDOW, [], 10, WIDTH)
def get_clicked_node(pos):
    x, y = pos
    row = y // NODE_WIDTH
    col = x // NODE_WIDTH

    return row, col

def main():
    GRID = make_grid()
    
    start = None
    end = None
    run = True

    while run:
        draw_grid(GRID) # lines included
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_node(pos)
                node = GRID[row][col]
                
                if not start and node != end:
                    start = node
                    start.make_start()
                
                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()
    
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos() # redundant
                row, col = get_clicked_node(pos)
                node = GRID[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in GRID:
                        for node in row:
                            
                            if node.is_start():
                                pass
                            elif node.is_end():
                                pass
                            elif node.is_barrier():
                                pass
                            else:
                                node.reset()

                            node.update_neighbours(GRID)
                    a_star(GRID, start, end)

                if event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    GRID = make_grid()
        
    pygame.quit()

main()





        
