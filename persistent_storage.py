from enum import Enum
import yaml
import threading
import time

ram = [0] * 1000
page_length = 100
# There will only be 25 pages used for lba's, while there will be 100 pages (total_pages)
lba_length = 25
total_pages = 100
block_num = 10
pages_per_block = 8

submission_queue = []
completion_queue = []

# inodes
# {
#     "inode_number": 12,
#     "file_mode": 0o100644,       # Standard file permissions (-rw-r--r--)
#     "uid": 1000,                 # Owner ID (user)
#     "file_size_bytes": 145820,   # Size of the file
#     "block_pointers": [500]      # <--- BINGO! The data lives at LBA 500
# }

# data
# The data itself looks like a pure string

class VFS:
    def __init__(self):
        pass
    def read_file(self):
        pass


class FileSystemDriver:
    def __init__(self, block_device):
        self.block_device = block_device
        # You NEED To distinguish between reading and writing in the FS driver because if you're writing, you need to look at the block bit map. But if you're reading, you don't need the block bit map
        # FS driver uses the inode table + bloc bit map to find the data. Also, for the kernel, block bit map is actually just lba's. 
        # raw_inode_table = self.get_metadata(self.super_block_lba)
        # self.io_request_queue = []
        # raw_inode_table = self.block_device.()
        self.inode_table = {}

        self.fs_metadata = self.get_fs_metadata()
        self.block_bit_map = self.fs_metadata["block_bitmap_start_lba"]
        self.inode_table = self.fs_metadata["inode_table_start_lba"]
        print("This is the block bit map", self.block_bit_map)
        print("This is the inode table", self.inode_table)

        # self.inode_table = self.read_data([inode_table_start_lba])


        # self.block_bit_map = self.ssd_controller.request_block_bit_map()
        # Super block is only a metadata. It contains the lba's for the real data for the block bit map AND the inode table

    def read_file(self, filename):
        lbas = self.inode_table[filename]["assigned_lbas"]
        data_index = self.read_data(lbas)
        data = ""
        for i in data_index:
            data += ram[i]
        return data

    def read_data(self, lbas):
        mem_locations = []
        for lba in lbas:
            memory_location = None
            for i in range(len(ram)):
                if ram[i] == 0:
                    ram[i] = 1
                    memory_location = i
                    mem_locations.append(i)
                    break
            self.block_device.submit_io_request_queue(lba, "READ", memory_location)
        return mem_locations
    
    def get_fs_metadata(self):
        # print(ram)
        super_block_lba = 0
        mem_locations = self.read_data([super_block_lba])
        print("mem_locations", mem_locations)
        print(ram)
        data = ""
        for i in mem_locations:
            print("hi", ram[i])
            data += ram[i]

        print("raw_data", data)
        
        return yaml.safe_load(data)

    def write_data(self, lba, data):
        # Figure out from the bit block map, the available lba to write the data. It must first figure out the length of the data, and how many lba's needed and then find which lba's are available.
        self.block_device.submit_io_request_queue("WRITE", data)


class BlockDevice:
    # fs -> block device layer -> device driver -> ssd controller -> ssd
    # Block device is responsible for page cache and request merging
    def __init__(self, device_driver):
        self.device_driver = device_driver
        self.io_request_queue = []
        self.queue_lock = threading.Lock()
        self.worker_thread = threading.Thread(target=self._background_loop, daemon=True)
        self.worker_thread.start()

        # device_driver.submit_io("READ", 2, "", 1)
    
    def _background_loop(self):
        """ This runs completely asynchronously in the background forever """
        while True:
            time.sleep(0.1) # Wake up every 5 milliseconds (our simulated timer)
            
            # Acquire the lock to safely check and process the queue
            with self.queue_lock:
                if len(self.io_request_queue) > 0:
                    print("\n[Timer] Background thread woke up! Flushing queue...")
                    self.merge_request()
    
    def submit_io_request_queue(self, lba, opcode, data):
        with self.queue_lock:
            self.io_request_queue.append(
                {"opcode": opcode, "lba": lba, "data": data}
            )

    def merge_request(self):

        # This function will be run by the FS driver every 3 seconds. It will gather every io_request in the io_request_queue
        # Homework
        # Make sure that the opcode are the same as well for homework
        # def submit_io(self, opcode, lba, data_payload, num_blocks=1):
        self.io_request_queue.sort(key=lambda req: (req["opcode"], req["lba"]))
        # while len(self.io_request_queue):
        current_stack = []
        while len(self.io_request_queue) > 0:
            r = self.io_request_queue.pop(0)
            if len(current_stack) == 0 or ((current_stack[-1]["lba"] == r["lba"] - 1) and ):
                current_stack.append(r)
            else:
                self.device_driver.submit_io()
                current_stack = []

                pass
            # r = self.io_request_queue.pop(0)
            current_stack.append(r)





        # for i in range(len(self.io_request_queue) - 1):
        #     if self.io_request_queue[i]["lba"] + 1 == self.io_request_queue[(i + 1)]["lba"]:

        #         pass


            

        
        # slba = 
        # block_count = 








        # self.device_driver.submit_io()
        pass

    

    



        
    
    



class Kernel:
    def __init__(self, ssd_controller):
        # self.ssd = ssd
        # fs -> block device layer -> device driver -> ssd controller -> ssd
        self.ssd_controller = ssd_controller
        self.device_driver = DeviceDriver(self.ssd_controller)
        self.block_device = BlockDevice(self.device_driver)
        self.fs_driver = FileSystemDriver(self.block_device)



        # self.block_bit_map = [0] * lba_length

        # self.block_bitmap = [1, 1, 0, 0, 0]

        # self.inode_table = {
        #     "/home/user/photo.jpg": {
        #         "size_bytes": 4096,
        #         "permissions": "rw-r--r--",
        #         "assigned_lbas": [0]  # The kernel maps the FILE to LBA 0
        #     }
        # }

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
        self.data = " " * page_length
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
    def __init__(self, ssd):
        self.ssd = ssd
        # self.flash_translation_layer = {}

        self.flash_translation_layer = {
            0: {
                "block": 0 // pages_per_block, 
                "page": 0 // pages_per_block
            }
        }

    def find_available_page(self, data_lba_mapping):
        if len(data_lba_mapping) == 0: return
        ftl_index = next(iter(data_lba_mapping))
        data = data_lba_mapping.pop(ftl_index)

        for i in range(len(self.ssd.plane)):
            for y in range(len(self.ssd.plane[i])):
                if self.ssd.plane[i][y].is_empty:
                    self.ssd.plane[i][y].is_empty = False
                    self.ssd.plane[i][y].data = data.ljust(page_length)
                    self.flash_translation_layer[ftl_index] = {
                        "block": i,
                        "page": y,
                    }
                    return self.find_available_page(data_lba_mapping)
        raise ValueError("The storage is full!")

    def ring_door_bell(self):
        # Check the SSD plane. Go through blocks and pages to find the available page. Save the data and update the FTL
        while len(submission_queue):

            sqe = submission_queue.pop(0)
            
            if sqe.opcode == "WRITE":
                searching_lba = []
                for i in range(sqe.block_count):
                    lba_index = sqe.slba + i
                    if lba_index in self.flash_translation_layer:
                        raise ValueError("The FTL already contains the index!")
                    searching_lba.append(lba_index)
                
                data_lba_mapping = {}
                beginning_index = 0
                for i in range(len(searching_lba)):
                    data_lba_mapping[searching_lba[i]] = sqe.data[beginning_index:beginning_index+100]
                    beginning_index += 100
            
                self.find_available_page(data_lba_mapping)

            elif sqe.opcode == "READ":                
                data = ""
                for i in range(sqe.block_count):
                    data += self.flash_translation_layer[sqe.slba + i]
                print("Reading the data...")
                print(data)
                # return data

class Ssd:
    def __init__(self):
        self.plane = [Block(i) for i in range(block_num)]
        self.plane[0].pages[0].data = "{block_bitmap_start_lba: 1, inode_table_start_lba: 2}".ljust(page_length)
        self.plane[0].pages[0].is_empty = False
        init_block_bit_map = [0] * lba_length
        init_block_bit_map[0:3] = [1, 1, 1]
        self.plane[0].pages[1].data = str(init_block_bit_map).ljust(page_length)
        self.plane[0].pages[1].is_empty = False
        self.plane[0].pages[2].data = "{}".ljust(page_length)
        self.plane[0].pages[2].is_empty = False

class DeviceDriver:

    def __init__(self, ssd_controller):
        self.ssd_controller = ssd_controller
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
        # block for the kernel, means its LBA. So block_count => lba count
        sqe = self.translate_to_bin(
            cid=assigned_cid, 
            opcode=opcode,
            slba=lba, 
            data=data_payload, 
            block_count=num_blocks
        )
        
        print(f"[Driver] Block Device handed off request. Packaged SQE (CID: {assigned_cid})")
        
        # 3. Call your queue helper to drop it in the list and poke the hardware
        # self.write_to_submission_queue(sqe)


    def translate_to_bin(self, cid, opcode, slba, data, block_count=1):
        # Your excellent translator method
        submission_queue_entry = SubmissionQueueEntry(cid, opcode, slba, data, block_count)
        return submission_queue_entry

    def write_to_submission_queue(self, submission_queue_entry):
        # Your excellent queue management method
        submission_queue.append(submission_queue_entry)
        print(f"[Driver] Appended SQE (CID: {submission_queue_entry.cid}) to SQ. Ringing Doorbell...")
        
        self.ssd_controller.ring_door_bell()



# Flow: User space -> VFS layer -> FS -> block device -> device driver -> hardware (SSD controller flashes the silicon)


my_ssd = Ssd()
my_ssd_controller = SsdController(my_ssd)

my_kernel = Kernel(my_ssd_controller)

# my_device_driver = DeviceDriver(my_ssd_controller, my_kernel)
# my_fs_driver = FileSystemDriver(my_ssd_controller, my_device_driver)


# my_kernel.create_file("a.txt", "EXT")
# my_kernel.write_file("a.txt", "Hello world!")

# my_kernel.bootup()
# my_kernel.create_file("a.txt", "EXT") -> vfs.create_file (VFS) -> fs -> block device -> device driver
