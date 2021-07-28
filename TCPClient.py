from socket import *
import threading

def handle_messages(clientSocket: socket):
    '''
        Receive messages sent by the server and display them to user
    '''
    while True:
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

def client() -> None:
    '''
        Main process that start client connection to the server 
        and handle it's input messages
    '''
    SERVER_PORT = 8000
    SERVER_ADDRESS = gethostbyname(gethostname())

    try:
        # Instantiate socket and start connection with server
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((SERVER_ADDRESS, SERVER_PORT))
        # Create a thread in order to handle messages sent by server
        threading.Thread(target=handle_messages, args=[clientSocket]).start()

        print('Connected to chat!')
        set_username = input('enter your name: ')
        clientSocket.send(set_username.encode())

        # Read user's input until it quit from chat and close connection
        while True:
            msg = input()

            if msg == 'quit':
                break

            # Parse message to utf-8
            clientSocket.send(msg.encode())

        # Close connection with the server
        clientSocket.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        clientSocket.close()

if __name__ == "__main__":
    client()