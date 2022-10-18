import socket
from _thread import *
import pickle
from game import Game

host = "192.168.1.115"
port = 7777

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: 
    sock.bind((host, port))

except socket.error as e:
    str(e)

sock.listen()
print("Server is listening on:" + str(host) + ':' + str(port))

connected = set()
games = {}
idCount = 0

def threaded_client(ws, player, gameId):
    global idCount 
    ws.send(str.encode(str(player)))

    while True:
        try:
            request = ws.recv(5000).decode()

            if gameId in games:
                game = games[gameId]
                
                if not request:
                    break
                else:
                    if request == "reset":
                        game.reset()
                    elif len(request) == 1:
                        game.set_letter(request)
                    elif request != "get":
                        game.set_word(request)

                    ws.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection. Closing game: ", gameId)
    try:
        del games[gameId]
    except:
        pass
    idCount -= 1 
    ws.close()

while True:
    ws, addr = sock.accept()
    print("Connected to:", addr)

    idCount += 1
    player = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game with id: ", gameId)
    else:
        games[gameId].ready = True
        player = 1


    start_new_thread(threaded_client, (ws, player, gameId))
