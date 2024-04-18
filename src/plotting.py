import os

PATH = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
DATA_DIR = os.path.join(PATH, "data")


def main():
    print(DATA_DIR)


if __name__ == '__main__':
    main()
