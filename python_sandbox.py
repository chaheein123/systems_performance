# block_bit_map = [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0]
block_bit_map = [0,0,0,0,0,0,0,0,0]


last_idx = len(block_bit_map) - 1 - block_bit_map[::-1].index(1)

# block_bit_map[last_idx + 1] = 1
# print(last_idx)
# print(block_bit_map)