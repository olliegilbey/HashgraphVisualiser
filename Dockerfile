FROM golang:1.8

#WORKDIR /go/src/app
#COPY . .

RUN git clone https://github.com/andrecronje/evm.git
RUN git clone https://github.com/andrecronje/lachesis.git

CMD curl https://glide.sh/get | sh
CMD glide install

CMD cd lachesis
CMD make build

CMD cd evm
CMD make build

CMD ./build/evm run --api_addr="`hostname -i`:6000" 

#CMD ./build/lachesis run -node_addr="`hostname -i`:12000" -service_addr="`hostname -i`:8000" -datadir=$DATADIR -store="inmem" 

