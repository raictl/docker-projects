const express = require("express");
const { MongoClient } = require("mongodb");

const app = express();

const port = 3000;
const mongoHost = process.env.MONGO_HOST || "mongodb";

const mongoUrl = `mongodb://${mongoHost}:27017`;

const client = new MongoClient(mongoUrl);

let database;

async function connectToMongoDB() {
    await client.connect();

    database = client.db("dockerdb");

    console.log("Connected to MongoDB");
}

app.get("/", (req, res) => {
    res.send("Hello from Node.js + MongoDB!");
});

app.get("/health", async (req, res) => {
    try {
        await database.command({ ping: 1 });

        res.send("Node.js and MongoDB are healthy!");
    } catch (error) {
        res.status(500).send("MongoDB connection failed!");
    }
});

app.get("/add", async (req, res) => {
    const collection = database.collection("users");

    const result = await collection.insertOne({
        name: "Docker User",
        role: "DevOps Engineer"
    });

    res.send(`Document inserted: ${result.insertedId}`);
});

app.get("/users", async (req, res) => {
    const collection = database.collection("users");

    const users = await collection.find().toArray();

    res.json(users);
});

connectToMongoDB()
    .then(() => {
        app.listen(port, "0.0.0.0", () => {
            console.log(`Node.js application running on port ${port}`);
        });
    })
    .catch((error) => {
        console.error("MongoDB connection failed:", error);
        process.exit(1);
    });



