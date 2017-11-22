'''
################################## server.py #############################
# Lab1 gRPC RocksDB Server 
################################## server.py #############################
'''
import time
import grpc
import datastore_pb2
import datastore_pb2_grpc
import uuid
import rocksdb

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyDatastoreServicer(datastore_pb2.DatastoreServicer):
    def __init__(self):
        self.db = rocksdb.DB("master.db", rocksdb.Options(create_if_missing=True))
        self.update_status = False #keep track of if there's an update
        self.update_content = "" #update content

    def update_status(some_function): #decorator to update status
        def wrapper(*args):
            self.update_status = True #new update
            return some_function(*args)
        return wrapper

    @update_status
    def put(self, request, context):
        print("put")
        key = uuid.uuid4().hex
        # TODO - save key and value into DB converting request.data string to utf-8 bytes 
        self.db.put(bytes(key, encoding='utf-8'), bytes(request.data, encoding='utf-8'))
        self.update_content = key + ":" + request.data #update content 
        return datastore_pb2.Response(data=key)

    def get(self, request, context):
        print("get")
        # TODO - retrieve the value from DB by the given key. Needs to convert request.data string to utf-8 bytes. 
        value = self.db.get(bytes(request.data, encoding='utf-8'))
        return datastore_pb2.Response(data=value)

    def update(self, request, context):
        if self.update_status == False:
            self.update_content = ""
        else:
            self.update_status = False #reset
        return datastore_pb2.Response(data=self.update_content)

def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    datastore_pb2_grpc.add_DatastoreServicer_to_server(MyDatastoreServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)
