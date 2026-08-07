const express = require("express");

const app = express();
const PORT = 3000;

app.get("/", (req, res) => {
    res.json({
        project: "Docker Project 18",
        message: "Welcome to Node.js REST API"
    });
});

app.get("/health", (req, res) => {
    res.json({
        status: "UP"
    });
});

app.get("/version", (req, res) => {
    res.json({
        version: "1.0.0"
    });
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server listening on port ${PORT}`);
});
