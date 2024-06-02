import os
import path 
import zipfile

from clients import tcp_client, udp_client
from servers import tcp_server, udp_server


def main(): 
    csv_zip = zipfile.ZipFile(f'output/csv_example.zip', mode='w')
    csv_zip.write('sample_folder/csv_example.csv', 'csv_example.csv')

    txt_zip = zipfile.ZipFile('output/text_example.zip', mode='w')
    txt_zip.write('sample_folder/text_example.txt', 'text_example.txt')

if __name__ == '__main__':
    main()