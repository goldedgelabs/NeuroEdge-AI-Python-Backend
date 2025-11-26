// core/engineManager.go
package core

type Engine interface {
    Run(input map[string]interface{}) map[string]interface{}
}

var EngineManager = map[string]Engine{}

func RegisterEngine(name string, engine Engine) {
    EngineManager[name] = engine
}

func RunEngine(name string, input map[string]interface{}) map[string]interface{} {
    if eng, ok := EngineManager[name]; ok {
        return eng.Run(input)
    }
    return map[string]interface{}{"error": "engine not found"}
}
