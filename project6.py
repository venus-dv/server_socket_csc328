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

def interrupt_handler(s):
    print("Server stopped.")
    s.close()
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
        with socket.socket() as s:

            print("args: ", sys.argv[0], sys.argv[1])

            s.bind(("0.0.0.0", int(sys.argv[1])))
            s.listen()

            signal.signal(signal.SIGINT, interrupt_handler(s))

            while True:
                (client_sock, client_add) = s.accept()

                file_in = "words.txt"
                word_packets = create_word_packets(file_in)

                for packet in word_packets:
                    print(packet)

                    client_sock.sendall(packet)
                
                print(f"Sent: ",  len(word_packets))

                client_sock.close()

    except OSError as err:
        exit(f'{err}')


if __name__ == "__main__":
    main()