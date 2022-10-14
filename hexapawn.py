"""
Gra:
    Hexapawn[https://pl.wikipedia.org/wiki/Hexapawn]
    Moliwość zagrania[https://www.mrozilla.cz/lab/hexapawn]

Autorzy:
    Damian Kijańczuk s20154
    Szymon Ciemny 

Przygotowanie środowiska:
    Oprócz języka Python, potrzebna takze będzie biblioteka easyAI[https://zulko.github.io/easyAI/installation.html]

Uruchomienie oraz instrukcja:
    By uruchomić wpisujemy
    'python3 hexapawn.py'

    By wyśwetlić mozliwe ruchy nalezy wpisać
    'show moves'


"""


from easyAI import TwoPlayerGame, AI_Player, Human_Player, Negamax

class Hexapawn(TwoPlayerGame):
    def __init__(self, players, size=(3, 3)):
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
        # Is oponents pawn on my side
        cond1 = any([i == self.opponent.goal_line for i, j in self.opponent.pawns])
        # Are there any possible moves
        cond2 = self.possible_moves() == []

        return cond1 or cond2

    def is_over(self):
        return self.lose()

    def show(self):
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
        
        print("")


if __name__ == "__main__":
    scoring = lambda game: -100 if game.lose() else 0
    ai = Negamax(10, scoring)
    game = Hexapawn([AI_Player(ai), AI_Player(ai)], size=(5,5))
    game.play()
    print("player %d wins after %d turns " % (game.opponent_index, game.nmove))
