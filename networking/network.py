from data import *

class NetworkRouter:
    def __init__(self, mac_address):
        # self.routing_table = {}
        # self.mac_table = {}
        # self.ip_table = {}
        self.mac_address = mac_address
        self.nat_translation_table = {}
        self.routing_table = {}

class NetworkSwitch:
    def __init__(self):
        # Homework
        # Fix this table so tthat the mapping is the index to the server object itself. not just the mac address. 
        self.mac_address_table = {
            0: None,
            1: None,
            2: None,
            3: None,
        }
    def connect_device(self, device_mac_address):
        for i in range(len(self.mac_address_table)):
            if self.mac_address_table[i] is None:
                self.mac_address_table[i] = device_mac_address
                return
        print("No available ports to connect the device.")
    
    def broadcast_arp_request(self, ip_address):
        for i in range(len(self.mac_address_table)):
            if self.mac_address_table[i] is not None:
                print(f"Broadcasting ARP request for IP {ip_address} to MAC {self.mac_address_table[i]} on port {i}")



class NetworkServer:
    def __init__(self, network_router, network_switch, ip_address, mac_address):
        self.network_router = network_router
        # self.network_switch = network_switch
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.local_arp_cache = {}
        network_switch.connect_device(self.mac_address)

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

        # Homework. Figure out how to find the destination mac address given the destination ip address. You can use ARP protocol to find the mac address of the destination ip address.
        # If the local arp cache has the destination mac then it will use that ip, if not then it will initiate arp broadcast

        # The kernel reads the Destination IP (142.250.190.46) and checks its internal Routing Table dictionary (ip route). It sees that Google is not on the local network, meaning the packet must be sent to the Default Gateway (your home router, 192.168.1.1).

        # The ARP Lookup: The computer realizes it needs the router's physical MAC address.

        # It checks its local ARP Cache ledger.

        # If it's a match: It grabs the MAC address.

        # If it's a miss: It pauses the data packet, shoots an ARP Broadcast (FF:FF:FF:FF:FF:FF) shouting across the room, gets the router's hardware MAC address (BB:BB:BB:BB:BB:BB), and caches it.



        # 
        # data_frame = self.create_data_frame(
        #     data_packet=data_packet,
        #     source_mac=self.mac_address,
        #     destination_mac="00:1B:2C:3D:4E:5F"
        # )
    def retrieve_dest_mac_address(self, destination_ip):
        if destination_ip in self.local_arp_cache: return self.local_arp_cache[destination_ip]
        return self.send_arp_req(destination_ip)

    def send_arp_req(self, destination_ip):
        if "192.168." in destination_ip:

            self.network_switch.
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


network_router = NetworkRouter()
network_switch = NetworkSwitch()
some_other_server = NetworkServer(network_router, network_switch, "192.168.1.101", "00:1A:2B:3C:4D:5E")
network_server = NetworkServer(network_router, network_switch, "192.168.1.100", "1A:1A:2B:3C:4D:5E")
# network_switch.connect_device(network_server.mac_address)
network_server.send_http_request(
    metadata="HTTP/1.1 200 OK\nContent-Type: application/json; charset=utf-8\nContent-Length: 85\nServer: nginx/1.25.3",
    data={"id": 180, "username": "devops_engineer", "status": "active", "location": "California"},
    source_port=8080,
    destination_port=80,
    destination_ip="142.250.190.46"

)
print(network_server.ip_address)
