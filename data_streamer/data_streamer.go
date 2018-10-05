package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
	"time"
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
	x         int
	y         int
	isFamous  bool
	isWitness bool
	jsonData  jsonEvent
}

type line struct {
	x1 int
	x2 int
	y1 int
	y2 int
	color string
}

var events = make(map[string]event) // map of events
var lines = make(map[string]map[string]line) // line that exist between any two events

const famousColor = "green"
const witnessColor = "blue"
const famousWitnessColor = "red"
const defaultColor = "black"
const nodeNumber = 3

func main() {

	//var output net.Conn
	var currX = 5

	/*
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
	*/

	// get root events
	

	for currentRoundNumber := 0; currentRoundNumber < 3; currentRoundNumber++ {

		// populate events map with new events
		for i := 1; i < nodeNumber; i++ {
			var currentRoundJson jsonRound
			var is = strconv.Itoa(i);
			json.Unmarshal(getData("http://localhost:800"+is+"/round/"+strconv.Itoa(currentRoundNumber)), &currentRoundJson)
			for key, value := range currentRoundJson.Events {
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
				var eventData jsonEvent
				json.Unmarshal(getData("http://localhost:800"+is+"/event/"+string(key)), &eventData)
				if eventData.Body.Parents[0] == "" {
					newEvent.x = currX
					currX += 1
					newEvent.y = 5
				}
				newEvent.jsonData = eventData
				events[key] = newEvent
			}
		}
		// populates lines 2d map with new lines
		for key, event := range events {
			if event.jsonData.Body.Parents[0] != "" {
				// event data
				event.x = events[event.jsonData.Body.Parents[0]].x
				event.y = events[event.jsonData.Body.Parents[0]].y + 1
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
				var selfParentLine line
				selfParentLine.x1 = events[event.jsonData.Body.Parents[0]].x
				selfParentLine.y1 = events[event.jsonData.Body.Parents[0]].y
				selfParentLine.x2 = event.x
				selfParentLine.y2 = event.y
				selfParentLine.color = color
				if lines[event.jsonData.Body.Parents[0]] == nil {
					lines[event.jsonData.Body.Parents[0]] = make(map[string]line)
				}
				lines[event.jsonData.Body.Parents[0]][key] = selfParentLine
				var otherParentLine line
				otherParentLine.x1 = events[event.jsonData.Body.Parents[1]].x
				otherParentLine.y1 = events[event.jsonData.Body.Parents[1]].y
				otherParentLine.x2 = event.x
				otherParentLine.y2 = event.y
				otherParentLine.color = color
				if lines[event.jsonData.Body.Parents[1]] == nil {
					lines[event.jsonData.Body.Parents[1]] = make(map[string]line)
				}
				lines[event.jsonData.Body.Parents[1]][key] = otherParentLine
			}
		}
		fmt.Println(events)
		fmt.Println(lines)
	}

}

func getData(url string) []byte {
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println(".")
		time.Sleep(10000000)
		return getData(url)
	}
	defer resp.Body.Close()
	respBody, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Print(err)
	}
	return respBody
}
