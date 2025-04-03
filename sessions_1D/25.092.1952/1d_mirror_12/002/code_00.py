# --- Example 1 ---
# Input:  [0, 3, 3, 3, 3, 3, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# Output: [0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0]
# Metrics:
#   grid_size: 22
#   pivot_index: 9
#   movable_block: color=3, start=1, size=5
#   input_block_end_index: 5
#   separation_distance (input): 9 - (5 + 1) = 3
#   output_block_start_index: 9 + 1 + 3 = 13
#   output_block_end_index: 13 + 5 = 18 (within bounds)

# --- Example 2 ---
# Input:  [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# Output: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0]
# Metrics:
#   grid_size: 22
#   pivot_index: 11
#   movable_block: color=2, start=4, size=6
#   input_block_end_index: 9
#   separation_distance (input): 11 - (9 + 1) = 1
#   output_block_start_index: 11 + 1 + 1 = 13
#   output_block_end_index: 13 + 6 = 19 (within bounds)

# --- Example 3 ---
# Input:  [0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0]
# Output: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 4, 4, 4, 4, 4, 4, 0]
# Metrics:
#   grid_size: 22
#   pivot_index: 13
#   movable_block: color=4, start=6, size=6
#   input_block_end_index: 11
#   separation_distance (input): 13 - (11 + 1) = 1
#   output_block_start_index: 13 + 1 + 1 = 15
#   output_block_end_index: 15 + 6 = 21 (within bounds)