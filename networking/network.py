from data import *

# This is a mapping of mac address to the object
server_registry = {}

class NetworkSwitch:
    def __init__(self):
        self.mac_address_table = {
            0: None,
            1: None,
            2: None,
            3: None,
        }
    def connect_device(self, device):
        for i in range(len(self.mac_address_table)):
            if self.mac_address_table[i] is None:
                self.mac_address_table[i] = device
                return
        print("No available ports to connect the device.")
    
    def broadcast_arp_request(self, ip_address):
        for i in range(len(self.mac_address_table)):
            if self.mac_address_table[i] is not None and self.mac_address_table[i].ip_address == ip_address:
                return self.mac_address_table[i].mac_address

class NetworkDevice:
    def __init__(self, mac_address, ip_address, device):
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.nat_translation_table = {}
        self.routing_table = {}
        server_registry[mac_address] = device

    # Homework
    # Routers first look at the packet and checks its destination ip and uses the routing table to determine the next hop router.
    # NAT table is to rewrite the source IP to router's public ip (this happens only once when the packet leaves the private network)
    # Routing table is used to map ip subnets to a next hop router ip 
    def process_data_frame(self, data_frame, network_type):
        data_frame.source_mac = self.mac_address
        if network_type == "LAN":
            data_packet = data_frame.data_packet
            data_packet.source_ip = 
        

        elif network_type == "WAN":
            pass
        # Process the data frame and extract the data packet
        
        # Process the data packet and extract the data segment
        # data_segment = data_packet.data_segment
        # Process the data segment and extract the data
        # data_data = data_segment.data_data


class NetworkRouter(NetworkDevice):
    def __init__(self, mac_address, ip_address):
        super().__init__(mac_address, ip_address, self)


class NetworkServer(NetworkDevice):
    def __init__(self, network_router, ip_address, mac_address):
        self.network_router = network_router
        self.local_arp_cache = {}
        super().__init__(mac_address, ip_address, self)

        # network_switch.connect_device(self.mac_address)

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

        destination_mac = self.retrieve_dest_mac_address(destination_ip)

        data_frame = self.create_data_frame(
            data_packet = data_packet,
            source_mac = self.mac_address,
            destination_mac = destination_mac
        )

        server_registry["destination_mac"].process_data_frame(data_frame, "LAN")

        

        print("This is the destination mac", destination_mac)

    def retrieve_dest_mac_address(self, destination_ip):
        if destination_ip in self.local_arp_cache: return self.local_arp_cache[destination_ip]
        return self.send_arp_req(destination_ip)

    def send_arp_req(self, destination_ip):
        if "192.168." in destination_ip:
            return self.network_switch.broadcast_arp_request(destination_ip)
        else:
            return self.network_router.mac_address
            


    
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


network_router = NetworkRouter("C0:25:E9:37:97:EE")
network_switch = NetworkSwitch()
some_other_server = NetworkServer(network_router, "192.168.1.101", "00:1A:2B:3C:4D:5E")
network_server = NetworkServer(network_router, "192.168.1.100", "1A:1A:2B:3C:4D:5E")
network_switch.connect_device(network_server)
network_server.send_http_request(
    metadata="HTTP/1.1 200 OK\nContent-Type: application/json; charset=utf-8\nContent-Length: 85\nServer: nginx/1.25.3",
    data={"id": 180, "username": "devops_engineer", "status": "active", "location": "California"},
    source_port=8080,
    destination_port=80,
    destination_ip="142.250.190.46"

)

print(network_switch.mac_address_table[0].mac_address)
print(server_registry)
