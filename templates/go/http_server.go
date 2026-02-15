/*
 * HTTP Server
 * A simple HTTP server with routing and JSON responses.
 * Author: Jay Singh (iamjaysingh)
 * Run: go run main.go
 */

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"strings"
	"sync"
	"time"
)

// Task represents a todo item
type Task struct {
	ID        int       `json:"id"`
	Title     string    `json:"title"`
	Done      bool      `json:"done"`
	CreatedAt time.Time `json:"created_at"`
}

// Store holds our in-memory data
type Store struct {
	mu     sync.RWMutex
	tasks  map[int]Task
	nextID int
}

func NewStore() *Store {
	s := &Store{
		tasks:  make(map[int]Task),
		nextID: 1,
	}
	// Seed data
	s.Add("Learn Go")
	s.Add("Build HTTP Server")
	s.Add("Practice Concurrency")
	return s
}

func (s *Store) Add(title string) Task {
	s.mu.Lock()
	defer s.mu.Unlock()
	task := Task{
		ID:        s.nextID,
		Title:     title,
		Done:      false,
		CreatedAt: time.Now(),
	}
	s.tasks[s.nextID] = task
	s.nextID++
	return task
}

func (s *Store) GetAll() []Task {
	s.mu.RLock()
	defer s.mu.RUnlock()
	tasks := make([]Task, 0, len(s.tasks))
	for _, t := range s.tasks {
		tasks = append(tasks, t)
	}
	return tasks
}

func (s *Store) Toggle(id int) (Task, bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	task, ok := s.tasks[id]
	if !ok {
		return Task{}, false
	}
	task.Done = !task.Done
	s.tasks[id] = task
	return task, true
}

func (s *Store) Delete(id int) bool {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, ok := s.tasks[id]; !ok {
		return false
	}
	delete(s.tasks, id)
	return true
}

func (s *Store) Stats() map[string]int {
	s.mu.RLock()
	defer s.mu.RUnlock()
	total := len(s.tasks)
	done := 0
	for _, t := range s.tasks {
		if t.Done {
			done++
		}
	}
	return map[string]int{
		"total":   total,
		"done":    done,
		"pending": total - done,
	}
}

func writeJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}

func main() {
	store := NewStore()

	// Routes
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"message": "🚀 Go HTTP Server is running!",
			"routes": []string{
				"GET  /api/tasks    - List all tasks",
				"POST /api/tasks    - Add a task",
				"GET  /api/stats    - Get stats",
				"GET  /api/quote    - Random quote",
			},
			"author": "Jay Singh (iamjaysingh)",
		})
	})

	http.HandleFunc("/api/tasks", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case "GET":
			tasks := store.GetAll()
			writeJSON(w, http.StatusOK, map[string]interface{}{
				"count": len(tasks),
				"tasks": tasks,
			})
		case "POST":
			var body struct {
				Title string `json:"title"`
			}
			if err := json.NewDecoder(r.Body).Decode(&body); err != nil || body.Title == "" {
				writeJSON(w, http.StatusBadRequest, map[string]string{"error": "title is required"})
				return
			}
			task := store.Add(body.Title)
			writeJSON(w, http.StatusCreated, task)
		default:
			writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"error": "method not allowed"})
		}
	})

	http.HandleFunc("/api/stats", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, store.Stats())
	})

	http.HandleFunc("/api/quote", func(w http.ResponseWriter, r *http.Request) {
		quotes := []string{
			"Simplicity is the ultimate sophistication. — Leonardo da Vinci",
			"Code is like humor. When you have to explain it, it's bad. — Cory House",
			"First, solve the problem. Then, write the code. — John Johnson",
			"Make it work, make it right, make it fast. — Kent Beck",
			"Programs must be written for people to read. — Harold Abelson",
		}
		writeJSON(w, http.StatusOK, map[string]string{
			"quote": quotes[rand.Intn(len(quotes))],
		})
	})

	port := "8080"
	fmt.Println(strings.Repeat("=", 50))
	fmt.Println("  🚀 Go HTTP Server")
	fmt.Println(strings.Repeat("=", 50))
	fmt.Printf("  Listening on http://localhost:%s\n", port)
	fmt.Println(strings.Repeat("=", 50))

	log.Fatal(http.ListenAndServe(":"+port, nil))
}
