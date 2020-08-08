import pygame
import sys
from newtwork import Network

pygame.init()

WIDTH = 800
HEIGHT = 450

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Client')


class Button():
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.width = 150
        self.height = 100
        self.rect = (self.x, self.y, self.width, self.height)

        self.color = color

    def draw(self):
        pygame.draw.rect(WINDOW, self.color, self.rect)
        font = pygame.font.SysFont('Matura MT Script Capitals', 40)
        text = font.render(self.text, 1, (220, 220, 220))

        WINDOW.blit(
            text,
            (
                self.x + (self.width - text.get_width())//2,
                self.y + (self.height - text.get_height())//2
            )
        )

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width\
           and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


buttons = [Button('Rock', 50, 50, (30, 30, 30)),
           Button('Paper', 300, 50, (30, 30, 30)),
           Button('Scissors', 550, 50, (30, 30, 30))]
        

    
def redraw_window(game, player):
    WINDOW.fill((80, 80, 80))
    if not game.connected():
        font = pygame.font.SysFont('Matura MT Script Capitals', 50, 1)
        text = font.render('Waiting for connection', 1, (220, 220, 220)) # True for bolt
        WINDOW.blit(text, ((WIDTH - text.get_width())//2, (HEIGHT - text.get_height())//2))
        
    else:
        font = pygame.font.SysFont('Matura MT Script Capitals', 60)
        text = font.render('Your Move', 1, (220, 220, 220))
        WINDOW.blit(text, (80, 200))
        text = font.render('Opponents Move', 1, (220, 220, 220))
        WINDOW.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.both_moved():
            text1 = font.render(move1, 1, (220, 220, 220))
            text2 = font.render(move2, 1, (220, 220, 220))
        else:
            if player == 0 and game.p1_moved:
                text1 = font.render(move1, 1, (220, 220, 220))
            elif player == 1 and game.p1_moved:
                text1 = font.render('Locked in', 1, (220, 220, 220))
            else: # p1_moved = False
                text1 = font.render('Waiting...', 1, (220, 220, 220))

            if player == 0 and game.p2_moved:
                text2 = font.render('Locked in', 1, (220, 220, 220))
            elif player == 1 and game.p2_moved:
                text2 = font.render(move2, 1, (220, 220, 220))
            else: # p2_moved = False
                text2 = font.render('Waiting...', 1, (220, 220, 220))
                
                
        if player == 0:
            WINDOW.blit(text1, (80, 350))
            WINDOW.blit(text2, (380, 350))

        else:
            WINDOW.blit(text1, (380, 350))
            WINDOW.blit(text2, (80, 350))

        for button in buttons:
            button.draw()
    
    pygame.display.update()



def main():
    run = True
    clock = pygame.time.Clock()

    n = Network()
    player = int(n.get_player())
    print('You are player', player)

    while run:
        clock.tick(60)
        
        try: # ask server to send tha game state
            game = n.send('get')
        except:
            print('Could not get game state')
            break

        if game.both_moved():
            redraw_window(game, player)
            pygame.time.delay(200)
            try:
                game = n.send('reset') # make the server reset the game and send the state back
            except:
                print('Could not get game state')
                break
            
            winner = game.winner()
            font = pygame.font.SysFont('Matura MT Script Capitals', 90)

            if (winner == 0 and player == 0)\
               or (winner == 1 and player == 1):
                text = font.render('You won!', 1, (80, 220, 30), (50, 50, 50))
            elif winner == -1:
                text = font.render('Tie Game.', 1, (220, 220, 220), (50, 50, 50))
            else:
                text = font.render('You Lost...', 1, (220, 80, 30), (50, 50, 50))
                
            WINDOW.blit(text, ((WIDTH - text.get_width())//2, (HEIGHT - text.get_height())//2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game.connected():
                    run = False
                    break
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    # game.connected() is True if both players connected to this game
                    if button.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1_moved:
                                n.send(button.text)
                        if player == 1:
                            if not game.p2_moved:
                                n.send(button.text)
        
        try:
            redraw_window(game, player)
        except:
            pass

        
def menu():
    WINDOW.fill((80, 80, 80))
    font = pygame.font.SysFont('Matura MT Script Capitals', 60)
    text = font.render('Click to play.', 1, (220, 220, 220), True)
    WINDOW.blit(text, ((WIDTH - text.get_width())//2, (HEIGHT - text.get_height())//2))
    pygame.display.update()
        
    run = True
    while run:
        
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False 
                break
    main()
        

        
while True:
    menu()
