import numpy as np

"""
Identify the largest contiguous block of solid, non-white rows in the input grid. 
Preserve only this block in the output grid, setting all other pixels to white (0).
A solid row consists entirely of a single non-white color.
A block is a vertically contiguous sequence of solid rows of the same color.
The largest block is the one with the greatest number of rows (height).
"""

def transform(input_grid):
    """
    Transforms the input grid by identifying the largest block of solid, 
    non-white rows and preserving only that block.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output grid with white (0)
    output_grid = np.zeros_like(input_array)

    # --- Find solid rows ---
    solid_rows = []  # Store tuples: (row_index, color)
    for r in range(height):
        row = input_array[r, :]
        unique_colors = np.unique(row)
        # Check if the row has exactly one unique color and it's not white (0)
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            solid_rows.append((r, unique_colors[0]))

    # If no solid rows found, return the all-white grid
    if not solid_rows:
        return output_grid.tolist()

    # --- Group solid rows into contiguous blocks of the same color ---
    blocks = []  # Store tuples: (start_row, end_row, color, height)
    if not solid_rows: # Should be redundant due to above check, but safe
         return output_grid.tolist()

    current_block_start_index = 0
    while current_block_start_index < len(solid_rows):
        start_row, color = solid_rows[current_block_start_index]
        current_height = 1
        
        # Look ahead to find contiguous rows of the same color
        next_row_in_block_index = current_block_start_index + 1
        while (next_row_in_block_index < len(solid_rows) and
               solid_rows[next_row_in_block_index][0] == start_row + current_height and # Check contiguity
               solid_rows[next_row_in_block_index][1] == color): # Check same color
            current_height += 1
            next_row_in_block_index += 1
            
        end_row = start_row + current_height - 1
        blocks.append((start_row, end_row, color, current_height))
        
        # Move to the start of the next potential block
        current_block_start_index = next_row_in_block_index

    # --- Select the largest block (by height) ---
    if not blocks: # If somehow no blocks were formed
        return output_grid.tolist()
        
    # Find the block with the maximum height
    # In case of ties in height, max() naturally takes the first one encountered in the list 'blocks'
    largest_block = max(blocks, key=lambda item: item[3])
    
    # --- Construct the output grid ---
    start_r, end_r, _, _ = largest_block
    
    # Copy the largest block from the input array to the output grid
    output_grid[start_r : end_r + 1, :] = input_array[start_r : end_r + 1, :]

    # Return the result as a list of lists
    return output_grid.tolist()
