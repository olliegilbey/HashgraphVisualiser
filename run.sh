#!/bin/bash

docker-compose --file ./lachesis/docker-compose.yml up --build > /dev/null &
go run ./data_streamer/data_streamer.go &
# start Bernard's conversion program
# start graph streaming program


