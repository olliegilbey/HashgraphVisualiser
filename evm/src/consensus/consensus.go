package consensus

import (
	"github.com/group9/HashgraphVisualiser/evm/src/service"
	"github.com/group9/HashgraphVisualiser/evm/src/state"
)

// Consensus is the interface that abstracts the consensus system
type Consensus interface {
	Init(*state.State, *service.Service) error
	Run() error
	Info() (map[string]string, error)
}
