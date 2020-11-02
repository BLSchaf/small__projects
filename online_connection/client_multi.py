import socket
import select
import errno # to match specific error codes
import sys

'''
- on connection clients tells server its username
- loop while to receive and send messages
'''

HEADERSIZE = 10
IP = socket.gethostname()
PORT = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False) # .recv won't be blocking

username = input("Username: ")
username_header = f'{len(username):<{HEADERSIZE}}'.encode('utf-8')
client_socket.send(username_header + username.encode('utf-8'))


while True:
    ''' send and receive messages '''
    message = input(f'{username} > ')
    
    #if message:
    ''' send things to server'''
    message = message.encode('utf-8')
    message_header = f'{len(message):<{HEADERSIZE}}'.encode('utf-8')
    client_socket.send(message_header + message)

    try:
        ''' receive things from server '''
        # server sends to user
        username_header = client_socket.recv(HEADERSIZE)
        if not username_header:
            print('Connection closed by the server')
            sys.exit()
            
        username_length = int(username_header.decode('utf-8').strip())
        sender = client_socket.recv(username_length).decode('utf-8')

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
