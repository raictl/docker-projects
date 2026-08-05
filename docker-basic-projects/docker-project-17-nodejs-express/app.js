const express = require("express");

const app = express();

const PORT = 3000;

app.get("/", (req, res) => {
    res.send("<h1>Docker Project 17</h1><h2>Hello from Node.js Express!</h2>");
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on port ${PORT}`);
});
