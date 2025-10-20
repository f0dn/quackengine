from move import Move
import os

if __name__ == "__main__":
    while True:
        user_input = input("Enter a valid PGN file path (or 'q' to exit): ")
        if user_input.lower() == "q":
            break
        if not os.path.isfile(user_input):
            print("File does not exist. Please enter a valid PGN path.")
            continue

        converter = Move(user_input)
        lan_moves = converter.extract_lan()
        json_file = converter.save_to_json()
        print(lan_moves)
        print(f"Moves saved to {json_file}")
