package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"strconv"
	"time"
)

// hashgraph data structs
type event struct {
	Key string
	IsFamous  bool
	IsWitness bool
	Parents   []string
	Timestamp time.Time
}

type round struct {
	Number int
	Events map[string]event
}

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
type node struct {
	x int
	y int
}

type line struct {
	x1 int
	x2 int
	y1 int
	y2 int
	color string
}

func main() {

	var participants []string
	var currentRound round
	var consensusEvents []string
	var output net.Conn
	var graphNodes map[string]node = make(map[string]node)
	var newLines = []line
	var currX = 0

	// wait for listen socket connection
	l, err := net.Listen("tcp", "localhost:3333")
	if err != nil {
		fmt.Println(err)
	}
	defer l.Close()
	output, err = l.Accept()
	if err != nil {
		fmt.Println(err)
	}

	// get graph participants and output
	var participantJson map[string]int
	json.Unmarshal(getData("http://localhost:8001/participants"), &participantJson)
	for key := range participantJson {
		participants = append(participants, key)
	}

	// constantly get next round of events and output
	var currentRoundNumber int
	var prevRoundNumber int
	prevRoundNumber = -1
	for {

		// check if next round available, and if so continue
		for {
			json.Unmarshal(getData("http://localhost:8001/lastround"), &currentRoundNumber)
			currentRound.Number = currentRoundNumber
			currentRound.Events = make(map[string]event)
			if currentRoundNumber != prevRoundNumber {
				break
			}
		}
		prevRoundNumber = currentRoundNumber

		// populate currentRound.events
		var currentRoundJson jsonRound
		json.Unmarshal(getData("http://localhost:8001/round/"+strconv.Itoa(currentRoundNumber)), &currentRoundJson)
		for key, value := range currentRoundJson.Events {
			var newEvent event
			newEvent.Key = key
			if value.Famous > 0 {
				newEvent.IsFamous = true
			} else {
				newEvent.IsFamous = false
			}
			if value.Witness == true {
				newEvent.IsWitness = true
			} else {
				newEvent.IsWitness = false
			}
			var eventData jsonEvent
			json.Unmarshal(getData("http://localhost:8001/event/"+string(key)), &eventData)
			newEvent.Parents = make([]string, 2)
			newEvent.Parents[0] = eventData.Body.Parents[0]
			newEvent.Parents[1] = eventData.Body.Parents[1]
			newEvent.Timestamp, _ = time.Parse(time.RFC3339Nano, eventData.Body.Timestamp)
			currentRound.Events[key] = newEvent
		}

		// populate consensusEvents
		json.Unmarshal(getData("http://localhost:8001/consensusevents"), &consensusEvents)

		// make nodes and lines for new events
		newLines = make([]line, len(currentRound.Events))
		for (key, index := currentRound.Events) {
			var parentLine line
			var otherLine line
			var selfParent node
			var otherParent node
			if index.Parents[0] == "" {
				var newNode node
				newNode.x = currX
				currX = currX + 1
				newNode.y = 0
				graphNodes[key] = newNode
			} else {
				var newNode node
				selfParent = graphNodes[index.Parents[0].Key]
				otherParent = graphNodes[index.Parents[1].Key]
				newNode.x = selfParent.x
				newNode.y = selfParent.y + 1
				graphNodes[key] = newNode
				parentLine.x1 = selfParent.x
				parentLine.y1 = selfParent.y
				parentLine.x2 = graphNodes[key].x
				parentLine.y2 = graphNodes[key].y
				otherLine.x1 = otherParent.x
				otherLine.y1 = otherParent.y
				otherLine.x2 = graphNodes[key].x
				otherLine.y2 = graphNodes[key].y
				if index.IsWitness {
					parentLine.color = "green"
					otherLine.color = "green"
				}
				if index.IsFamous {
					parentLine.color = "blue"
					otherLine.color = "blue"
				}
				newLines = append(newLines, parentLine)
				newLines = append(newLines, otherLine)
			}
		}

		// output new lines to draw
		fmt.Println("write new lines")
		for _, v := newLines {
			data := Itoa(v.x1) + ";" + Itoa(v.y1) + ";" + Itoa(v.x2) + ";" + Itoa(v,y2) + ";" + v.color
			fmt.Println("sending line " + data)
			output.Write(data)
			output.Read(make([]byte, 2))
		}

	}

}

func getData(url string) []byte {
	resp, err := http.Get(url)
	if err != nil {
		fmt.Print(err)
	}
	defer resp.Body.Close()
	respBody, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Print(err)
	}
	return respBody
}
