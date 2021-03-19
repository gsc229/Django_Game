import socket
from _thread import *
import sys

server = "192.168.1.5"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# this binds our server and port to the socket
try:
  s.bind((server, port))
except socket.error as e:
  str(e)

# if no argumen allows unlimited connections, but this allows 2 people to connect
s.listen(2)

print("Server Started, Waiting for a connection...")


def read_pos(str):
  str = str.split(",")
  return int(str[0]), int(str[1])


def make_pos(tup):
  return str(tup[0]) + "," + str(tup[1])

pos = [(0, 0), (100, 100)]


# A threaded function. Threading works by allowing multiple processess to work at once
# When the threaded_client function is called in the lower while loop, 
# under normal circumstances (without threading) we would have to wait until the threaded_client function returned
# before the next loop. However you can see in the while loop that threaded_client is called in start_new_thread
# which starts a new process (a 'thread') and allows the while loop to keep iterating.
def threaded_client(conn, player):
  # sending something when the client first connects in order to for them to know connection was made
  conn.send(str.encode(make_pos(pos[player])))

  reply = ""

  
  while True:
    try:
      #2048 is the amount of bits we are trying to receive, not a lot so it sending/recieing happnes almost instantly, but increasing
      #the amount of info. could make it take considerabley longer  
      data = read_pos(conn.recv(2048).decode()) 

      pos[player] = data

      if not data:
        print("Disconnected")
        break
      else:
        if player == 1:
          reply = pos[0]
        if player == 0:
          reply = pos[1]
        print("Received: ", data)
        print("Sending: ", reply)

      conn.sendall(str.encode(make_pos(reply)))
    except:
      break
  print("Lost Connection")
  conn.close()


currentPlayer = 0
# this while loop continuously looks for connections
while True:
  conn, addr = s.accept()
  print(currentPlayer)
  print("Connected to: ", addr)

  start_new_thread(threaded_client, (conn, currentPlayer))
  currentPlayer += 1