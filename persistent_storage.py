# dram cache

from enum import Enum

ram = [None] * 10
lba_length = 100

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

        self.file_mapping_lba = {}
        self.block_bit_map = [0] * lba_length * 800
        # self.file_mapping_lba = {
        #     "a.txt": {"lba": 0, "fs_type": "EXT", "read": self.read_ext, "write": self.write_ext},
        #     "b.txt": {"lba": 1, "fs_type": "EXT", "read": self.read_ext, "write": self.write_ext},
        #     "c.txt": {"lba": 2, "fs_type": "EXT", "read": self.read_ext, "write": self.write_ext},
        #     "d.txt": {"lba": 3, "fs_type": "FAT", "read": self.read_ext, "write": self.write_ext},
        #     "e.txt": {"lba": 4, "fs_type": "EXT", "read": self.read_ext, "write": self.write_ext},
        #     "f.txt": {"lba": 5, "fs_type": "EXT", "read": self.read_ext, "write": self.write_ext},
        # }
    def create_file(self, file_name, fs_type):
        # Homework: Fix the create_file() function
        # This has to look through the self.block_bit_map first to find out the first occurence of 1 and then find the first occurence of 0 after that.
        # And then change the block bit map to 1 and then add the info to the self.file_mapping_lba.
        # In this lba, the disk controller needs to have the data on the ssd, such as "author:Ian Cha,permission:[read,write],uid:3,gid:32,blockpointers:[1]"

        if file_name not in self.file_mapping_lba:
            if len(self.file_mapping_lba) == 0:
                self.file_mapping_lba[file_name] = {"lba": 0}
            else:
                max_lba = max(info["lba"] for info in self.file_mapping_lba.values())
                self.file_mapping_lba[file_name] = {"lba": max_lba + 1}
            self.file_mapping_lba[file_name]["fs_type"] = fs_type
            if fs_type == "EXT":
                self.file_mapping_lba[file_name]["read"] = self.read_ext
                self.file_mapping_lba[file_name]["write"] = self.write_ext

                data = f"filename:{filename},author:Ian Cha,permission:[read,write],uid:3,gid:32,blockpointers:[]"
                self.write_ext(data)
                # Need to write to the disk. For example, "author:Ian Cha,permission:[read,write],uid:3,gid:32,filesize:5102,blockpointers:[1]"
            print(f"{file_name} is created!")
            # data = "author:Ian Cha,permission:[read,write],uid:3,gid:32,filesize:5102,blockpointers:[1]"

        else:
            print(f"There is already a file: {file_name}")

    def read_ext(self, inode_table):
        # print(inode_table, len(c), "yoyoyo")
        start = inode_table.find("blockpointers:[") + len("blockpointers:[")
        end = inode_table.find("]", start)
        raw_value = inode_table[start:end] # This gives you the string "1"

        # 2. Convert to a list
        # .split(",") handles multiple items, int(x) makes them numbers
        block_list = [int(x) for x in raw_value.split(",") if x.strip()]
        return(self.diskcontroller.get_data(block_list))
    
    def write_ext(self, lba_index, data):
        self.file_mapping_lba = 
        self.block_bit_map = 
        # self.block_bit_map[lba_index] = 1
        # if 0 not in self.block_bit_map:
        #     self.block_bit_map[0] = 1
        # else:
        #     idx = self.block_bit_map.index(0)
        #     self.block_bit_map[idx] = 1
        lba_quantity = len(data) % 100
        
            
        return (self.diskcontroller.write_data(lba_index, data))

    def read_file(self, file_name):
        lba_index = self.file_mapping_lba[file_name]["lba"]
        inode_table = self.diskcontroller.get_data([lba_index])
        return(self.file_mapping_lba[file_name]["read"](inode_table))
    
    def write_data(self, file_name, data):
        lba_index = self.file_mapping_lba[file_name]["lba"]
        self.block_bit_map[lba_index] = 1
        return(self.file_mapping_lba[file_name]["write"](lba_index, data))
        print(lba_index)

        # inode_table = self.diskcontroller.write_data([lba_index], data)
        # return(self.file_mapping_lba[file_name]["write"](inode_table, data))
        
class DiskController:
    def __init__(self, ssd):
        print("Hi I am the diskcontroller")
        self.ssd = ssd
    def get_data(self, lba_indexes):
        data_result = ""
        for i in lba_indexes:
            lba_dictionary = self.ssd.lba[i]
            block_index = lba_dictionary["block"]
            page_index = lba_dictionary["page"]
            blocks = next((item for item in self.ssd.plane if item.block_id == block_index), None)
            page = next((item for item in blocks.pages if item.page_id == page_index), None)
            data_result += page.data
            return data_result
    def write_data(self, lba_index, data):
        # right now
        pass

class Ssd:
    def __init__(self):
        self.plane = [Block(i) for i in range(lba_length)]
        # self.plane[0]

        # lba's mapping is this: lba key -> PBA
        # self.lba = {1: {"block": 0, "page": 0}, 2: {"block": 0, "page": 1}, 3: {"block": 0, "page": 2}, 4: {"block": 0, "page": 3}}
        pages_per_block = 8

        self.lba = {}


        # self.lba = {
        #     i: {
        #         "block": i // pages_per_block, 
        #         "page": i % pages_per_block
        #     }
        #     for i in range(0, lba_length)
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
        self.data_length = 100

        # if self.page_id < 5

        self.data = ""
        # self.data = "author:Ian Cha,permission:[read,write],uid:3,gid:32,filesize:5102,blockpointers:[1]"
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
my_kernel.create_file("a.txt", "EXT")
my_kernel.create_file("b.txt", "EXT")
my_kernel.create_file("a.txt", "EXT")
print(my_kernel.read_file("a.txt"))
my_kernel.write_data("a.txt", "hihihihihi")
# my_kernel.write_data("a.txt", "abcdef")
# my_kernel.delete_all("a.txt")
# my_kernel.delete_data("a.txt")

