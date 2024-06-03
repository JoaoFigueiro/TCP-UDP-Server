import socket
import os

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 512

def send_file(file_name, server_address=(UDP_IP, UDP_PORT)):
    with open(file_name, 'rb') as f:
        file_data = f.read()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Enviar arquivo para o servidor
    sock.sendto(file_data, server_address)

    # Receber arquivo compactado do servidor
    received_data = bytearray()
    while True:
        chunk, addr = sock.recvfrom(BUFFER_SIZE)
        received_data.extend(chunk)

        # Enviar confirmação de recebimento (ACK)
        sock.sendto(b"ACK", addr)
        
        if len(chunk) < BUFFER_SIZE:
            break
    
    # Salvar o arquivo compactado na pasta 'output'
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    file_name = os.path.basename(file_path)
    compressed_file_name = 'udp_' + file_name.split('.')[0] + '.zip'


    compressed_file_path = os.path.join(output_dir, compressed_file_name)
    with open(compressed_file_path, 'wb') as f:
        f.write(received_data)

    print(f"Arquivo compactado recebido e salvo como '{compressed_file_path}'")

if __name__ == "__main__":
    file_path = 'sample_folder/text_example.txt' 
    send_file(file_path)

    # file_path = 'sample_folder/csv_example.csv'
    # send_file(file_path)
