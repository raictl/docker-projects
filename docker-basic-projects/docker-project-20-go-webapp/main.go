package main

import (
	"fmt"
	"net/http"
)

func home(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "<h1>Docker Project 20</h1><h2>Hello from Go!</h2>")
}

func main() {
	http.HandleFunc("/", home)

	fmt.Println("Server started on port 8080")

	http.ListenAndServe(":8080", nil)
}
