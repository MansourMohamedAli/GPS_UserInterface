import socket
import subprocess
from logger import logger

# Define the server address and port

# SERVER_HOST = '0.0.0.0'
SERVER_HOST_NAME = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(SERVER_HOST_NAME)
SERVER_PORT = 9999

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse the socket address
server_socket.bind((IP_ADDRESS, SERVER_PORT))
server_socket.listen(5)
print(f"Listening on {IP_ADDRESS}:{SERVER_PORT}...")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        try:
            # Receive the command from the client
            command = client_socket.recv(1024).decode()

            if command.lower() == 'exit':
                print("Exiting...")
                break            

            if command:
                print(f"Received command: {command}")

                # Execute the command
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                    output = output.decode().replace('\r\n', '\n')
                    logger.info(f'SUCCESS:{output}')
                    continue
                except subprocess.CalledProcessError as e:
                    output = e.output.decode().replace('\r\n', '\n')
                    logger.info(f'EXCEPTION:{output}')

                # Send the output back to the client
                client_socket.send(output.encode())
                print(f"Sent output to client: {client_address}")
                
        except socket.error as e:
            print(f"Socket error: {e}")

        finally:
            client_socket.close()
            print(f"Closed connection with {client_address}")

finally:
    server_socket.close()
    print("Server shut down.")
