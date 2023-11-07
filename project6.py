#!/usr/bin/env python3
#   Author:		Venus Velazquez
#	Major:		CS
#	Due Date:	Nov. 7, 2023
#	Course:		CSC328 020
#	Assignment:	Socket programming
#	Filename:	project6.py
#	Purpose: 	This server program sends word data to connected clients

import signal
import sys
import socket
import struct
import random

# Description:  
# Parameters:   
# Returns: 

def interrupt_handler(s_socket):
    print("Server stopped.")
    s_socket.close()
    sys.exit(0)

def create_word_packets(file_in):

    with open(file_in, 'r') as file:
        words = file.read().splitlines()
    num_packets = random.randint(1, 10)
    packets = []

    for _  in range(num_packets):
        word = random.choice(words)
        word_length = len(word)
        word_bytes = struct.pack('>H', word_length)
        word_data = word.encode('ascii')
        word_packet = word_bytes + word_data
        packets.append(word_packet)

    return(packets)


def main():

    if len(sys.argv) != 2:
        exit('Usage: server <port>')
    try:
        print("args: ", sys.argv[0], sys.argv[1])

        s_socket = socket.socket()
        s_socket.bind(("0.0.0.0", int(sys.argv[1])))
        s_socket.listen()

        signal.signal(signal.SIGINT, interrupt_handler(s_socket))

        while True:
            (client_sock, client_add) = s_socket.accept()

            file_in = "words.txt"
            word_packets = create_word_packets(file_in)

            for packet in word_packets:
                print(packet)

                client_sock.sendall(packet)
            
            print("Sent: ", word_packets)

            client_sock.close()

    except OSError as err:
	print("Error: ", err)
        sys.exit(-1)


if __name__ == "__main__":
    main()
