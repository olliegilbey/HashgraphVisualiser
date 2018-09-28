FROM golang:1.8

WORKDIR /go/src/app
COPY . .

CMD ./build/lachesis run -node_addr="localhost:12000" -service_addr="localhost:8000" -datadir=$DATADIR -store="inmem" 

