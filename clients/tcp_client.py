import os
import socket


def send_file(file_path, host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    file_name = os.path.basename(file_path)
    client_socket.send(file_name.encode())

    with open(file_path, 'rb') as f:
        while (chunk := f.read(1024)):
            client_socket.sendall(chunk)

    compressed_file_name = file_name + '.zip'

    with open(compressed_file_name, 'wb') as f:
        while True:
            bytes_read = client_socket.recv(1024)

            if not bytes_read:
                break

            f.write(bytes_read)

    client_socket.close()

    print(f"Compressed file recieved and saved as {compressed_file_name}")


if __name__ == '__main__': 
    path = '~/unziped_folder'   
    send_file(path)