import json

import dns.v1.dns_pb2 as dns_pb2


def get_root_nameservers_db():
    root_nameservers = []
    with open("root_nameserver_db.json", "r") as file:
        data = json.load(file)

        for nameserver in data["root_nameservers"]:
            root_nameserver = dns_pb2.RootNameserver(
                id=nameserver["id"],
                name=nameserver["name"],
                address=nameserver["address"],
            )
            root_nameservers.append(root_nameserver)
    return root_nameservers
