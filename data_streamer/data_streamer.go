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

type event struct {
	IsFamous  bool
	IsWitness bool
	Parents   []string
	Timestamp time.Time
}

type round struct {
	Number int
	Events map[string]event
}

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

func main() {

	var participants []string
	var currentRound round
	var consensusEvents []string
	var output net.Conn

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
	data, err := json.Marshal(participants)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("write participants")
	output.Write(data)
	output.Read(make([]byte, 2))

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

		// output
		data, err := json.Marshal(currentRound)
		if err != nil {
			fmt.Println(err)
		}
		fmt.Println("write current round")
		output.Write(data)
		output.Read(make([]byte, 2))
		data, err = json.Marshal(consensusEvents)
		if err != nil {
			fmt.Println(err)
		}
		fmt.Println("write consensus events")
		output.Write(data)
		output.Read(make([]byte, 2))
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
