FROM golang:1.8

WORKDIR /go/src/app
#COPY . .
COPY ./lachesis ./lachesis
COPY ./node_config ./node_config

#CMD ./evm/build/evm run --api_addr :6000

CMD ./lachesis/build/lachesis run -node_addr="`hostname -i`:12000" -service_addr="`hostname -i`:8000" -datadir=$DATADIR -store="inmem" 

