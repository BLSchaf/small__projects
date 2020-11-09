import pygame
import sys
import os
import socket


# Socket Stuff
HEADERSIZE = 10


# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 450, 600

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((SIZE))
pygame.display.set_caption('Chat')

#IMG = pygame.image.load(os.path.join('assets', 'IMG.png'))
menu_font = pygame.font.SysFont('Matura MT Script Capitals', 60, 1)
##menu_label = menu_font.render('Some Menu Title', False, (0,0,0))


class Button():
    def __init__(self, window, msg, font, x, y, w, h, ac, ic):
        self.window = window
        self.msg = msg
        self.font = font
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.ac = ac
        self.ic = ic


    def check(self):
        mouse = pygame.mouse.get_pos()
        
        return self.x <= mouse[0] <= self.x + self.w\
               and self.y <= mouse[1] <= self.y + self.h

    
    def render_font(self):
        self.label = self.font.render(self.msg, 1, (25,25,25))
        self.label_rect = self.label.get_rect()
        self.label_rect.center = ((self.x+(self.w//2)),
                                  (self.y+(self.h//2)))

        self.window.blit(self.label, self.label_rect)


    def draw(self):
        if self.check():
            pygame.draw.rect(self.window, self.ac, self.rect)
        else:
            pygame.draw.rect(self.window, self.ic, self.rect)

        self.render_font()
        

    def draw_clicked(self):
        pygame.draw.rect(self.window, self.ac,
                             (self.x, self.y, self.w, self.h))
        self.render_font()
    

    def is_clicked(self, action=None, args=None):
        if self.check() and pygame.mouse.get_pressed()[0] == 1:
            if args:
                action(*args)
            else:
                action()



def typing(button, limit=280):
    typing = True
    message = ''
    
    while typing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        typing = False
                        break
                    elif event.key == pygame.K_RETURN:
                        typing = False
                        button.msg = message
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        message = message[:-1]
                    elif len(message) < limit:
                        message += event.unicode

            button.msg = message + '_'
            button.draw_clicked()
            pygame.display.update(button.rect)
            

def connect_to_chat(username, ip, port): #button.msg x 3
    print('Connecting...')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, int(port)))
        client_socket.setblocking(False) # .recv won't be blocking
        
        username_header = f'{len(username):<{HEADERSIZE}}'.encode('utf-8')
        client_socket.send(username_header + username.encode('utf-8'))
        chat(client_socket)
        
    except:
        print('Connection failed!')


def menu():
    username_button = Button(WINDOW,
                             'Enter Name',
                             menu_font,
                             50,int(HEIGHT*.1),WIDTH-100,100,
                             (180,180,180),(240,240,240),
                             )

    ip_button = Button(WINDOW,
                       socket.gethostname(),
                       menu_font,
                       50,int(HEIGHT*.46),WIDTH-100,80,
                       (180,180,180),(240,240,240),
                       )

    port_button = Button(WINDOW,
                         '1234',
                         menu_font,
                         50,int(HEIGHT*.6),WIDTH-100,80,
                         (180,180,180),(240,240,240),
                         )

    connect_button = Button(WINDOW,
                            'connect',
                            menu_font,
                            100,int(HEIGHT*.8),WIDTH-200,50,
                            (180,180,180),(240,240,240),
                            )

    # Loop -------------------------------------------------------- #
    while True:

        # Background ---------------------------------------------- #
        WINDOW.fill((25,25,25))
        connection_label = menu_font.render('Connect to Server', 1, (255, 180, 80))
        connection_label_rect = connection_label.get_rect()
        connection_label_rect.center = (int(WIDTH*.5), int(HEIGHT*.4))
        WINDOW.blit(connection_label, connection_label_rect)
        

        # Buttons n stuff ----------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: # event has no key attribute
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        

        username_button.draw()
        username_button.is_clicked(action=typing, args=(username_button, 20))

        ip_button.draw()
        ip_button.is_clicked(action=typing, args=(ip_button, 12))

        port_button.draw()
        port_button.is_clicked(action=typing, args=(port_button, 6))

        connect_button.draw()
        connect_button.is_clicked(action=connect_to_chat, args=(username_button.msg,
                                                                ip_button.msg,
                                                                port_button.msg))

        




    
                            
        ##menu_label = menu_font.render('Some Menu Title', False, (0,0,0))
        
        # Update window ------------------------------------------- #
        pygame.display.update()
        main_clock.tick(FPS)


def chat(client_socket):
    run = True
    while run:
        WINDOW.fill((25,25,25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: # event has no key attribute
                if event.key == pygame.K_ESCAPE:
                    run = False
                    client_socket.close()
                    
        pygame.display.update()
        main_clock.tick(FPS)

    
menu()
    
# Close Pygame ------------------------------------------------ #
pygame.quit()
sys.exit()
