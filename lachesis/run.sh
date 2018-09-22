#!/bin/sh

#docker network create --subnet 172.30.100.0/24 hashgraph_net

# -d bridge :
# network is a User Defined Bridge : Containers connected to the same 
# user-defined bridge network automatically expose all ports to each other
# --subnet : 
# if the netmask is 255.255.255.0 (or /24 for short), and the network address 
# is 192.168.10.0, then that defines a range of IP addresses 192.168.10.0 
# through 192.168.10.255

docker network create -d bridge --subnet=172.30.100.0/24 hashgraph_net
docker network ls

docker run --rm --name node1 --ip 172.30.100.101 --network="hashgraph_net" node1 &
docker run --rm --name node2 --ip 172.30.100.102 --network="hashgraph_net" node2 &
docker run --rm --name node3 --ip 172.30.100.103 --network="hashgraph_net" node3 &
sleep 5 
docker network inspect hashgraph_net 
echo PING: 
docker exec node2 ping node1 &

docker network connect hashgraph_net node1 &
docker network connect hashgraph_net node2 &
docker network connect hashgraph_net node3 &

docker exec node2 ping node1 &
read input

docker kill node1
docker kill node2
docker kill node3
docker network rm hashgraph_net
