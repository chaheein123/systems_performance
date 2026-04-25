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
