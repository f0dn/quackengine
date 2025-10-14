class engine: 
    def __init__(self):
        pass

    def start():
        pass

    def handle_input(self, command: str):
        if(command == "uci"):
            print("id name quackengine")
            print("id author project quack")
            #engine need to tell the GUI which parameters can be changed in the engine, example below:
            print("option name Hash type spin default 1 min 1 max 128")
            print("option name NalimovPath type string default <empty>")
            print("option name NalimovCache type spin default 1 min 1 max 32")
            print("option name Nullmove type check default true")
            print("option name Style type combo default Normal var Solid var Normal var Risky")
            print("uciok")
            #if this is a copyprotected engine, need to tell GUI 'copyprotection checking' and actually check copyright after uciok
            #engine can send registration checking after the uciok command followed by either registration ok or registration error
            #registration needed for engines that need a username and/or a code to function with all features
        elif(command == "isready"):
            print("readyok")
        elif("setoption" in command):
            pass
        elif("ucinewgame"):
            pass
        elif("register" in command):
            pass
        elif("debug" in command):
            pass
        elif("position" in command):
            pass
        elif("go" in command):
            #engine needs to send info about the position
            pass
        elif(command == "stop"):
            self.calculate_best_move()
            pass
        elif(command == "ponderhit"):
            pass
        elif(command == "quit"):
            pass

    def calculate_best_move():
        pass

