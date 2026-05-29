from enum import Enum

ram = [None] * 10
page_length = 100
block_num = 10
pages_per_block = 8

class Kernel:
    def __init__(self, diskcontroller):
        self.diskcontroller = diskcontroller
        self.submission_queue = []
        self.completion_queue = []

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

class SsdController:
    def __init__(self, ssd, kernel):
        self.ssd = ssd
        self.kernel = kernel
        self.flash_translation_layer = {}

        # self.flash_translation_layer = {
        #     0: {
        #         "block": 0 // pages_per_block, 
        #         "page": 0 // pages_per_block
        #     }
        # }

    def ring_door_bell(self):
        # Let's the controller know that there is a new submission in the queue
        while len(self.kernel.submission_queue):
            current_sqe = self.kernel.submission_queue.pop(0)
            self.process_sqe(current_sqe)

    def process_sqe(self, sqe):
        # Homework
        pass

class Ssd:
    def __init__(self):
        self.plane = [Block(i) for i in range(block_num)]
    

    

class DeviceDriver:

    def __init__(self, ssd_controller, kernel):
        self.ssd_controller = ssd_controller
        self.kernel = kernel
        # self.submission_queue = []
        # self.completion_queue = []
        self.next_cid = 0

    def submit_io(self, opcode, lba, data_payload, num_blocks=1):
        """
        THIS is the main method called by the Block Device Layer!
        It acts as the director, orchestrating your two helper functions.
        """
        # 1. Grab the next available tracking ID
        assigned_cid = self.next_cid
        self.next_cid += 1  # Increment it for the next run
        
        # 2. Call your translator helper to package the variables into an SQE
        sqe = self.translate_to_bin(
            cid=assigned_cid, 
            opcode=opcode, 
            slba=lba, 
            data=data_payload, 
            block_count=num_blocks
        )
        
        print(f"[Driver] Block Device handed off request. Packaged SQE (CID: {assigned_cid})")
        
        # 3. Call your queue helper to drop it in the list and poke the hardware
        self.write_to_submission_queue(sqe)


    def translate_to_bin(self, cid, opcode, slba, data, block_count=1):
        # Your excellent translator method
        submission_queue_entry = SubmissionQueueEntry(cid, opcode, slba, data, block_count)
        return submission_queue_entry

    def write_to_submission_queue(self, submission_queue_entry):
        # Your excellent queue management method
        self.kernel.submission_queue.append(submission_queue_entry)
        print(f"[Driver] Appended SQE (CID: {submission_queue_entry.cid}) to SQ. Ringing Doorbell...")
        
        # Ring the doorbell! (Note: watch out for the spelling 'ring_door_bell' vs 'ring_doorbell' 
        # based on how you name it in your SSDController class)
        self.ssd_controller.ring_door_bell()
    

    


# Flow: User space -> VFS layer -> FS -> block device -> device driver -> hardware (SSD controller flashes the silicon)


# my_ssd = Ssd()
# my_diskcontroller = DiskController(my_ssd)
# my_kernel = Kernel(my_diskcontroller)


# my_kernel.create_file("a.txt", "EXT")
# my_kernel.write_file("a.txt", "Hello world!")

# my_kernel.bootup()
# my_kernel.create_file("a.txt", "EXT") -> vfs.create_file (VFS) -> fs -> block device -> device driver
