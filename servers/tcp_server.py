import os
import socket
import zipfile


def compress_file(file_path):
    zip_path = file_path + '.zip'

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(file_path, os.path.basename(file_path))

    return zip_path


def start_server(host='localhost', port=12345):
    protocol = 'tcp'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        print("Dentro do while")
        client_socket, addr = server_socket.accept()

        print(f"Connection from {addr}")

        file_name = client_socket.recv(1024).decode()
        with open(file_name, 'wb') as f:
            while True:
                bytes_read = client_socket.recv(1024)

                if not bytes_read:
                    break

                f.write(bytes_read)

        compressed_file = compress_file(file_name)

        with open(compressed_file, 'rb') as f:
            while (chunk := f.read(1024)):
                client_socket.sendall(chunk)

        client_socket.close()
        os.remove(file_name)
        os.remove(compressed_file)

        print(f"File {file_name} recieved, compressing and sending back to the client.")


if __name__ == "__main__":
    start_server()