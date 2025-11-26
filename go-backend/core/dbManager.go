// core/dbManager.go
package core

import (
    "sync"
    "time"
)

type Record map[string]interface{}

type DBManager struct {
    Edge   map[string]map[string]Record
    Shared map[string]map[string]Record
    mu     sync.RWMutex
}

var DB = &DBManager{
    Edge:   make(map[string]map[string]Record),
    Shared: make(map[string]map[string]Record),
}

// Set record
func (db *DBManager) Set(collection, key string, value Record, storage string) {
    db.mu.Lock()
    defer db.mu.Unlock()

    target := db.Edge
    if storage == "shared" {
        target = db.Shared
    }

    if _, ok := target[collection]; !ok {
        target[collection] = make(map[string]Record)
    }
    target[collection][key] = value
}

// Get record
func (db *DBManager) Get(collection, key, storage string) (Record, bool) {
    db.mu.RLock()
    defer db.mu.RUnlock()

    target := db.Edge
    if storage == "shared" {
        target = db.Shared
    }

    rec, ok := target[collection][key]
    return rec, ok
}

// Get all
func (db *DBManager) GetAll(collection, storage string) []Record {
    db.mu.RLock()
    defer db.mu.RUnlock()
    var records []Record
    target := db.Edge
    if storage == "shared" {
        target = db.Shared
    }
    for _, r := range target[collection] {
        records = append(records, r)
    }
    return records
}
