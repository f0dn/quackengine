from move import Move
def main():
    print("Hello World")
    while True:

        user_input = input("Enter a valid move (or 'q' to exit): ")
        if user_input.lower()=='q':
            break
        try:
            converter=Move(user_input)
            print(converter.san_notation())
            continue
        except Exception as e:
            print("Invalid Move " + str(e))
        
    

if __name__ == "__main__":
    main()
    
        
       