"""
Gra:
    Hexapawn[https://pl.wikipedia.org/wiki/Hexapawn]
    Mozliwość zagrania[https://www.mrozilla.cz/lab/hexapawn]

Autorzy:
    Damian Kijańczuk s20154
    Szymon Ciemny    s21355

Skrócone zasady:
    Gracze dysponują pionkami ustawionymi po przeciwległych stronach. Ruchy są wykonywane na przemian w linii pionowej,
    natomiast zbijanie pionków odbywa się po linii ukośnej. Wygrywa ten, kto doprowadzi swój pionek na linię startu przeciwnika,
    zbije wszystkie pionki przeciwnika lub gdy przeciwnik nie będzie w stanie wykonać ruchu.

Przygotowanie środowiska:
    Oprócz języka Python, potrzebna takze będzie biblioteka easyAI[https://zulko.github.io/easyAI/installation.html]

Uruchomienie oraz instrukcja:
    By uruchomić wpisujemy przykładowo
    'python3 hexapawn.py --player1 AI --player2 AI' albo
    'python3 hexapawn.py --player1 Human --player2 AI'

    By wyśwetlić mozliwe ruchy nalezy wpisać
    'show moves'


"""


from easyAI import TwoPlayerGame, AI_Player, Human_Player, Negamax, DUAL, SSS
import sys
import argparse

class Hexapawn(TwoPlayerGame):
    def __init__(self, players, size=(3, 3)):
        """
        Initialization of a game and all parameters

        Parameters:
        players ([easyAI.Player.AI_Player, easyAI.Player.AI_Player]):
            2 element list with players, can be Human (Human_Player())
            or AI AI_Player(ai) with chosen artifical inteligence

        size ((int,int)):
            list of ints defining the size of checkerboard, minimum sensible
            gaming area is 3x3(default value)

        """

        # Height and width of playarea
        HEIGHT, WIDTH = size
        self.size = HEIGHT, WIDTH

        # Giving each player direction its pawns will be going, line
        # which must reach in order to win and pawns with their postions
        players[0].direction = 1
        players[0].goal_line = HEIGHT-1
        players[0].pawns = [(0, j) for j in range(WIDTH)] 
        players[1].direction = -1
        players[1].goal_line = 0
        players[1].pawns = [(HEIGHT - 1, j) for j in range(WIDTH)] 

        # Variables required for TwoPlayerGame fullfill TwoPlayerGame class
        self.players = players
        self.current_player = 1

    def possible_moves(self):
        """
        Calculating all possible moves that player can do

        Returns:
        list((int,int), (int,int)):
            return list of current postion of pawn and where it can move

        """
        moves = []
        dir = self.player.direction 
        for i, j in self.player.pawns:
            # Check what moves are possible
            # It checks for place ahead and diagonally left and right
            if (i + dir, j) not in self.opponent.pawns:
                moves.append(((i, j), (i + dir, j)))
            if (i + dir, j + 1) in self.opponent.pawns:
                moves.append(((i, j), (i + dir, j + 1)))
            if (i + dir, j - 1) in self.opponent.pawns:
                moves.append(((i, j), (i + dir, j - 1)))

        # Return list of all possible moves
        return moves

    def make_move(self, move):
        """
        Making a move and dealing with ist consequences

        Parameters:
        move list((int, int)(int, int)):
            move that has to made, in move[0] we have current postion of pawn
            and in move[1] place on which to place this pawn

        """

        currentPostion = move[0] # Current postion of the pawn
        nextPostion    = move[1] # Postion to which move the pawn

        # Get postion of pawn we want to move in the array of all pawns
        pawnIndex = self.player.pawns.index(currentPostion)
        # Move pawn to new postion
        self.player.pawns[pawnIndex] = nextPostion

        # If moved pawn lands on opponents pawn
        if nextPostion in self.opponent.pawns:
            # Remove opponents pawn
            self.opponent.pawns.remove(nextPostion)

    def lose(self):
        """
        Calculating if loosing condition appeared fo a player

        Returns:
            bool: If True player lost the match, opposite if False

        """

        # Is oponents pawn on my side
        cond1 = any([i == self.opponent.goal_line for i, j in self.opponent.pawns])
        # Are there any possible moves
        cond2 = self.possible_moves() == []

        return cond1 or cond2

    def win(self):
        """
        Calculating if winning condition appeared fo a player

        Returns:
            bool: If True player lost the match, opposite if False

        """

        # Is oponents pawn on my side
        cond1 = any([i == self.opponent.goal_line for i, j in self.opponent.pawns])
        # Are there any possible moves
        cond2 = self.possible_moves() == []

        return not (cond1 or cond2)

    def is_over(self):
        """
        Function required by TwoPlayerGame Class

        Returns:
            bool: If True player lost the match, opposite if False

        """
        return self.lose()

    def show(self):
        """
        Show play area with current position of the pawns and the cordinates

        """
        print("")
        print("X ", end=" ")
        for y in range(self.size[1]):
            print(y, end=" ")
        print("\n")

        for x in range(self.size[0]):
            print(x, end="  ")
            for y in range(self.size[1]):
                if (x, y) in self.players[0].pawns:
                    print("1", end=" ")
                elif (x, y) in self.players[1].pawns:
                    print("2", end=" ")
                else:
                    print(".", end=" ")
            print("")



if __name__ == "__main__":
    # Parse commandline arguments
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--player1',
        action='store',
        type=str,
        required=True,
        help="Type of player participating in game. Can take value of 'AI' or 'Human'")
    my_parser.add_argument('--player2',
        action='store',
        type=str,
        required=True,
        help="Type of player participating in game. Can take value of 'AI' or 'Human'")
    my_parser.add_argument('--boardSize',
        action='store',
        type=int,
        help="Size of checkerboard. Default is 3 which is also resonable minimum")
    my_parser.add_argument('--aiDepth',
        action='store',
        type=int,
        help="Number od moves that AI computes forward")
    args = my_parser.parse_args()

    # Assign commandline arguments to variables
    if args.boardSize:
        BOARD_SIZE = args.boardSize
    else:
        BOARD_SIZE = 3

    if args.aiDepth:
        AI_DEPTH = args.aiDepth
    else:
        AI_DEPTH = 10

    # Initiate players and AI alogrithm
    scoring = lambda game: -100 if game.lose() else 0
    #scoring = lambda game: 100 if game.win() else 0
    if args.player1 == "AI":
        PLAYER1 = AI_Player(Negamax(AI_DEPTH, scoring))
    elif args.player1 == "Human":
        PLAYER1 = Human_Player()

    if args.player2 == "AI":
        PLAYER2 = AI_Player(Negamax(AI_DEPTH, scoring))
    elif args.player2 == "Human":
        PLAYER2 = Human_Player()

    game = Hexapawn([PLAYER1, PLAYER2], size=(BOARD_SIZE,BOARD_SIZE))
    game.play()
    print("player %d wins after %d turns " % (game.opponent_index, game.nmove))
