import pygame
import math
from queue import PriorityQueue

ROWS = 19
NODE_WIDTH = 40
RADIUS = NODE_WIDTH // 2
WIDTH = ROWS * NODE_WIDTH

WHITE = (240, 240, 240)
BLACK  = (40, 40, 40)
ORANGE = (230, 150, 25)

WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Go Board')


class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * NODE_WIDTH
        self.y =row * NODE_WIDTH
        self.center = (self.x + RADIUS, self.y + RADIUS)
        self.neighbours = []
        self.group = [self]
        self.color = None

    def __repr__(self):
        if self.color:
            return f'Black {self.row}.{self.col}' if self.color == BLACK else f'White {self.row}.{self.col}'
        return str(None)

    def draw(self):
        if self.color:
            pygame.draw.circle(WINDOW, self.color, self.center, RADIUS)   

    def update_neighbours(self, board):
        '''Updates list of valid neighbours'''
        # Check node on top
        if self.row > 0:
            self.neighbours.append(board.position[self.row - 1, self.col])
        # Check node below
        if self.row < ROWS - 1:
            self.neighbours.append(board.position[self.row + 1, self.col])
        # Check node left
        if self.col > 0:
            self.neighbours.append(board.position[self.row, self.col - 1])
        # Check node right
        if self.col < ROWS - 1:
            self.neighbours.append(board.position[self.row, self.col + 1])
        
    def get_group(self, group):
        if self not in group:
            group.append(self)
        for neighbour in self.neighbours:
            if self.color == neighbour.color and not neighbour in group:
                neighbour.get_group(group)
        return group

    def has_liberty(self):
        for node in self.group:
            for neighbour in node.neighbours:
                if neighbour.color == None:
                    return True
        return False

    def draw_last_move(self):
        pygame.draw.circle(WINDOW, (220, 70, 30), self.center, RADIUS//2)
        pygame.draw.circle(WINDOW, self.color, self.center, RADIUS//3)


class Board():
    def __init__(self):
        self.position = {}
        for row in range(ROWS):
            for col in range(ROWS):
                self.position[row,col] = Node(row, col)
                
        for node in self.position.values():
            node.update_neighbours(self)

    def reset(self):
        for node in self.position.values():
            node.color = None
            #node.group = [node]
    
    def get_clicked_node(self, pos):
        x, y = pos
        row = y // NODE_WIDTH
        col = x // NODE_WIDTH

        return self.position[row,col]

    # board or node method? -> kinda node
    def place_stone(self, node, turn):
        if turn == 'black':
            node.color = BLACK
        elif turn == 'white':
            node.color = WHITE

    # board or node method? -> kinda node
    def remove_stone(self, node):
         node.color = None
         

    # board or node method? -> kinda node
    def update_board(self, node):
        for neighbour in node.neighbours:
            # suicide without enemy neighbours -> check first for enemy groups, then for self.group
            if node.color != neighbour.color and neighbour.color != None:
                neighbour.group = neighbour.get_group([])
                if not neighbour.has_liberty():
                    for stone in neighbour.group:
                        self.remove_stone(stone)
                        
        node.group = node.get_group([])
        if not node.has_liberty():
            print('suicide')
            for stone in node.group:
                self.remove_stone(stone)

        
            

    def draw(self, last_stone):
        WINDOW.fill(ORANGE)
        for row in range(ROWS):
            pygame.draw.line(WINDOW,
                             BLACK,
                             (0 + RADIUS, row*NODE_WIDTH + RADIUS),
                             (NODE_WIDTH*ROWS - RADIUS, row*NODE_WIDTH + RADIUS))
            
        for col in range(ROWS):
            pygame.draw.line(WINDOW,
                             BLACK,
                             (col*NODE_WIDTH + RADIUS, 0 + RADIUS),
                             (col*NODE_WIDTH + RADIUS, NODE_WIDTH*ROWS - RADIUS))

        pygame.draw.circle(WINDOW,
                           BLACK,
                           (ROWS//2*NODE_WIDTH + RADIUS, ROWS//2*NODE_WIDTH + RADIUS),
                           RADIUS//3)
        
        for node in self.position.values():
            node.draw()

        if last_stone:
            last_stone.draw_last_move()
                
        pygame.display.update()



def main():
    board = Board()
##    for node in self.position.values():
##            node.update_neighbours(self)
        
    turn = 'black'
    last_stone = None
    run = True

    while run:
        board.draw(last_stone)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                node = board.get_clicked_node(pos)
                last_stone = node
                
                if node.color == None:
                    board.place_stone(node, turn)
                    turn = 'black' if turn == 'white' else 'white'
                    board.update_board(node)                        
    
            elif pygame.mouse.get_pressed()[1]:
                #remove last move, not any move clicked on
                pos = pygame.mouse.get_pos() # redundant
                node = board.get_clicked_node(pos)
                print(node)
                print(node.group, node.has_liberty())

            elif pygame.mouse.get_pressed()[2]:
                #remove last move, not any move clicked on
                pos = pygame.mouse.get_pos() # redundant
                node = board.get_clicked_node(pos)
                if node.color != None:
                    board.remove_stone(node)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    last_stone = None
                    turn = 'black'
                    board.reset()
        
    pygame.quit()

main()





        
