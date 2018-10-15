# HashgraphVisualiser
A visualiser tool for the Hashgraph algorithm displayed by web frontend.

## Usage
* ### Open two AWS terminals using the following command:
``` ssh -L 3333:localhost:3333 -i team9-blockchain.pem ubuntu@18.222.162.68```

* ### Run the data streamer in one AWS terminal
```cd /go/src/github.com/group9/HashgraphVisualiser/data_streamer```
```go run data_streamer.go```

* ### Run the docker instances in the other AWS terminal
```cd  go/src/github.com/group9/HashgraphVisualiser/lachesis```
``` docker-compose up```

* ### In a local terminal run the `pyserver.py`
```python pyserver.py```

* ### In a fourth terminal run the `pyflask.py`
```python pyflask.py```

* ### Open a browser to
```localhost:5001```
