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
    def __init__(self, data_data):
        self.data_data = data_data



class DataPacket:
    def __init__(self):
        pass

class DataFrame:
    def __init__(self):
        pass

class NetworkRouter:
    def __init__(self):
        pass

class NetworkServer:
    def __init__(self):
        pass

    def send_http_request(self):
        pass

    def create_data_data():
        pass

    def create_data_segment():
        pass
