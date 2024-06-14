import sys
import socket

def get_http_response(host, port):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get the IP address of the host
    ip_address = socket.gethostbyname(host)

    # Connect to the server on the specified port
    client_socket.connect((ip_address, port))

    # Prepare the HTTP GET request
    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    
    # Send the request
    client_socket.sendall(request.encode())

    # Receive the response
    response = b""
    while True:
        data = client_socket.recv(4096)
        if len(data) == 0:
            break
        response += data

    # Close the connection
    client_socket.close()

    return response.decode()

def main():
    # Check the number of command line arguments
    if len(sys.argv) < 2:
        print("Usage: python webclient.py <hostname> [port]")
        sys.exit(1)

    # Get the host and port from command line arguments
    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 80

    # Get the HTTP response from the server
    response = get_http_response(host, port)

    # Print the response
    print(response)

if __name__ == "__main__":
    main()
