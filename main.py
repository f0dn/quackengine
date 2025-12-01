from engine import Engine

def main():
    with Engine("database") as engine:
        engine.start()

if __name__ == "__main__":
    main()
