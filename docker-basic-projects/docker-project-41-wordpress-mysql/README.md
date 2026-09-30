Project 41: WordPress + MySQL Using Docker CLI

Goal:

Run a basic WordPress + MySQL application using only Docker CLI.

Architecture:

Browser
   ↓
WordPress Container
   ↓
MySQL Container

We will:

Create a Docker network
Run MySQL
Run WordPress
Connect WordPress to MySQL using the container name
Verify the application
Check the database connection

1. Directory Structure

At this stage:

project-41-wordpress-mysql/
└── README.md

This project does not require custom Dockerfiles because we will use the official images directly.

2. Create Docker Network

docker network create wordpress-net

Verify:

docker network ls

You should see:

wordpress-net

3. Start MySQL

Run:

docker run -d \
  --name wordpress-db \
  --network wordpress-net \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=wordpress \
  -e MYSQL_USER=wordpress \
  -e MYSQL_PASSWORD=wordpresspassword \
  mysql:8.4

Verify:

docker ps

You should see:

wordpress-db

4. Wait for MySQL

MySQL needs time to initialize.

Check:

docker logs wordpress-db

Wait until MySQL reports that it is ready to accept connections.

You can also test:

docker exec wordpress-db \
  mysqladmin ping \
  -uwordpress \
  -pwordpresspassword

Expected:

mysqld is alive

5. Start WordPress

Now start WordPress:

docker run -d \
  --name wordpress \
  --network wordpress-net \
  -p 8080:80 \
  -e WORDPRESS_DB_HOST=wordpress-db:3306 \
  -e WORDPRESS_DB_USER=wordpress \
  -e WORDPRESS_DB_PASSWORD=wordpresspassword \
  -e WORDPRESS_DB_NAME=wordpress \
  wordpress:latest

Verify:

docker ps

You should have:

wordpress

wordpress-db

running.

6. Check WordPress Logs

docker logs wordpress

If WordPress is still starting, wait a little and check again:

docker logs wordpress

7. Open WordPress

Open this in your browser:

http://localhost:8080

You should see the WordPress installation page.

Follow the WordPress setup:

Select language.
Enter a site title.
Create an administrator username.
Set an administrator password.
Enter an email address.
Complete the installation.

You do not need to expose MySQL port 3306 to your host.

18. Verify WordPress → MySQL Communication

Check the WordPress environment:

docker exec wordpress env | grep WORDPRESS_DB

You should see:

WORDPRESS_DB_HOST=wordpress-db:3306
WORDPRESS_DB_USER=wordpress
WORDPRESS_DB_PASSWORD=wordpresspassword
WORDPRESS_DB_NAME=wordpress

The important value is:

WORDPRESS_DB_HOST=wordpress-db:3306

wordpress-db is the MySQL container name.

9. Verify Docker DNS

Check whether WordPress can resolve the MySQL container:

docker exec wordpress getent hosts wordpress-db

Expected output will contain an IP address similar to:

172.18.0.2    wordpress-db

This confirms Docker's internal DNS is resolving:

wordpress → wordpress-db

10. Verify MySQL Database

Enter MySQL:

docker exec -it wordpress-db \
  mysql \
  -uwordpress \
  -pwordpresspassword \
  wordpress

Inside MySQL:

SHOW TABLES;

After completing the WordPress installation, you should see several WordPress tables, such as:

wp_options
wp_posts
wp_users
wp_comments
...

Check WordPress users:

SELECT ID, user_login FROM wp_users;

Exit:

exit

11. Verify Containers Are on the Same Network

Run:

docker network inspect wordpress-net

Look for:

wordpress
wordpress-db

Both containers must appear under the network's Containers section.

12. Verify MySQL Is Not Exposed

Run:

docker ps

WordPress should have:

0.0.0.0:8080->80/tcp

But MySQL should not have:

0.0.0.0:3306->3306/tcp

This means:

Browser
   ↓
Host:8080
   ↓
WordPress
   ↓
Docker Network
   ↓
MySQL:3306

MySQL is only reachable through the Docker network.

13. Test MySQL Failure

This is an important troubleshooting exercise.

Stop MySQL:

docker stop wordpress-db

Now refresh:

http://localhost:8080

WordPress should no longer be able to communicate with MySQL.

Check WordPress logs:

docker logs wordpress

You should see database connection-related errors if WordPress attempts a new database connection.

14. Start MySQL Again

docker start wordpress-db

Wait for MySQL:

docker exec wordpress-db \
  mysqladmin ping \
  -uwordpress \
  -pwordpresspassword

Expected:

mysqld is alive

Refresh:

http://localhost:8080

WordPress should become available again.

15. Inspect WordPress Container

docker inspect wordpress

Useful information includes:

Container IP
Network
Environment variables
Port mapping
Image
Mounts

For a shorter network-focused view:

docker inspect wordpress \
  --format '{{json .NetworkSettings.Networks}}'
16. Check WordPress Logs

docker logs wordpress

Follow logs:

docker logs -f wordpress

Press:

Ctrl+C

to stop following the logs.

17. Check MySQL Logs

docker logs wordpress-db

18. Cleanup

Because WordPress and MySQL are stateful applications, remove the containers and network after completing the lab.

Stop:

docker stop wordpress wordpress-db

Remove:

docker rm wordpress wordpress-db

Remove network:

docker network rm wordpress-net
Optional: Remove Downloaded Images

Only if you want to clean the images too:

docker rmi wordpress:latest
docker rmi mysql:8.4

Check:

docker images
