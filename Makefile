#	Author:	    Venus Velazquez
#	Major:      CS
#	Due Date:   Nov. 7, 2023
#	Course:	    CSC328 020
#	Assignment: Socket programming
#	Filename:   Makefile
#	Purpose:    Creates executable for project6 and cleans up artifacts

all: server

server: project6.py
	@cp project6.py server
	@chmod a+x server

.PHONY: clean submit
clean:
	rm -f server
	rm -rf __pycache__
submit:
	~schwesin/bin/submit csc328 project6
