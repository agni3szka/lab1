#!/usr/bin/env python
import socket
import sys
from Board import Board
class Server:
    def __init__(self, address, server_port, server_data_size):
        self._data_size = server_data_size
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (address, server_port)
        self._socket.bind(server_address)
        self._players = 0
        self._clientSymbol = 'O'
        self._symbol = 'X'
        print('Stating TicTacToe server on %s:%s' % server_address)

    def listen(self):
        self._socket.listen(5)
        while True:
            channel, client_address = self._socket.accept()
            b = Board()            
            b.cls()
            print('---------------Starting the Game----------------')
            print >>sys.stderr, 'Fighting with: ', client_address
            print('Your symbol is: ' + self._symbol)
            b.printHelp()
            try:
                channel.sendall(self.initializePlayer())
                while True:
                    print('Waiting for move...')
                    data = channel.recv(self._data_size)
                    b.cls()
                    print('---------------Starting the Game----------------')
                    print >>sys.stderr, 'Fighting with: ', client_address
                    print('Your symbol is: ' + self._symbol)
                    print('Player O: ' + str(data)) 
                    b.addMove(data, 'O')
                    b.printBoard()
                    if str(data) == 'q' or not data:
                        print('---------------End of the game----------------')
                        channel.close()
                        sys.exit()
                        break
                    if data == 'h':
                        b.printHelp()
                    else:
                        while True:
                            msg = raw_input('Type number of field you want to fill (h for help, q for quit):\n')
                            if(b.checkIfEmpty(msg)):
                                b.cls()
                                print('---------------Starting the Game----------------')
                                print >>sys.stderr, 'Fighting with: ', client_address
                                print('Your symbol is: ' + self._symbol)
                                b.addMove(msg, self._symbol)
                                b.printBoard()
                                channel.send(str(msg))
                                break
                            else:
                                if msg == 'q':
                                    channel.close()
                                    break
                                if msg == 'h':
                                    b.printHelp()
                                else:
                                    print('bad move')

                    
            finally:
                print('Connection %s:%s closed' % client_address)
                break
                channel.close()            


    def initializePlayer(self):
        return str(self._clientSymbol)


if __name__ == "__main__":
    host = "localhost"
    port = 5004
    data_size = 512
    server = Server(host, port, data_size)
    server.listen()
