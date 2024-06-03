import socket
import os
import zipfile

# Configurações do servidor
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024

def compress_file(file_path):
    zip_path = file_path + '.zip'

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(file_path, os.path.basename(file_path))

    return zip_path

# Criar socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Servidor UDP ouvindo em {UDP_IP}:{UDP_PORT}")

received_data = bytearray()

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    
    if data:
        received_data.extend(data)

        if len(data) < BUFFER_SIZE:
            received_file_path = "received_file"
            with open(received_file_path, 'wb') as f:
                f.write(received_data)
            
            zip_path = compress_file(received_file_path)
            
            with open(zip_path, 'rb') as f:
                compressed_data = f.read()
            
            sock.sendto(compressed_data, addr)
            print(f"Arquivo compactado enviado de volta para {addr}")
            
            received_data = bytearray()

            os.remove(received_file_path)
            os.remove(zip_path)
