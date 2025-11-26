// go-backend/agents/CorrectionAgent.go
package agents

import (
    "core"
    "fmt"
)

type CorrectionAgent struct {
    Name string
}

func NewCorrectionAgent() *CorrectionAgent {
    agent := &CorrectionAgent{Name: "CorrectionAgent"}

    // Subscribe to DB events
    core.Bus.Subscribe("db:update", agent.HandleDBUpdate)
    core.Bus.Subscribe("db:delete", agent.HandleDBDelete)

    core.Log(fmt.Sprintf("[%s] Initialized", agent.Name))
    return agent
}

// Apply corrections to a record in the database
func (c *CorrectionAgent) CorrectEntry(collection string, key string, corrections map[string]interface{}) map[string]interface{} {
    record, ok := core.DB.Get(collection, key, "edge")
    if !ok {
        core.Log(fmt.Sprintf("[%s] Record not found: %s:%s", c.Name, collection, key))
        return nil
    }

    // Apply corrections
    for k, v := range corrections {
        record[k] = v
    }

    // Save updated record
    core.DB.Set(collection, key, record, "edge")

    // Emit DB update event
    go core.Bus.Publish("db:update", map[string]interface{}{
        "collection": collection,
        "key": key,
        "value": record,
        "source": c.Name,
    })

    core.Log(fmt.Sprintf("[%s] Record corrected: %s:%s → %v", c.Name, collection, key, corrections))
    return record
}

// Handle DB update events
func (c *CorrectionAgent) HandleDBUpdate(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB update received: %s:%s", c.Name, collection, key))
}

// Handle DB delete events
func (c *CorrectionAgent) HandleDBDelete(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB delete received: %s:%s", c.Name, collection, key))
}

// Recover from errors
func (c *CorrectionAgent) Recover(err error) {
    core.Error(fmt.Sprintf("[%s] Recovering from error: %v", c.Name, err))
}

func init() {
    core.RegisterAgent("CorrectionAgent", NewCorrectionAgent())
}
