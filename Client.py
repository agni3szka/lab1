#!/usr/bin/env python
import socket
import sys
import os
from Board import Board

class Client:
    def __init__(self, address, server_port, server_data_size):
        self._data_size = server_data_size
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connect_to_server(address, server_port)
        self._server_address = (address, server_port)

    def _connect_to_server(self, address, server_port):
        server_address = (address, server_port)
        self._socket.connect(server_address)

    def initializePlayer(self):
        print('Waiting for server to initialize player')
        self._symbol = self._socket.recv(self._data_size)
        print('Intialized' + str(self._symbol))

    def startGame(self):
        b = Board()
        b.cls()
        print('---------------Starting the Game----------------')
        print >>sys.stderr, 'Fighting with: ', self._server_address
        print('Your symbol is: ' + self._symbol)      
        b.printHelp()
        while True:
            while True:
                msg = raw_input('Type number of field you want to fill (h for help, q for quit):\n')
                if(b.checkIfEmpty(msg)):
                    b.addMove(msg, self._symbol)
                    b.printBoard()
                    self._socket.send(str(msg))
                    break
                else:
                    if msg == 'q':
                        self._socket.close()
                        sys.exit()
                        break
                    if msg == 'h':
                        b.printHelp()
                    else:
                        print('bad move')

            if msg == 'h':
                b.printHelp()
            b.cls()
            print('---------------Starting the Game----------------')
            print >>sys.stderr, 'Fighting with: ', self._server_address
            print('Your symbol is: ' + self._symbol)      
            b.printBoard()
            print('Waiting for move...')
            response = self._socket.recv(self._data_size)
            b.addMove(response, 'X')
            b.cls()
            print('---------------Starting the Game----------------')
            print >>sys.stderr, 'Fighting with: ', self._server_address
            print('Your symbol is: ' + self._symbol)      
            b.printBoard()
            print('Player X: ' + str(response))
            if msg == 'q' or response == 'q':
                print('---------------End of the game----------------')
                self._socket.close()
                break


if __name__ == "__main__":
    host = 'localhost'
    port = 5004
    data_size = 512
    client = Client(host, port, data_size)
    client.initializePlayer()
    client.startGame()