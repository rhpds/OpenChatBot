#!/usr/bin/env bash

APP_HOME=$(pwd)

if [ "$#" -eq 0 ]; then
	echo Starting Chainlit Chatbot
	chainlit run src/main.py --watch --headless --port 8443
else
	exec "$@"
fi
