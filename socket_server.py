from dotenv import load_dotenv, find_dotenv
import socket
import pickle
import os
import threading

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
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

def handle_client(conn, addr):
    try:
        request = conn.recv(1024).decode()
        if request == "G_L":
            send_file_list(conn)
        elif request == "S_F":
            conn.sendall("OK".encode())
            filename = conn.recv(1024).decode()
            get_file(conn, filename)
        elif 'R_F' in request:
            filename = request.split()[1]
            send_file(conn, filename)
        else:
            print("Неизвестный запрос.")
    except socket.error as error:
        print(f"Ошибка при обработке запроса от клиента {addr}: {error}")
    finally:
        conn.close()

def get_file(conn, filename):
    with open(f'data/input/{filename}', 'wb') as f:
        while True:
            file_data = conn.recv(1024)
            if not file_data:
                break
            f.write(file_data)

def send_file_list(conn):
    file_list = [file for file in os.listdir('data/results') if os.path.splitext(file)[1] in ['.docx', '.csv']]
    try:
        file_list_data = pickle.dumps(file_list)
        conn.sendall(file_list_data)
        print("Список файлов успешно отправлен.")
    except socket.error as error:
        print(f"Ошибка при отправке списка файлов: {error}")

def send_file(conn, filename):
    with open(f'data/results/{filename}', 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            conn.sendall(data)
    print(f"Файл '{filename}' отправлен.")
