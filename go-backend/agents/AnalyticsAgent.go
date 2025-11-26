// go-backend/agents/AnalyticsAgent.go
package agents

import (
    "core"
    "fmt"
)

type AnalyticsAgent struct {
    Name string
}

func NewAnalyticsAgent() *AnalyticsAgent {
    agent := &AnalyticsAgent{Name: "AnalyticsAgent"}

    // Subscribe to DB events
    core.Bus.Subscribe("db:update", agent.HandleDBUpdate)
    core.Bus.Subscribe("db:delete", agent.HandleDBDelete)

    core.Log(fmt.Sprintf("[%s] Initialized", agent.Name))
    return agent
}

// Analyze data and store results
func (a *AnalyticsAgent) AnalyzeData(collection, key string, data map[string]interface{}) map[string]interface{} {
    result := map[string]interface{}{
        "id":         key,
        "collection": collection,
        "analytics":  data, // simple placeholder for analysis results
    }

    // Save to edge DB
    core.DB.Set(collection, key, result, "edge")

    // Emit DB update event concurrently
    go core.Bus.Publish("db:update", map[string]interface{}{
        "collection": collection,
        "key":        key,
        "value":      result,
        "source":     a.Name,
    })

    core.Log(fmt.Sprintf("[%s] DB updated → %s:%s", a.Name, collection, key))
    return result
}

// Handle DB update events
func (a *AnalyticsAgent) HandleDBUpdate(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB update received: %s:%s", a.Name, collection, key))
}

// Handle DB delete events
func (a *AnalyticsAgent) HandleDBDelete(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB delete received: %s:%s", a.Name, collection, key))
}

// Recover from errors
func (a *AnalyticsAgent) Recover(err error) {
    core.Error(fmt.Sprintf("[%s] Recovering from error: %v", a.Name, err))
}

func init() {
    core.RegisterAgent("AnalyticsAgent", NewAnalyticsAgent())
}
