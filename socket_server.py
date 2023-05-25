from dotenv import load_dotenv, find_dotenv
import socket
import os

load_dotenv(find_dotenv())
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Сервер запущен!')
        while True:
            conn, addr = s.accept()
            with conn:
                file_data = conn.recv(1024)
                number = len(os.listdir('data/input'))
                with open(f'data/input/data{number + 1}.json', 'wb') as f:
                    while file_data:
                        f.write(file_data)
                        file_data = conn.recv(1024)
