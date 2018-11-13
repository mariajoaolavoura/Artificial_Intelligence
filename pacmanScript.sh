#!/bin/bash

s()
{
	ghosts=$1

	if [ $# -eq 0 ]; then	
		ghosts=0
	fi

	source venv/bin/activate
	python server.py --ghosts $ghosts
	pacman > gnome-terminal
}

v()
{
	source venv/bin/activate	
	python viewer.py
	pacman > gnome-terminal
}

c()
{
	source venv/bin/activate	
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
