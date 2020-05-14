import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to the port
server_address = ('192.168.1.131', 52024)
print (sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)



# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print ('waiting for a connection')
    connection, client_address = sock.accept()


    try:
            print ('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(30).decode()
                print ('received "%s"' % data)
                if data:
                    print (data)
                 #   connection.sendall(data.encode())
                #else:
                 #   print ('no more data from', client_address)


    finally:
        # Clean up the connection
        connection.close()
