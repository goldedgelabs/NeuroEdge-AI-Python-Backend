// Run: go get github.com/gorilla/websocket
package main
import (
    "log"
    "net/http"
    "time"
    "github.com/gorilla/websocket"
    "fmt"
)

var upgrader = websocket.Upgrader{
    CheckOrigin: func(r *http.Request) bool { return true },
}

func wsHandler(w http.ResponseWriter, r *http.Request){
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil { log.Println('upgrade err', err); return }
    defer conn.Close()
    for {
        msgType, msg, err := conn.ReadMessage()
        if err != nil { log.Println('read err', err); break }
        log.Println('recv', string(msg))
        // echo back
        err = conn.WriteMessage(msgType, []byte(fmt.Sprintf('echo: %s', string(msg))))
        if err != nil { log.Println('write err', err); break }
    }
}

func main(){
    http.HandleFunc('/ws', wsHandler)
    log.Println('ws server listening :6000')
    srv := &http.Server{Addr: ':6000', ReadTimeout: 10*time.Second, WriteTimeout: 10*time.Second}
    log.Fatal(srv.ListenAndServe())
}
