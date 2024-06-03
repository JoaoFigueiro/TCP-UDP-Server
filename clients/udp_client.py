import socket
import os

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024

def send_file(file_name, server_address=(UDP_IP, UDP_PORT)):
    with open(file_name, 'rb') as f:
        file_data = f.read()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Enviar arquivo para o servidor
    sock.sendto(file_data, server_address)

    # Receber arquivo compactado do servidor
    compressed_data, _ = sock.recvfrom(BUFFER_SIZE)
    
    # Salvar o arquivo compactado na pasta 'output'
    output_dir = '../output'
    os.makedirs(output_dir, exist_ok=True)
    compressed_file_path = os.path.join(output_dir, "received_compressed_file_from_UDP.zip")
    
    with open(compressed_file_path, 'wb') as f:
        f.write(compressed_data)

    print(f"Arquivo compactado recebido e salvo como '{compressed_file_path}'")

if __name__ == "__main__":
    file_path = '../sample_folder/text_example.txt' 
    send_file(file_path)

    file_path = '../sample_folder/csv_example.csv'
    send_file(file_path)
