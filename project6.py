#!/usr/bin/env python3
#   Author:		Venus Velazquez
#	Major:		CS
#	Due Date:	Nov. 7, 2023
#	Course:		CSC328 020
#	Assignment:	Socket programming
#	Filename:	project6.py
#	Purpose: 	This server program sends word data to connected clients

import signal
import os
import sys
import socket
import struct
import random

# Description:  
# Parameters:   
# Returns: 

def signal_handler(sig, frame):
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

        print("Socket: ", s_socket)

        s_socket.bind(("127.0.0.1", int(sys.argv[1])))

        print("A")

        s_socket.listen()

        print("B")

        while True:
            (client_sock, client_add) = s_socket.accept()

            print("passed accept")

            file_in = "words.txt"
            word_packets = create_word_packets(file_in)

            print("passed create word packets")

            for packet in word_packets:
                print(packet)

                client_sock.sendall(packet)
            
            print("Sent: ", word_packets)

            client_sock.close()

    except OSError as err:
        print("Error: ", err)
        sys.exit(-1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    pid = os.fork()
    if pid == 0:
        main()
    else:
        child_pid, exit_status = os.wait()

# python project6.py 55555