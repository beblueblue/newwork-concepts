import sys
import socket
import ssl

def get_https_response(host, port):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap the socket with SSL
    context = ssl.create_default_context()
    ssl_sock = context.wrap_socket(client_socket, server_hostname=host)

    response = b""

    try:
        # Connect to the server
        ssl_sock.connect((host, port))

        # Prepare the HTTP GET request
        request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        ssl_sock.sendall(request.encode())

        # Receive the response
        while True:
            data = ssl_sock.recv(4096)
            if not data:
                break
            response += data

    except ssl.SSLError as e:
        print(f"SSL error: {e}")
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        # Close the connection
        ssl_sock.close()

    return response.decode()

def main():
    # Check the number of command line arguments
    if len(sys.argv) < 2:
        print("Usage: python webclient.py <hostname> [port]")
        sys.exit(1)

    # Get the host and port from command line arguments
    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 443

    # Get the HTTP response from the server
    response = get_https_response(host, port)

    # Print the response
    print(response)

if __name__ == "__main__":
    main()
