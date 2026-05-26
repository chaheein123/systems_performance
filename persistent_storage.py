from enum import Enum

ram = [None] * 10
page_length = 100
pages_per_block = 8

class Kernel:
    def __init__(self, diskcontroller):
        self.diskcontroller = diskcontroller

class SsdController:
    def __init__(self, ssd):
        self.ssd = ssd

class Ssd:
    def __init__(self):
        self.plane = [Block(i) for i in range(page_length)]
        self.lba = {}

class Block:
    class _BLOCKTYPE(Enum):
        INODE = 1
        FAT = 2
        DATA = 3

    def __init__(self, block_id, pages_per_block=8):
        self.block_id = block_id
        self.pages = [Page(i) for i in range(pages_per_block)]
        self.is_empty = True

class Page:
    def __init__(self, page_id):
        self.page_id = page_id
        # Supposed to be 4096 bytes
        self.data_length = page_length
        self.data = ""
        self.is_empty = True
    
    def __str__(self):
        return (f"Page {self.page_id}")

class SubmissionQueueEntry:
    def __init__(self, cid, opcode, slba, data, block_count=1):
        self.cid = cid       # Command Identifier
        self.opcode = opcode # e.g., "WRITE" or "READ"
        self.slba = slba     # Starting LBA
        self.data = data     # Data Pointer (RAM location)
        self.block_count = block_count

class CompletionQueueEntry:
    def __init__(self, cid, status="SUCCESS"):
        self.cid = cid       # Matches the Submission packet's CID
        self.status = status # "SUCCESS", "ERROR_BAD_LBA", etc.



class DeviceDriver:

    def __init__(self, ssd_controller):
        self.ssd_controller = ssd_controller
        self.submission_queue = []
        self.completion_queue = []

    def translate_to_bin():
        pass

    def write_to_submission_queue():
        pass

    def read_from_completion_queue():
        pass

    def ring_door_bell():
        pass

    


# Flow: User space -> VFS layer -> FS -> block device -> device driver -> hardware (SSD controller flashes the silicon)


# my_ssd = Ssd()
# my_diskcontroller = DiskController(my_ssd)
# my_kernel = Kernel(my_diskcontroller)


# my_kernel.create_file("a.txt", "EXT")
# my_kernel.write_file("a.txt", "Hello world!")



