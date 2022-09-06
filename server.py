from operator import truediv
import socket
import threading

port = 8989

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## the code below is for the server to listen to the client
## written by github copilot
address = ('0.0.0.0', port)
socket.bind(address)
socket.listen(port)


def SendToClient(client):
  print(client.recv(1024).decode())
  
  filename = "index.html"
  filedata = open(filename, "rb").read()
  message = b"HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n"
  message += b"Content-Length: " + str(len(filedata)).encode() + b"\r\n\r\n"
  message += filedata
  client.send(message)
  client.close()
  

while True:
  try:
    client, address = socket.accept()
    print('Connected to', address)
    ## there connect has been set up
    SendToClient(client)


  except KeyboardInterrupt:
    print('Server closed')
    break


