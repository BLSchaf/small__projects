import socket
import select
import time


HEADERSIZE = 10
IP = socket.gethostname()
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# To reuse the address, set Socket Option Level > Socket Option Reuseaddr = 1(True)
#server_socket,setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

# clients and server
socket_list = [server_socket]
# to easily address a client without writing the (IP, PORT) out everytime
clients = {}


def receive_message(s):
    '''
        first receives the header, then the rest of the message from client
        return it as dict
    '''
    try:
        message_header = s.recv(HEADERSIZE)
        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': s.recv(message_length)}
        
    except:
        return False


while True:
    # select.select(read_list, write_list, error_list)
    # could also just loop through list?
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

    for current_socket in read_sockets:
        if current_socket == server_socket:
            ''' Everything that happens on the Server '''
            # For Server Socket accept new clients - client address = (Port, ID)
            client_socket, client_address = server_socket.accept()
            # And receive first message from client which will be the a dict of {header, data}
            user = receive_message(client_socket) # this is a dict
            if not user:
                # no initial message sent or exception error
                continue

            socket_list.append(client_socket)
            # append client to clients dict
            clients[client_socket] = user #cs{user{header, data}}

            print(time.asctime(),
                  f'Accepted new connection from {client_address[0]}:{client_address[1]} \nUsername: {user["data"].decode("utf-8")}',
                  sep='\n')
            #print(socket_list)
            #print(clients)

        else:
            ''' Everything that happens for clients '''
            # current client (socket in list) receives from itself ???
            message = receive_message(current_socket) # this is a dict

            if not message:
                print(time.asctime(),
                      f'Closed connection from {clients[current_socket]["data"].decode("utf-8")}',
                      sep='\n')
                socket_list.remove(current_socket)
                del clients[current_socket]
                continue

            if not message["data"]:
                continue

            else:
                user = clients[current_socket] 
                print(time.asctime(),
                      f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}',
                      sep='\n')

            for client_socket in clients:
                if client_socket != current_socket:
                    # Send message to all other sockets
                    client_socket.send(user['header'] + user['data'] + message['header'] + message ['data'])
                    
              
    for current_socket in exception_sockets:
        socket_list.remove(current_socket)
        del clients[notified_socket]
