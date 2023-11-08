#!/usr/bin/env python3
#   Author:		Venus Velazquez
#	Major:		CS
#	Due Date:	Nov. 7, 2023
#	Course:		CSC328 020
#	Assignment:	Socket programming
#	Filename:	project6.py
#	Purpose: 	This server program sends word data to connected clients

# import signal
# import os
import sys
import socket
import struct
import random

# Description:  Handler for keyboard interrupt  
# Parameters:   int sig - the signal being handled
# Returns:      N/A
# def signal_handler(sig):
#     print("Server stopped.")
#     sys.exit(0)

# Description:  Creates word packets to send to client
# Parameters:   N/A
# Returns:      list - all packets being sent to client
def create_word_packets():
    word_list = ["apple", "red", "blue", "bank", "bat", "dog", "moon", 
                 "flower", "food", "grape", "cat", "day", "chair", "car", 
                 "sun", "water", "soda", "bird", "pear", "trophy"]
    
    num_packets = random.randint(1, 10)
    packets = []
    for _  in range(num_packets):
        word = random.choice(word_list)
        word_length = len(word)
        bytes = struct.pack('!H', word_length)
        word_bytes = word.encode('ascii', errors = 'strict') 
        word_packet = bytes + word_bytes
        packets.append(word_packet)

    return(packets)

def main():
    if len(sys.argv) != 2:
        exit('Usage: ./server <port>')

    try:
        s_socket = socket.socket()
        s_socket.bind(("127.0.0.1", int(sys.argv[1])))
        s_socket.listen(5)

        while True:
            (client_sock, client_add) = s_socket.accept()

            word_packets = create_word_packets()

            for packet in word_packets:
                client_sock.sendall(packet)

            client_sock.close()
    except OSError as err:
        print("Error: ", err)
        sys.exit(-1)
    except KeyboardInterrupt:
        print("Server terminated")
        s_socket.close()
        sys.exit(0)

if __name__ == "__main__":
    # signal.signal(signal.SIGINT, signal_handler)
    # pid = os.fork()
    # if pid == 0:
        main()
    # else:
    #     child_pid, exit_status = os.wait()