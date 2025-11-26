// go-backend/agents/ConversationAgent.go
package agents

import (
    "core"
    "fmt"
    "time"
)

type ConversationAgent struct {
    Name string
}

func NewConversationAgent() *ConversationAgent {
    agent := &ConversationAgent{Name: "ConversationAgent"}

    // Subscribe to DB events
    core.Bus.Subscribe("db:update", agent.HandleDBUpdate)
    core.Bus.Subscribe("db:delete", agent.HandleDBDelete)

    core.Log(fmt.Sprintf("[%s] Initialized", agent.Name))
    return agent
}

// Start or continue a conversation session
func (c *ConversationAgent) HandleConversation(sessionID string, message string, metadata map[string]interface{}) map[string]interface{} {
    // Simple example: echo + timestamp
    response := fmt.Sprintf("You said: %s", message)
    result := map[string]interface{}{
        "sessionID": sessionID,
        "message": message,
        "response": response,
        "metadata": metadata,
        "timestamp": time.Now().String(),
    }

    // Save conversation to DB
    convID := fmt.Sprintf("conv_%s_%d", sessionID, time.Now().UnixMilli())
    core.DB.Set("conversations", convID, result, "edge")

    // Emit DB update event
    go core.Bus.Publish("db:update", map[string]interface{}{
        "collection": "conversations",
        "key": convID,
        "value": result,
        "source": c.Name,
    })

    core.Log(fmt.Sprintf("[%s] Conversation handled → %s:%s", c.Name, "conversations", convID))
    return result
}

// Handle DB update events
func (c *ConversationAgent) HandleDBUpdate(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB update received: %s:%s", c.Name, collection, key))
}

// Handle DB delete events
func (c *ConversationAgent) HandleDBDelete(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB delete received: %s:%s", c.Name, collection, key))
}

// Recover from errors
func (c *ConversationAgent) Recover(err error) {
    core.Error(fmt.Sprintf("[%s] Recovering from error: %v", c.Name, err))
}

func init() {
    core.RegisterAgent("ConversationAgent", NewConversationAgent())
}
