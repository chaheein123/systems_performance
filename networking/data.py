# Design a system where different classes are: router, your own laptop, other company servers
# a data packet will be passed from each object and encasulate/decasulate the data packets.


class DataData:
    # Application Data (Layer 7)
    def __init__(self, metadata, data):
        # metadata looks like: 
        # HTTP/1.1 200 OK
        # Content-Type: application/json; charset=utf-8
        # Content-Length: 85
        # Server: nginx/1.25.3

        # data looks like:
        # {
        #     "id": 180,
        #     "username": "devops_engineer",
        #     "status": "active",
        #     "location": "California"
        # }
        self.metadata = metadata
        self.data = data

class DataSegment:
    # TCP segment (Layer 4)
    # Create tcp header and add application data = segment
    def __init__(self, data_data, source_port, destination_port):
        self.data_data = data_data
        self.source_port = source_port
        self.destination_port = destination_port


class DataPacket:
    def __init__(self, data_segment, source_ip, destination_ip, protocol):
        self.data_segment = data_segment
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.protocol = protocol

class DataFrame:
    def __init__(self, data_packet, source_mac, destination_mac):
        self.data_packet = data_packet
        self.source_mac = source_mac
        self.destination_mac = destination_mac

