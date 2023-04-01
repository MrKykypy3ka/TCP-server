from socket_server import start
from time import *

def main():
    while True:
        print(strftime("%H:%M", localtime()))
        sleep(60)


if __name__ == "__main__":
    main()
