import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 51918)
print ('connecting to %s port %s' % server_address)
sock.connect(server_address)




try:

    # Send data
    message = 'hi'

    print ('sending "%s"' % message)
    sock.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(30).decode()
        amount_received += len(data)
        print ('received "%s"' % data)

finally:
    print ('closing socket')
    sock.close()
