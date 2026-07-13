from data import *
class NetworkRouter:
    def __init__(self):
        # self.routing_table = {}
        # self.mac_table = {}
        # self.ip_table = {}
        self.nat_translation_table = {}
        self.routing_table = {}

class NetworkServer:
    def __init__(self, ip_address, mac_address):
        self.ip_address = ip_address
        self.mac_address = mac_address

    def send_http_request(self, metadata, data, source_port, destination_port, destination_ip):
        data_segment = self.create_data_segment(
            metadata="HTTP/1.1 200 OK\nContent-Type: application/json; charset=utf-8\nContent-Length: 85\nServer: nginx/1.25.3",
            data={"id": 180, "username": "devops_engineer", "status": "active", "location": "California"},
            source_port=source_port,
            destination_port=destination_port
        )
        data_packet = self.create_data_packet(
            data_segment=data_segment,
            source_ip=self.ip_address,
            destination_ip=destination_ip,
            protocol="TCP"
        )
        # Homework. Figure out how to find the destination mac address given the destination ip address. You can use ARP protocol to find the mac address of the destination ip address.
        # data_frame = self.create_data_frame(
        #     data_packet=data_packet,
        #     source_mac=self.mac_address,
        #     destination_mac="00:1B:2C:3D:4E:5F"
        # )
    
    def create_data_frame(self, data_packet, source_mac, destination_mac):
        return DataFrame(
            data_packet=data_packet,
            source_mac=source_mac,
            destination_mac=destination_mac
        )


    def create_data_segment(self, metadata, data, source_port, destination_port):
        data_data = DataData(
            metadata=metadata,
            data=data
        )
        return DataSegment(
            data_data=data_data,
            source_port=source_port,
            destination_port=destination_port
        )
    
    def create_data_packet(self, data_segment, source_ip, destination_ip, protocol):
        return DataPacket(
            data_segment=data_segment,
            source_ip=source_ip,
            destination_ip=destination_ip,
            protocol=protocol
        )

    
network_server = NetworkServer("192.168.1.100", "00:1A:2B:3C:4D:5E")
network_server.send_http_request(
    metadata="HTTP/1.1 200 OK\nContent-Type: application/json; charset=utf-8\nContent-Length: 85\nServer: nginx/1.25.3",
    data={"id": 180, "username": "devops_engineer", "status": "active", "location": "California"},
    source_port=8080,
    destination_port=80,
    destination_ip="142.250.190.46"

)
print(network_server.ip_address)