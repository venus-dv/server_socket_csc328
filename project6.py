#!/usr/bin/env python3
#   Author:		Venus Velazquez
#	Major:		CS
#	Due Date:	Nov. 7, 2023
#	Course:		CSC328 020
#	Assignment:	Socket programming
#	Filename:	project6.py
#	Purpose: 	This server program sends word data to connected clients

import sys
import socket

# Description:  
# Parameters:   
# Returns: 


def main():

    if len(sys.argv) != 2:
        exit('Usage: server <port>')
    try:
        with socket.socket() as s:
            s.bind(("127.0.0.1", int(sys.argv[1])))
            s.listen()
            while True:
                (client_sock, client_add) = s.accept()

                while True:
                    data = client_sock.recv(1024)
                    if data != b'':
                        client_sock.sendall(data)
                        break
    except OSError as err:
        exit(f'{err}')


if __name__ == "__main__":
    main()