package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"strconv"
)

// json structs
type jsonRound struct {
	Events map[string]jsonRoundEvent
}

type jsonRoundEvent struct {
	Witness bool
	Famous  int
}

type jsonEvent struct {
	Body      jsonEventBody
	Signature string
}

type jsonEventBody struct {
	Transactions    []string
	Parents         []string
	Creator         string
	Timestamp       string
	Index           int
	BlockSignatures []string
}

// visualizer structs
type event struct {
	x           int
	y           int
	isFamous    bool
	isWitness   bool
	isConsensus bool
	jsonData    jsonEvent
}

type line struct {
	x1    int
	y1    int
	x2    int
	y2    int
	color string
}

var events = make(map[string]event)          // map of events
var lines = make(map[string]map[string]line) // line that exist between any two events

const famousColor = "green"
const witnessColor = "blue"
const famousWitnessColor = "red"
const defaultColor = "black"
const nodeNumber = 3

var currX = 0
var maxY = 0

func main() {

	var currentRoundNumber = 0

	// handle the network socket
	var channel = make(chan string)
	go handleChannel(channel)

	for {

		var lastRound = 0
		json.Unmarshal(getData("http://localhost:8001/lastround"), &lastRound)

		// get events up to current round
		for ; currentRoundNumber < lastRound; currentRoundNumber++ {

			channel <- "round:" + strconv.Itoa(currentRoundNumber) + "," + strconv.Itoa(maxY)

			// populate events map with new events
			for i := 1; i <= nodeNumber; i++ {
				var currentRoundJson jsonRound
				json.Unmarshal(getData("http://localhost:800"+strconv.Itoa(i)+"/round/"+strconv.Itoa(currentRoundNumber)), &currentRoundJson)
				for key, value := range currentRoundJson.Events {
					if _, ok := events[key]; ok {
						continue // we already have this node
					}
					var newEvent event
					if value.Famous > 0 {
						newEvent.isFamous = true
					} else {
						newEvent.isFamous = false
					}
					if value.Witness == true {
						newEvent.isWitness = true
					} else {
						newEvent.isWitness = false
					}
					// get event data and check if root node
					var eventData jsonEvent
					json.Unmarshal(getData("http://localhost:800"+strconv.Itoa(i)+"/event/"+string(key)), &eventData)
					newEvent.jsonData = eventData
					if eventData.Body.Parents[0] == "" {
						currX += 1
						newEvent.x = currX
						newEvent.y = 0
					}
					events[key] = newEvent
				}
			}

			// get consensus events and update graph
			var consensusEvents []string
			json.Unmarshal(getData("http://localhost:8001/consensusevents"), &consensusEvents)
			for _, evId := range consensusEvents {
				var ev = events[evId]
				ev.isConsensus = true
				events[evId] = ev
			}

			// populates event x's and y's
			for key := range events {
				if events[key].x == 0 {
					x, y := findEventXY(key)
					if maxY < y {
						maxY = y
					}
					e := events[key]
					e.x = x
					e.y = y
					events[key] = e
				}
			}

			// populates lines matrix with line data
			for key, event := range events {
				var selfParent = events[key].jsonData.Body.Parents[0]
				var otherParent = events[key].jsonData.Body.Parents[1]
				if selfParent == "" {
					continue
				}
				var color string
				if event.isWitness && event.isFamous {
					color = famousWitnessColor
				} else if event.isWitness {
					color = witnessColor
				} else if event.isFamous {
					color = famousColor
				} else {
					color = defaultColor
				}
				// line data
				// if consensus or not
				var consensusInt = 0
				if event.isConsensus {
					consensusInt = 1
				}
				// self parent line
				var selfParentLine line
				selfParentLine.x1 = events[selfParent].x
				selfParentLine.y1 = events[selfParent].y
				selfParentLine.x2 = event.x
				selfParentLine.y2 = event.y
				selfParentLine.color = color
				if lines[selfParent] == nil {
					lines[selfParent] = make(map[string]line)
				}
				// add to map and output to channel
				lines[selfParent][key] = selfParentLine
				channel <- "line:" + strconv.Itoa(selfParentLine.x1) + "," + strconv.Itoa(selfParentLine.y1) + "," +
					strconv.Itoa(selfParentLine.x2) + "," + strconv.Itoa(selfParentLine.y2) + "," +
					selfParentLine.color + "," + strconv.Itoa(consensusInt)
				// other parent line
				var otherParentLine line
				otherParentLine.x1 = events[otherParent].x
				otherParentLine.y1 = events[otherParent].y
				otherParentLine.x2 = event.x
				otherParentLine.y2 = event.y
				otherParentLine.color = color
				if lines[otherParent] == nil {
					lines[otherParent] = make(map[string]line)
				}
				// add to map and output to channel
				lines[otherParent][key] = otherParentLine
				channel <- "line:" + strconv.Itoa(otherParentLine.x1) + "," + strconv.Itoa(otherParentLine.y1) + "," +
					strconv.Itoa(otherParentLine.x2) + "," + strconv.Itoa(otherParentLine.y2) + "," +
					otherParentLine.color + "," + strconv.Itoa(consensusInt)
			}
		}
	}
}

func getData(url string) []byte {
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println(err)
	}
	defer resp.Body.Close()
	respBody, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Print(err)
	}
	return respBody
}

func findEventXY(key string) (int, int) {
	ev := events[key]
	selfParent := ev.jsonData.Body.Parents[0]
	if selfParent == "" {
		return ev.x, ev.y
	}
	if events[selfParent].x > 0 {
		return events[selfParent].x, events[selfParent].y + 1
	}
	x, y := findEventXY(selfParent)
	return x, y + 1
}

func handleChannel(channel chan string) {

	var output net.Conn

	// wait for listen socket connection
	l, err := net.Listen("tcp", ":2738")
	if err != nil {
		fmt.Println(err)
	}
	defer l.Close()
	output, err = l.Accept()
	if err != nil {
		fmt.Println(err)
	}

	for {
		output.Write([]byte(<-channel + "\n"))
	}
}
