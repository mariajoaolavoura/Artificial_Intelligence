#!/bin/bash

s()
{
	ghosts=$1

	if [ $# -eq 0 ]; then	
		ghosts=0
	fi

	python server.py --ghosts $ghosts
}

v()
{	
	python viewer.py
}

c()
{	
	python client.py
}

ks()
{
	fuser 8000/tcp
}

k()
{
	pkill -f "python client.py"
}


##################

# chama o server online e joga
sr()
{
	ghosts=$1

	if [ $# -eq 0 ]; then	
		ghosts=0
	fi

	PORT=80 SERVER=pacman-aulas.ws.atnog.av.it.pt NAME=SantissimaTrindade python client.py
}

# viewer para servidor online
vr()
{
	python viewer.py --server pacman-aulas.ws.atnog.av.it.pt --port 80 --scale 2
}
