import os
class Board:
    def __init__(self):
        self._board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']

    def addMove(self, fieldNumber, symbol):
        self._board[int(fieldNumber)-1] = str(symbol)


    def checkIfEmpty(self, fieldNumber):
        if fieldNumber.isdigit() and int(fieldNumber) <= 9:
            if self._board[int(fieldNumber)-1] == ' ':
                return True
            else:
                return False
        else:
            return False

    def printBoard(self):
        print('   %s   ||   %s   ||   %s   ' % (self._board[0], self._board[1], self._board[2]))
        print('=========================')
        print('   %s   ||   %s   ||   %s   ' % (self._board[3], self._board[4], self._board[5]))
        print('=========================')
        print('   %s   ||   %s   ||   %s   ' % (self._board[6], self._board[7], self._board[8]))
    def printHelp(self):
    	print('Numbering of fields:')
    	print('   1   ||   2   ||   3   ')
    	print('=========================')
    	print('   4   ||   5   ||   6   ')
    	print('=========================')
    	print('   7   ||   8   ||   9   ')

    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')