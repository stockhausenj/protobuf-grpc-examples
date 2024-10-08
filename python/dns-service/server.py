import logging
from concurrent import futures

import grpc

import dns.v1.dns_pb2 as dns_pb2
import dns.v1.dns_pb2_grpc as dns_pb2_grpc
import root_nameserver_resources


def get_root_nameserver(root_nameserver_db, request):
    for root_nameserver in root_nameserver_db:
        if root_nameserver.id == request.id:
            return root_nameserver
    return None


class DnsServicer(dns_pb2_grpc.DnsServiceServicer):
    def __init__(self):
        self.db = root_nameserver_resources.get_root_nameservers_db()

    def GetRootNameserver(self, request, context):
        root_nameserver = get_root_nameserver(self.db, request)
        if root_nameserver is None:
            return dns_pb2.RootNameserver(name="")
        else:
            print("returning found")
            return root_nameserver


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dns_pb2_grpc.add_DnsServiceServicer_to_server(DnsServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
