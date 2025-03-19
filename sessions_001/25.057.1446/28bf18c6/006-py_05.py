"""
1.  **Identify Azure Blocks:** Find all pixels in the input grid that are colored azure (8).
2.  **Group Contiguous Blocks:** Group the azure pixels into contiguous blocks. Two azure pixels are contiguous if they are adjacent horizontally or vertically.
3.  **Output Grid:** Create a new output grid that is 3 rows by 6 columns, filled with black (0) pixels.
4.  **Transfer and Arrange Blocks:** Iterate through the contiguous blocks found in the input.  For each block:
    *   Maintain its original shape and size.
    *   Place the block into the output grid, prioritizing the top-left corner.
        * If the block will fit by placing the top-left of the object in the (0,0) of the grid, use that location
        * If not, find the next empty space from left-to-right, top-to-bottom where placing the top-left corner of the block will still allow the entire block to fit in the output grid.
5.  **Output:** The output grid is the result.
"""

import numpy as np

def find_pixels(grid, color):
    # Find coordinates of pixels with the specified color.
    return np.array(np.where(grid == color)).T

def get_contiguous_blocks(pixels):
    # group pixels into contiguous sets, horizontally or vertically
    
    if len(pixels) == 0:
      return []

    blocks = []
    current_block = [pixels[0]]

    for i in range(1, len(pixels)):
        is_contiguous = False
        for prev_pixel in current_block:
            if (abs(pixels[i][0] - prev_pixel[0]) == 1 and pixels[i][1] == prev_pixel[1]) or \
               (abs(pixels[i][1] - prev_pixel[1]) == 1 and pixels[i][0] == prev_pixel[0]):
               is_contiguous = True
               break

        if is_contiguous:
          current_block.append(pixels[i])
        else:
            blocks.append(np.array(current_block))
            current_block = [pixels[i]]

    blocks.append(np.array(current_block))
    return blocks

def get_block_dimensions(block):
     # Calculate the width and height of a block
    min_row, min_col = np.min(block, axis=0)
    max_row, max_col = np.max(block, axis=0)
    return max_row - min_row + 1, max_col - min_col + 1

def can_place_block(output_grid, block, row_start, col_start):
    # check if the block will fit in the output grid starting from the (row_start, col_start)
    block_height, block_width = get_block_dimensions(block)
    if row_start + block_height > output_grid.shape[0] or col_start + block_width > output_grid.shape[1]:
        return False

    # Get relative positions within the block.
    min_row = np.min(block[:, 0])
    min_col = np.min(block[:, 1])
    relative_positions = block - [min_row, min_col]

    for pos in relative_positions:
        if output_grid[row_start + pos[0], col_start + pos[1]] != 0:
            return False  # Overlapping with existing block

    return True

def place_block(output_grid, block, row_start, col_start):
     # Place the block in the output grid starting at row_start, col_start.
    min_row = np.min(block[:, 0])
    min_col = np.min(block[:, 1])
    relative_positions = block - [min_row, min_col]

    for pos in relative_positions:
        output_grid[row_start + pos[0], col_start + pos[1]] = 8


def transform(input_grid):
    # initialize output_grid (3x6)
    output_grid = np.zeros((3, 6), dtype=int)

    # Find all azure pixels.
    azure_pixels = find_pixels(input_grid, 8)

    # Group into contiguous blocks.
    blocks = get_contiguous_blocks(azure_pixels)

    # Place each block in the output grid.
    for block in blocks:
        placed = False
        for row_start in range(output_grid.shape[0]):
            for col_start in range(output_grid.shape[1]):
                if can_place_block(output_grid, block, row_start, col_start):
                    place_block(output_grid, block, row_start, col_start)
                    placed = True
                    break  # Move to the next block after placing
            if placed:
                break

    return output_grid