from socket import *

serverName = 'localhost'
serverPort = 80
# sentence = input('Input lowercase sentence: ')

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    msg = input()

    if msg == 'quit':
        break

    # Parse message to utf-8
    clientSocket.send(msg.encode())
    try:
        msg = clientSocket.recv(1024)

        # If there is no message, there is a chance that connection has closed
        # so the connection will be closed and an error will be displayed.
        # If not, it will try to decode message in order to show to user.
        if msg:
            print(msg.decode())
        else:
            clientSocket.close()
            break

    except Exception as e:
        print(f'Error handling message from server: {e}')
        clientSocket.close()
        break
# Close connection with the server
clientSocket.close()

# sentence = str.encode(sentence)
# print(sentence)
# clientSocket.send(sentence)
# modifiedSentence = clientSocket.recv(1024)
# print('From Server "{}": {}'.format(serverName, modifiedSentence))
# clientSocket.close()