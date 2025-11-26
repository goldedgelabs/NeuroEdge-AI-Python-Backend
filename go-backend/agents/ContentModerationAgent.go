// go-backend/agents/ContentModerationAgent.go
package agents

import (
    "core"
    "fmt"
    "time"
)

type ContentModerationAgent struct {
    Name string
}

func NewContentModerationAgent() *ContentModerationAgent {
    agent := &ContentModerationAgent{Name: "ContentModerationAgent"}

    // Subscribe to DB events
    core.Bus.Subscribe("db:update", agent.HandleDBUpdate)
    core.Bus.Subscribe("db:delete", agent.HandleDBDelete)

    core.Log(fmt.Sprintf("[%s] Initialized", agent.Name))
    return agent
}

// Moderate content of a record
func (c *ContentModerationAgent) ModerateContent(collection string, key string, content map[string]interface{}) map[string]interface{} {
    moderationResult := map[string]interface{}{
        "recordID": key,
        "collection": collection,
        "status": "approved",
        "issues": []string{},
        "checkedAt": time.Now().String(),
    }

    // Example checks: flag offensive words or inappropriate content
    offensiveWords := []string{"badword1", "badword2", "badword3"}
    for field, val := range content {
        strVal, ok := val.(string)
        if !ok {
            continue
        }
        for _, word := range offensiveWords {
            if containsWord(strVal, word) {
                moderationResult["status"] = "flagged"
                moderationResult["issues"] = append(moderationResult["issues"].([]string), field)
            }
        }
    }

    // Save moderation result
    moderationID := fmt.Sprintf("moderation_%s_%d", key, time.Now().UnixMilli())
    core.DB.Set("moderation_results", moderationID, moderationResult, "edge")

    // Publish DB update event
    go core.Bus.Publish("db:update", map[string]interface{}{
        "collection": "moderation_results",
        "key": moderationID,
        "value": moderationResult,
        "source": c.Name,
    })

    core.Log(fmt.Sprintf("[%s] Content moderation done → %s:%s Status: %s", c.Name, collection, key, moderationResult["status"]))
    return moderationResult
}

// Simple helper to check if a word exists in a string
func containsWord(text string, word string) bool {
    // naive implementation; can be improved with regex
    return len(text) >= len(word) && (text == word || len(text) > len(word) && (text[:len(word)] == word || text[len(text)-len(word):] == word || contains(text, word)))
}

func contains(text, word string) bool {
    return len(text) > len(word) && (indexOf(text, word) >= 0)
}

// IndexOf helper
func indexOf(text, word string) int {
    for i := 0; i <= len(text)-len(word); i++ {
        if text[i:i+len(word)] == word {
            return i
        }
    }
    return -1
}

// Handle DB update events
func (c *ContentModerationAgent) HandleDBUpdate(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB update received: %s:%s", c.Name, collection, key))
}

// Handle DB delete events
func (c *ContentModerationAgent) HandleDBDelete(event map[string]interface{}) {
    collection := event["collection"].(string)
    key := event["key"].(string)
    core.Log(fmt.Sprintf("[%s] DB delete received: %s:%s", c.Name, collection, key))
}

// Recover from errors
func (c *ContentModerationAgent) Recover(err error) {
    core.Error(fmt.Sprintf("[%s] Recovering from error: %v", c.Name, err))
}

func init() {
    core.RegisterAgent("ContentModerationAgent", NewContentModerationAgent())
}
