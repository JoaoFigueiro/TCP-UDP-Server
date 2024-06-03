import socket
import os
import zipfile
import random
import select

# Configurações do servidor
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 512
PACKET_LOSS_RATE = 0.5  # Taxa de perda de pacotes (10%)

def compress_file(file_path):
    """
    Comprime o arquivo especificado no formato zip e retorna o caminho do arquivo zipado.
    
    Args:
        file_path (str): Caminho do arquivo a ser comprimido.
    
    Returns:
        str: Caminho do arquivo zipado.
    """
    zip_path = file_path + '.zip'
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(file_path, os.path.basename(file_path))
    return zip_path

def receive_file(sock):
    """
    Recebe um arquivo em partes pelo socket especificado e retorna os dados recebidos e o endereço do remetente.
    
    Args:
        sock (socket.socket): O socket UDP para receber os dados.
    
    Returns:
        bytearray: Dados recebidos.
        tuple: Endereço do remetente.
    """
    received_data = bytearray()
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        received_data.extend(data)
        if len(data) < BUFFER_SIZE:
            return received_data, addr

def send_compressed_file(sock, addr, file_path, simulate_packet_loss):
    """
    Envia o arquivo comprimido para o cliente em partes e aguarda confirmações (ACKs).
    
    Args:
        sock (socket.socket): O socket UDP para enviar os dados.
        addr (tuple): Endereço do cliente.
        file_path (str): Caminho do arquivo a ser comprimido e enviado.
        simulate_packet_loss (bool): Se True, simula perda de pacotes.
    """
    zip_path = compress_file(file_path)
    
    with open(zip_path, 'rb') as f:
        compressed_data = f.read()

    for i in range(0, len(compressed_data), BUFFER_SIZE):
        chunk = compressed_data[i:i + BUFFER_SIZE]
        while True:
            if simulate_packet_loss and random.random() <= PACKET_LOSS_RATE:
                print(f"Pacote {i // BUFFER_SIZE + 1} perdido intencionalmente para simulação.")
            else:
                sock.sendto(chunk, addr)
                print(f"Enviando pacote {i // BUFFER_SIZE + 1}")
            
            sock.settimeout(1.0)
            try:
                ack, _ = sock.recvfrom(BUFFER_SIZE)
                if ack.decode() == "ACK":
                    print(f"ACK recebido para o pacote {i // BUFFER_SIZE + 1}")
                    break
            except socket.timeout:
                print(f"Timeout esperando ACK para o pacote {i // BUFFER_SIZE + 1}. Reenviando...")

    os.remove(zip_path)

def start_udp_server(simulate_packet_loss=False):
    """
    Inicia o servidor UDP que recebe arquivos, os comprime e os envia de volta ao cliente.
    
    Args:
        simulate_packet_loss (bool): Se True, simula perda de pacotes.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    print(f"Servidor UDP ouvindo em {UDP_IP}:{UDP_PORT}")

    try:
        while True:
            ready = select.select([sock], [], [], 1.0)
            if ready[0]:
                received_data, addr = receive_file(sock)
                
                received_file_path = "received_file"
                with open(received_file_path, 'wb') as f:
                    f.write(received_data)

                send_compressed_file(sock, addr, received_file_path, simulate_packet_loss)
                print(f"Arquivo compactado enviado de volta para {addr}")
                
                os.remove(received_file_path)
    except KeyboardInterrupt:
        print("\nServidor interrompido pelo usuário.")
    finally:
        sock.close()
        print("Socket fechado. Servidor encerrado.")

if __name__ == "__main__":
    # Iniciar o servidor UDP com simulação de perda de pacotes ativada
    start_udp_server(simulate_packet_loss=True)
