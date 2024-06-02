import os
import path 

from clients import tcp_client, udp_client
from servers import tcp_server, udp_server


def main(): 
    tcp_server.start_server()


if __name__ == '__main__':
    main()