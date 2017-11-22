1.Create a Docker network so that each container can connect to the host under the fixed IP 192.168.0.1.
docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 dockernet

2.run command to start up the server:
docker run -p 3000:3000 -it --rm --name server -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 server.py

3.run command to start up the follower 
docker run -it --rm --name follower -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 client1.py 192.168.0.1

4.run command to insert data into server, follower would also be updated:
docker run -it --rm --name client -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 client.py 192.168.0.1
