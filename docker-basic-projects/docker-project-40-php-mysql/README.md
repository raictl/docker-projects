Project 41: Connect PHP + MySQL

Goal

Build a simple PHP + MySQL application using only Docker CLI.

Architecture:

Client
   ↓
PHP Container
   ↓
MySQL Container

The PHP application will:

Connect to MySQL
Create a database table
Insert data
Display stored data
Provide a health check




1. Build PHP Image
exit

2. Verify Container-to-Container DNS

The PHP container connects to:

mysql:3306

Check DNS:

docker exec php getent hosts mysql

You should receive the IP address of the MySQL container.

This confirms Docker's internal DNS is working.

3. Verify MySQL Port Is Not Published

Run:

docker ps

You should see PHP with:

0.0.0.0:8080->80/tcp

But MySQL should not have:

0.0.0.0:3306->3306/tcp

MySQL is therefore accessible to the PHP container through the Docker network but isn't exposed directly on the host.

4. Test MySQL Failure

Stop MySQL:

docker stop mysql

Test:

curl http://localhost:8080

The PHP application should report a MySQL connection error.

Start MySQL again:

docker start mysql

Wait for MySQL to become ready:

docker exec mysql mysqladmin ping \
  -uappuser \
  -papppassword

Expected:

mysqld is alive

Now test:

curl http://localhost:8080

The application should work again.

5. Check Logs

PHP container:

docker logs php

MySQL container:

docker logs mysql

6. Inspect Docker Network

docker network inspect php-mysql-net

You should see:

php
mysql

connected to the same network.

7. Cleanup

Stop containers:

docker stop php mysql

Remove containers:

docker rm php mysql

Remove network:

docker network rm php-mysql-net

Remove application image:

docker rmi php-mysql-app:1.0
