from move import Move

def main():
    moves = []

    while True:
        user_input = input("Enter a move (or 'quit' to exit): ")

        if user_input.lower() == "quit":
            break
        try:
            move = Move(user_input)
            moves.append(move.to_long_algebraic())
            print(f"Move accepted: {move.to_long_algebraic()}")
            print(f"Source coords: {move.src_coords}, Target coords: {move.target_coords}")
        except Exception as e:
            print(f"Invalid move: {e}")

    move_history = tuple(moves)
    print(move_history)


if __name__ == "__main__":
    main()
