import os
import time 
import socket

def send_file(file_path, host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    file_name = os.path.basename(file_path)
    client_socket.send(file_name.encode())

    time.sleep(1) 

    with open(file_path, 'rb') as f:
        while (chunk := f.read(1024)):
            client_socket.sendall(chunk)

    client_socket.shutdown(socket.SHUT_WR)

    compressed_file_name = file_name.split('.')[0] + '.zip'

    with open(f'output/{compressed_file_name}', 'wb') as f:
        while True:
            bytes_read = client_socket.recv(1024)

            if not bytes_read:
                break

            f.write(bytes_read)

    client_socket.close()

    print(f"Compressed file received and saved as {compressed_file_name}")

if __name__ == "__main__":
    file_path = 'sample_folder/text_example.txt' 
    send_file(file_path)

    file_path = 'sample_folder/csv_example.csv'
    send_file(file_path)

