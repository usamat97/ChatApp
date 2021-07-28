from socket import *
import threading

# Global variable that mantain client's connections
connections = []
# user = {'address':'', 'name':''}
SERVER_PORT = 8000
SERVER_NAME = gethostname()
SERVER_ADDRESS = gethostbyname(SERVER_NAME)

def handle_user_connection(connectionSocket: socket, address: str, user: dict) -> None:
    '''
        Get user connection in order to keep receiving their messages and
        sent to others users/connections.
    '''
    first_msg = True
    while True:
        try:
            # Get client message
            msg = connectionSocket.recv(1024)
            print(f'user: {user}')
            # If no message is received, there is a chance that connection has ended
            # so in this case, we need to close connection and remove it from connections list.
            if msg:

                if first_msg:
                    user['name'] = msg.decode()

                # Log message sent by user
                print(f'[{user["name"]}] {address[0]}:{address[1]} - {msg.decode()}')
                # Build message format and broadcast to users connected on server
                msg_to_send = f'\t\t\t\t[{user["name"]}] - {msg.decode()}'
                if not first_msg:
                    broadcast(msg_to_send, connectionSocket)
                first_msg = False

            # Close connection if no message was sent
            else:
                remove_connection(connectionSocket)
                break

        except Exception as e:
            print(f'Error to handle user connection: {e}')
            remove_connection(connectionSocket)
            break

def broadcast(message: str, connectionSocket: socket) -> None:
    '''
        Broadcast message to all users connected to the server
    '''

    # Iterate on connections in order to send message to all client's connected
    for client_conn in connections:
        # Check if isn't the connection of who's send
        if client_conn != connectionSocket:
            try:
                # Sending message to client connection
                client_conn.send(message.encode())

            # if it fails, there is a chance of socket has died
            except Exception as e:
                print('Error broadcasting message: {e}')
                remove_connection(client_conn)

def remove_connection(connectionSocket: socket) -> None:
    '''
        Remove specified connection from connections list
    '''

    # Check if connection exists on connections list
    if connectionSocket in connections:
        # Close socket connection and remove connection from connections list
        connectionSocket.close()
        connections.remove(connectionSocket)

def server() -> None:
    '''
        Main process that receive client's connections and start a new thread
        to handle their messages
    '''

    try:
        # Create server and specifying that it can only handle 4 connections by time!
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(('',SERVER_PORT))
        serverSocket.listen(4)

        print(f'The server "{SERVER_NAME}" is ready to receive.')
        
        while True:

            # Accept client connection
            connectionSocket, address = serverSocket.accept()
            # Add client connection to connections list
            connections.append(connectionSocket)
            user = {'address':address, 'name':''}
            # Start a new thread to handle client connection and receive it's messages
            # in order to send to others connections
            threading.Thread(target=handle_user_connection, args=[connectionSocket, address, user]).start()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        # In case of any problem we clean all connections and close the server connection
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn)

        serverSocket.close()


if __name__ == "__main__":
    server()