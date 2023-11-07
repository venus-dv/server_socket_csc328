#!/usr/bin/env python3
#   Author:		Venus Velazquez
#	Major:		CS
#	Due Date:	Oct. 31, 2023
#	Course:		CSC328 020
#	Assignment:	Socket programming
#	Filename:	project5.py
#	Purpose: 	This client program reads word data from a server

import struct
import sys
import socket

# Description: Checks for command line arguments 
# Parameters:  N/A
# Returns:     str - host server, int - port number
def check_args():

    # check for number of arguments
    num_args = len(sys.argv)

    # args will be <host> <port>
    if num_args == 3:

        host = sys.argv[1]
        port = sys.argv[2]

        if not isinstance(host, str): 
            print("Error: expected string for <host>")
            sys.exit(-1)

        if not port.isdigit():
            print("Error: expected integer for <port>")
            sys.exit(-1)
        else:
            port = int(port)

        if port < 10000 or port > 65535:
            print("Error: expected <port> from 10000 to 65535")
            sys.exit(-1)
    else:
        print("Usage: ./client <host> <port>")
        sys.exit(-1)

    return (host, port)

# Description: Creates socket and connects to host and port
# Parameters:  str host - host name to connect
#              int port - port  number to connect
# Returns:     socket object - socket object that will receive packets
def conn_socket(host, port):

    try:
        # creation & connection of socket
        client_socket = socket.create_connection((host, port))

        # return socket object
        return (client_socket)
    
    except socket.error as e:
        print("Socket error: ", e)
        sys.exit(-1)
    except Exception as err:
        print("An error occurred: ", err)
        sys.exit(-1)


# Description: Converts 2 bytes in front of each word to an integer
# Parameters:  int byte_data - number of bytes to grab
# Returns:     int - the converted integer  
def bytes_to_int(byte_data):

    if len(byte_data) == 2:
        try:
            # unpack the bytes as an integer
            integer = struct.unpack('>H', byte_data)[0]
        except struct.error as e :
            print("Error trying to unpack bytes: ", e)
            sys.exit(-1)
    else:
        print("Error: Byte data size does not match expected size.")
        sys.exit(-1)

    return(integer)

# Description: Reads word packets sent from server
# Parameters:  socket object client_socket - the client receiving the word packets
# Returns:     str - the entire string containing all the words and bytes
def read_word_packets(client_socket):

    data = b""

    while True:
        try:
            temp = client_socket.recv(1024)
        except socket.error as e:
            print("Error receiving data: ", e)
            sys.exit(-1)
        if len(temp) == 0:
            break

        data += temp

    return(data)

# Description: Parses the packets received
# Parameters:  str data - the entire string of bytes and words
# Returns:     array - all words parsed from the packets
def parse_packet(data):

    all_words = []
    curr_byte = 0

    while curr_byte < len(data):
        byte_len = bytes_to_int(data[curr_byte:curr_byte + 2])
        curr_byte += 2
        all_words.append(data[curr_byte:curr_byte + byte_len])
        curr_byte += byte_len
    
    return(all_words)

# Description: Formats each word to print on a new line
# Parameters:  array words - the array holding all the words from the packets
# Returns:     N/A
def print_words(words):

    for word in words:
        print(word)
    
if __name__ == "__main__":

    # host and port 
    conn_data = check_args()

    # socket connected to server
    client_socket = conn_socket(conn_data[0], conn_data[1])

    data = read_word_packets(client_socket)
    words = parse_packet(data)
    print_words(words)

    if client_socket:
        try:
            client_socket.close()
        except IOError as e:
            print("An error occurred trying to close the socket: ", e)
            sys.exit(-1)