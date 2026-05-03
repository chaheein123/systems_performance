# LBA -> exposes the whole cylinder and expresses it as an array
# NAND -> uses page and block. Each LBA's map to a page
# You cannot use half a page. You're using a full page for anything. Minimum.
# Application, VFS, FS Driver, Device Driver (NVMe/SATA), Disk Controller, Inode
# Logical blocks maps to pages
# For example, if LBA 1 is mapped to page A. If you want to change a data on page A,
# then you need to use another page and then have the new data on the new page (B, in this case). And then have the LBA 1 mapped to Page B
# This mapping is done in DRAM cache. which is located right next to the ssd controller
# Erasing the data is expensive. So erasing the data only happens block-wide. As the pages become invalid and the whole block become invalid, then the block will be cleaned and available for data storage
# Process $\rightarrow$ VFS (Inode) $\rightarrow$ LBA $\rightarrow$ Page.
# LBA=4kib, page=4-16kib block=2-8mib
# fs block=2048, LBA=1024, PBA=4096
# fs block in a nutshell
# A. Data Blocks (The Content)
# This is what you expect. If you save a photo or a main.py file, the actual text and pixels are stored here.

# What's inside: The raw bytes of your files.

# B. Metadata Blocks (The "Data about the Data")
# This is the "Brain" of the filesystem. These blocks store the information required to find and manage your files. This includes:

# Inodes: These blocks store the file's size, permissions, owner, and timestamps (Modified/Created).

# Pointers/Extents: This is a "map" that says: "File 'notes.txt' is spread across LBA 100, 101, and 500."

# Directories: A directory is actually just a special "file" (stored in a block) that contains a list of filenames and their corresponding Inode numbers.

# Superblocks: These are the "Master" blocks at the very beginning of the partition that describe the entire filesystem (how many blocks total, how many are free, etc.).

# The Corrected FlowThe Directory Lookup: The Kernel looks at the folder and sees ian.txt $\rightarrow$ Inode #500.The Request (The "Correction"): The Kernel doesn't ask the SSD for a "Block Number." It translates that into an LBA first.Kernel thinks: "Inode #500 lives in FS Block #3 of the Inode Table."Kernel asks SSD: "Hey, give me LBA #200" (because the Kernel already knows that FS Block #3 maps to LBA #200).The SSD Delivery: The SSD finds LBA #200 (using its internal PBA map) and sends that 4KB chunk of data to the RAM.The RAM Discovery: The Kernel looks at that 4KB chunk in RAM and reads: "The actual data for ian.txt lives in LBA #300."The Final Fetch: The Kernel says: "SSD, now give me LBA #300."The Result: The SSD grabs the actual data from the physical silicon and sends it back.

# PartitionLBAs UsedFilesystem TypePartition 10 – 500,000FAT32 (Boot loader)Partition 2500,001 – 200,000,000Ext4 (Your Linux OS)Partition 3200,000,001 – EndXFS (Your Database/Data)

# FS Blocks #1-50 => Inode tables. FS blocks #51-5000 -> Data blocks. And inside each inode table, can have up to 16 inodes. 
# ohhhh I just understood something. So for ian.txt. if you want to read the file, the kernel gets the LBA from the Inode table, which has the information on which LBA from the DATA blocks. And from there the LBA from the DAta blocks knows where the data is on the pba. So the disk driver gives the data to the kernel and kernel loads into memory and thats how you see the memory?

# The "hi.txt" Data Journey
# 1. The Inode Hunt (Metadata)
# The Kernel needs the "ID Card" (Inode) for hi.txt. It knows the Inode Table lives at a specific set of addresses.

# The Kernel calculates the LBA for the FS Block that contains Inode #500.

# The Kernel asks the SSD: "Give me the data at LBA #200."

# The SSD sends back a 4KB FS Block.

# 2. Reading the Map (Inside RAM)
# The Kernel opens that 4KB block in your MacBook's RAM.

# The Kernel looks at Inode #500 and reads a specific piece of info: "The actual text for hi.txt is stored at LBA #300."

# 3. The Data Grab (The "Actually Data")
# Now the Kernel knows exactly where to go for the content.

# The Kernel asks the SSD: "Give me the data at LBA #300."

# The SSD Controller translates LBA #300 into a PBA (the physical silicon address).

# The SSD sends the actual "hi.txt" text back to the Kernel.

ram = [None] * 10

class Kernel:
    def __init__(self, diskcontroller):
        self.diskcontroller = diskcontroller
        self.partition_map = {
            "inode_table": {
                "beginning": 0,
                "end": 19
            },
            "data_block": {
                "beginning": 20,
                "end": 99
            }
        }

        self.file_mapping_lba = {
            "a.txt": 0,
            "b.txt": 1,
            "c.txt": 2,
            "d.txt": 3,
            "e.txt": 4,
            "f.txt": 5,
        }

    def read_file(self, file_name):
        lba_index = self.file_mapping_lba[file_name]
        return self.diskcontroller.get_data(lba_index)
    
class DiskController:
    def __init__(self, ssd):
        print("Hi I am the diskcontroller")
        self.ssd = ssd
    def get_data(self, lba_index):
        block_page_index = self.ssd.lba[lba_index]
        block_index = block_page_index["block"]
        page_index = block_page_index["page"]
        # print(self.ssd.plane[0])
        pages = next((item for item in self.ssd.plane if item.block_id == block_index), None).pages
        print(pages)


    
class Ssd:
    def __init__(self):
        self.plane = [Block(i) for i in range(100)]

        # lba's mapping is this: lba key -> PBA
        # self.lba = {1: {"block": 0, "page": 0}, 2: {"block": 0, "page": 1}, 3: {"block": 0, "page": 2}, 4: {"block": 0, "page": 3}}
        pages_per_block = 8
        total_lbas = 100

        # We use (i-1) because your keys start at 1, but hardware addresses start at 0
        self.lba = {
            i: {
                "block": i // pages_per_block, 
                "page": i % pages_per_block
            }
            for i in range(0, total_lbas + 1)
        }
    
    

class Block:
    def __init__(self, block_id, pages_per_block=8):
        self.block_id = block_id
        self.pages = [Page(i) for i in range(pages_per_block)]
        self.is_empty = True

class Page:
    def __init__(self, page_id):
        self.page_id = page_id
        # Supposed to be 4096 bytes
        self.data_length = 4
        self.data = "    "
        self.is_empty = True
    
    def __str__(self):
        return (f"Page {self.page_id}")

# class DiskController:
#     def __init__(self):
#         pass

# class Lba:
#     def __init__(self):
#         pass

# my_kernel = Kernel()
my_ssd = Ssd()
my_diskcontroller = DiskController(my_ssd)
my_kernel = Kernel(my_diskcontroller)

# Kernel finds out that a.txt is at LBA 0.  
my_kernel.read_file("a.txt")
# print(my_ssd.plane)


