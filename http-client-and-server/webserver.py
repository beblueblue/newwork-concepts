import sys
import socket

# Default port
DEFAULT_PORT = 28333

def start_server(port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow the address to be reused
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to the port
    server_socket.bind(('0.0.0.0', port))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print(f"\nConnection from {client_address}")

        # Receive the request
        request = client_socket.recv(1024).decode()
        print(f"\nRequest: {request}")

        # Check if the request is for favicon.ico
        if 'GET /favicon.ico' in request:
          print("\nGET /favicon.ico")
          response = (
              "HTTP/1.1 404 Not Found\r\n"
              "Content-Type: text/plain\r\n"
              "Content-Length: 9\r\n"
              "Connection: close\r\n"
              "\r\n"
              "Not Found"
          )
        else:
          print("\nPrepare the response")
          # Prepare the response
          response = (
              "HTTP/1.1 200 OK\r\n"
              "Content-Type: text/plain\r\n"
              "Content-Length: 13\r\n"
              "Connection: close\r\n"
              "\r\n"
              "Hello, world!"
          )

        # Send the response
        client_socket.sendall(response.encode())

        # Close the connection
        client_socket.close()

def main():
    # Get the port from command line arguments
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT

    try:
        start_server(port)
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
