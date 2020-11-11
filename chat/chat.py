import pygame
import sys
import os
import socket
import errno


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

    
    def render_font(self, align):
        self.label = self.font.render(self.msg, 1, (25,25,25))
        self.label_rect = self.label.get_rect()
        if not align:
            self.label_rect.center = ((self.x+(self.w//2)),
                                      (self.y+(self.h//2)))
        if align == 'left':
            self.label_rect.midleft = (self.x+20,
                                      (self.y+(self.h//2)))

        self.window.blit(self.label, self.label_rect)


    def draw(self, align=None):
        if self.check():
            pygame.draw.rect(self.window, self.ac, self.rect)
        else:
            pygame.draw.rect(self.window, self.ic, self.rect)

        self.render_font(align)
        

    def draw_clicked(self, align=None):
        pygame.draw.rect(self.window, self.ac,
                         (self.x, self.y, self.w, self.h))
        
        self.render_font(align)
    

    def is_clicked(self, action=None, args=None):
        if self.check():
            if args:
                action(*args)
            else:
                action()
            return True



def typing(button, align=None, limit=280):
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
            button.draw_clicked(align)
            pygame.display.update(button.rect)
            

def connect_to_chat(username, ip, port): #button.msg x 3
    print('Connecting...')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, int(port)))
        client_socket.setblocking(False) # .recv won't be blocking
        
        username_header = f'{len(username):<{HEADERSIZE}}'.encode('utf-8')
        client_socket.send(username_header + username.encode('utf-8'))
        print('Successfully Connected...')
        
    except:
        print('Connection failed!')
        return None

    chat(client_socket)


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
        username_button.draw()
        ip_button.draw()
        port_button.draw()
        connect_button.draw()

        # Events n stuff ------------------------------------------ #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: # event has no key attribute
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    username_button.is_clicked(action=typing, args=(username_button, None, 20))
                    ip_button.is_clicked(action=typing, args=(ip_button, None, 12))
                    port_button.is_clicked(action=typing, args=(port_button, None, 6))
                    connect_button.is_clicked(action=connect_to_chat, args=(username_button.msg,
                                                                            ip_button.msg,
                                                                            port_button.msg))

        ##menu_label = menu_font.render('Some Menu Title', False, (0,0,0))
        
        # Update window ------------------------------------------- #
        pygame.display.update()
        main_clock.tick(FPS)


def chat(client_socket):
    message_button = Button(WINDOW,
                            '>',
                            menu_font,
                            50,int(HEIGHT*.8),WIDTH-100,100,
                            (180,180,180),(240,240,240),
                            )
    
    run = True
    while run:
        WINDOW.fill((25,25,25))
        message_button.draw('left')
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: # event has no key attribute
                if event.key == pygame.K_ESCAPE:
                    run = False
                    client_socket.close()

            # Type and send message            
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:                        
                    message = message_button.is_clicked(action=typing,
                                                        args=(message_button, 'left'))

                    ''' send things to server'''
                    if message:
                        message = message_button.msg.encode('utf-8')
                        message_header = f'{len(message):<{HEADERSIZE}}'.encode('utf-8')
                        client_socket.send(message_header + message)
                        message_button.msg = '>'

        if run:            
            try:
                ''' receive things from server '''
                # server sends to user
                sender_header = client_socket.recv(HEADERSIZE)
                if not sender_header: #when?
                    print('Connection closed by the server')
                    sys.exit()
                    
                sender_length = int(sender_header.decode('utf-8').strip())
                sender = client_socket.recv(sender_length).decode('utf-8')

                message_header = client_socket.recv(HEADERSIZE)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')

                print(f'{sender} > {message}')

                    
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    # above errors: when there are no more messages to receive
                    # if not one of these:
                    print('Reading Error', str(e))
                    sys.exit()

                    
            except Exception as e:
                print('General Error', str(e))
                sys.exit()

        
        main_clock.tick(FPS)

    
menu()
    
# Close Pygame ------------------------------------------------ #
pygame.quit()
sys.exit()
