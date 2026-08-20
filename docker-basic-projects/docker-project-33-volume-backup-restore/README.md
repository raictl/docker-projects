Project 33: Backup and Restore a Docker Volume

Goal

Create a Docker volume, store application data in it, back it up to a .tar.gz file, delete the volume, and then restore the data into a new volume.

Step 1: Build the image

  #docker build -t volume-backup-demo:v1 .

Step 2: Create a Docker volume

  #docker volume create backup-data

  Verify:
  #docker volume ls

Step 3: Start a container using the volume

  #docker run -d \
  --name backup-source \
  -v backup-data:/data \
  volume-backup-demo:v1

Step 4: Add some application data

  Create multiple files:
  #docker exec backup-source sh -c 'echo "Application configuration" > /data/config.txt'

  #docker exec backup-source sh -c 'echo "Customer data" > /data/customers.txt'

  #docker exec backup-source sh -c 'echo "Database backup information" > /data/database.txt'

Step 5: Verify the volume data

  #docker exec backup-source ls -l /data

  Then:

  #docker exec backup-source cat /data/config.txt

  You should see:

  Application configuration

Step 6: Create the volume backup

  #docker run --rm \
  -v backup-data:/data:ro \
  -v "$(pwd)/backup:/backup" \
  alpine:3.22 \
  tar czf /backup/backup-data.tar.gz -C /data .

Step 7: Verify the backup

  #ls -lh backup/

  you should see:

  backup-data.tar.gz

  Verify the archive:

  #tar -tzf backup/backup-data.tar.gz

  You should see files such as:

 ./
./info.txt
./config.txt
./customers.txt
./database.txt

Step 8: Remove the source container

  #docker stop backup-source
  #docker rm backup-source

Step 9: Remove the original volume

  #docker volume rm backup-data

  Verify:

  #docker volume ls
  backup-data should no longer exist.

Step 10: Create a new volume

  #docker volume create restored-data

Step 11: Restore the backup

  #docker run --rm \
  -v restored-data:/data \
  -v "$(pwd)/backup:/backup:ro" \
  alpine:3.22 \
  tar xzf /backup/backup-data.tar.gz -C /data

Step 12: Verify restored data

  Start a new container:

  #docker run -d \
  --name restored-container \
  -v restored-data:/data \
  alpine:3.22 \
  tail -f /dev/null

  Check:

  #docker exec restored-container ls -l /data

  You should see:

info.txt
config.txt
customers.txt
database.txt

Step 13: Verify individual files

  #docker exec restored-container cat /data/config.txt

  Expected:

Application configuration

  Check another file:

  #docker exec restored-container cat /data/customers.txt

  Expected:

Customer data

Step 14: Cleanup

  #docker stop restored-container
  #docker rm restored-container


