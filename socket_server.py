import socket

HOST = '192.168.50.69'  # Локальный IP-адрес
PORT = 7000         # Порт

# Создаем сокет
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print(f'Сервер запущен на порту {PORT}...')

    # Бесконечный цикл ожидания клиентских подключений
    while True:
        conn, addr = s.accept()
        with conn:
            print(f'Подключение клиента: {addr}')
            # Принимаем данные
            file_data = conn.recv(1024)
            # Сохраняем файл на диск
            with open('data/input/data.json', 'wb') as f:
                while file_data:
                    f.write(file_data)
                    file_data = conn.recv(1024)
            print('Файл успешно получен.')