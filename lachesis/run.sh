#!/bin/sh

docker network create --subnet 172.30.100.0/24 hashgraph_net

docker run --rm --name node1-run --ip 172.30.100.101 --network hashgraph_net node1 &
docker run --rm --name node2-run --ip 172.30.100.102 --network hashgraph_net node2 &
docker run --rm --name node3-run --ip 172.30.100.103 --network hashgraph_net node3 &

read input

docker kill node1-run
docker kill node2-run
docker kill node3-run
docker network rm hashgraph_net
