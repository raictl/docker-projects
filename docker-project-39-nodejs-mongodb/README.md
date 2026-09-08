Project 39: Connect Node.js + MongoDB

Goal

Build a simple Node.js + MongoDB application using only Docker CLI.

Architecture:

Client
   ↓
Node.js Container
   ↓
MongoDB Container

The Node.js application will:

Connect to MongoDB
Insert a document
Read documents
Verify the database connection

1. Build Node.js Image

From the project directory:

#docker build -t nodejs-mongodb-app:1.0 .

Verify:

#docker images nodejs-mongodb-app

2. Create Docker Network

#docker network create node-mongodb-net

Verify:

#docker network ls

3. Start MongoDB Container

#docker run -d \
  --name mongodb \
  --network node-mongodb-net \
  mongo:8

Verify:

#docker ps

You should see:

mongodb

4. Verify MongoDB

Check MongoDB logs:

#docker logs mongodb

Wait until MongoDB is ready.

You can also test it directly:

#docker exec mongodb mongosh --eval "db.adminCommand({ ping: 1 })"

You should see a successful ping response.

5. Start Node.js Container

#docker run -d \
  --name nodejs \
  --network node-mongodb-net \
  -p 8080:3000 \
  -e MONGO_HOST=mongodb \
  nodejs-mongodb-app:1.0

Check:

#docker ps

You should have:

nodejs
mongodb

running.

6. Check Node.js Logs

#docker logs nodejs

You should see:

Connected to MongoDB

Node.js application running on port 3000

7. Test Node.js Application

#curl http://localhost:8080

Expected:

Hello from Node.js + MongoDB!

8. Test MongoDB Health

#curl http://localhost:8080/health

Expected:

Node.js and MongoDB are healthy!

This confirms:

Node.js → MongoDB

communication is working.

9. Insert Data into MongoDB

Run:

#curl http://localhost:8080/add

You should receive something similar to:

Document inserted: 68xxxxxxxxxxxxxxxxxxxx

Run it again:

#curl http://localhost:8080/add

Now you have multiple documents.

10. Read Data from MongoDB

Run:

#curl http://localhost:8080/users

Expected output will look similar to:

[
  {
    "_id": "...",
    "name": "Docker User",
    "role": "DevOps Engineer"
  },
  {
    "_id": "...",
    "name": "Docker User",
    "role": "DevOps Engineer"
  }
]

11. Verify Data Directly in MongoDB

Enter MongoDB:

d#ocker exec -it mongodb mongosh

Inside mongosh:

#show dbs

Then:

#use dockerdb

Check collections:

show collections

You should see:

users

Query the data:

db.users.find()

You should see the documents inserted through the Node.js application.

Exit:

exit

12. Verify Docker DNS

Node.js connects to:

mongodb:27017

Verify that the Node.js container can resolve MongoDB:

#docker exec nodejs getent hosts mongodb

You should get an IP address similar to:

172.18.0.2    mongodb

13. Inspect the Docker Network

#docker network inspect node-mongodb-net

You should see both:

nodejs
mongodb

connected to the same network.
20.


 Test MongoDB Failure

Stop MongoDB:

#docker stop mongodb

Now:

curl http://localhost:8080/health

The health request should fail because MongoDB is unavailable.

Start MongoDB again:

docker start mongodb

Wait a few seconds, then:

curl http://localhost:8080/health

Expected:

Node.js and MongoDB are healthy!

21. Cleanup

Stop containers:

#docker stop nodejs mongodb

Remove containers:

#docker rm nodejs mongodb

Remove network:

#docker network rm node-mongodb-net

Remove image:

#docker rmi nodejs-mongodb-app:1.0


