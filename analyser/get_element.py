# 50.268368, 127.536263
# 56.657713, 124.711333

from API import yandex
import os

def main():
    yandex.get_map(127.536263, 50.268368,  "map", 4, 0.000001, 0.000001)


if __name__ == "__main__":
    os.chdir(r'C:\Users\olegm\Documents\GitHub\road')
    main()
