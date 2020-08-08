import socket
import pickle
from _thread import *
from game import Game


''' pickle to not just transfer encoded strings but objects '''

SERVER = ''
PORT = 9999
MAX_CLIENTS = 2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER, PORT))

except socket.error as e:
    print(str(e))

s.listen(MAX_CLIENTS)
print('Waiting for connection - Server started')

# create new game when alrdy 2 in previous
games = {} # store games
id_count = 0 # keep track of id count
connected = set() # store ip of connected clients


def threaded_client(connection, player, game_id):
    global id_count #global so that it is changed outside of this function on the server
    status_timer = 200
    
    connection.send(str.encode(str(player))) # will be called by Network().connect() once and enter loop
    reply = ''

    while True:
        status_timer -= 1
        if status_timer == 0:
            status_timer = 200
            print('Number of games running:', len(games))
            
        try:
            data = connection.recv(4096*4).decode()

            if game_id in games: #check if game still exists
                game = games[game_id]
                if not data:
                    print('Error: No data')
                    break
                else: # what is send - update game accordingly (in here, server side)
                    if data == 'reset':
                        game.reset()
                    elif data != 'get': # 'R','P','S'
                        game.play(player, data)

                    reply = game # in any case, reply game state
                    connection.sendall(pickle.dumps(reply)) # send game state to client
            else:
                print('Error: No game')
                break
            
        except Exception as e:
            print(e)
            break
        
    print('Lost Connection')
    
    try:
        del games[game_id]
        print('Closing game',  game_id)
        
    except Exception as e:
        print(e)
        pass

    id_count -= 1
    connection.close

        
while True:
    connection, address = s.accept() #wait for connection (var connection is a socket object)
    id_count += 1 # client id
    print('Connected to client', id_count)
    
    player = 0 # default player 0
    game_id = (id_count-1) // 2 # two ids for one game_id
    

    if id_count % 2 == 1: # new game for player1 - first player has to have id = 1
        games[game_id] = Game(game_id)
        print('Creating a new game..')
        
    else: # game rdy for second player and game rdy when second joined
        games[game_id].game_rdy = True
        player = 1
        
    

    start_new_thread(threaded_client, (connection, player, game_id))
    
