'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import datastore_pb2
import argparse
import time
import rocksdb

PORT = 3000

class DatastoreClient():
    
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)
        self.db = rocksdb.DB("follower1.db", rocksdb.Options(create_if_missing=True))

    def put(self, value):
        return self.stub.put(datastore_pb2.Request(data=value))

    def get(self, key):
        return self.stub.get(datastore_pb2.Request(data=key))

    def update(self):
        msg = ""
        resp = self.stub.update(datastore_pb2.Request(data=""))
        if resp.data != "": #if there's a update from master DB, store in local DB
            pair = resp.data.split(":")
            key = pair[0]
            value = pair[1]
            self.db.put(bytes(key, encoding='utf-8'), bytes(value, encoding='utf-8'))
            msg = key + ":" + value + " stored in client DB"
        return msg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="display a square of a given number")
    args = parser.parse_args()
    print("Client is connecting to Server at {}:{}...".format(args.host, PORT))
    client = DatastoreClient(host=args.host)
    try:
        print("Client listening to server")
        while True:
            msg = client.update()
            if msg != "":
                print(msg)
            time.sleep(3) #delay for 3 secs
    except KeyboardInterrupt:
       print("Client Stopped") 

if __name__ == "__main__":
    main()

