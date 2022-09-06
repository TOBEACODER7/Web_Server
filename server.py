from operator import truediv
import socket
import threading

port = 8989

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('101.201.155.42', port))
socket.listen(port)


while True:
  try:
    client, address = socket.accept()
    print('Connected to', address)
    threading.Thread(target=client.recv(1024).decode()).start()
  except KeyboardInterrupt:
    print('Server closed')
    break

