import numpy as np

"""
Moves a contiguous horizontal block of a single color (not white or maroon) 
relative to a fixed maroon pixel in a single-row grid.

1. Finds the maroon (9) pixel and its index.
2. Finds the contiguous block of pixels with a color other than white (0) or maroon (9).
3. Creates a new grid of the same size, filled with white (0).
4. Places the maroon pixel in the new grid at its original index.
5. Calculates the new starting index for the block as the maroon pixel's index plus 2.
6. Places the colored block (using its original color and length) into the new grid 
   starting at the calculated new index.
"""

def find_maroon_index(grid_row):
    """Finds the index of the maroon (9) pixel in a 1D array."""
    for index, pixel in enumerate(grid_row):
        if pixel == 9:
            return index
    return -1 # Should not happen based on task description

def find_colored_block(grid_row):
    """Finds the color, start index, and length of the non-white/maroon block."""
    block_color = -1
    block_start_index = -1
    block_length = 0
    in_block = False

    for index, pixel in enumerate(grid_row):
        if pixel != 0 and pixel != 9: # Found the block color
            if not in_block:
                block_color = pixel
                block_start_index = index
                block_length = 1
                in_block = True
            else: # Continue the block
                block_length += 1
        elif in_block: # Block has ended
            break # Since there's only one block expected

    if block_color != -1:
        return block_color, block_start_index, block_length
    else:
        return None, -1, 0 # Should not happen based on task description

def transform(input_grid):
    """
    Applies the transformation rule to move the colored block.
    Assumes input_grid is a 2D numpy array with only one row.
    """
    # Work with the first (and only) row
    input_row = input_grid[0]
    grid_length = len(input_row)

    # Initialize output_grid (as a 1D list for now)
    # filled with the background color (white/0)
    output_row = [0] * grid_length

    # Find the index of the maroon (9) pixel
    maroon_index = find_maroon_index(input_row)
    if maroon_index == -1:
        # Handle error or unexpected input: no maroon pixel found
        # For now, return the input or an empty grid? Returning input.
        return input_grid 

    # Place the maroon pixel in the output row
    output_row[maroon_index] = 9

    # Find the colored block (color, start index, length)
    block_color, _, block_length = find_colored_block(input_row)

    if block_color is None:
         # Handle error or unexpected input: no colored block found
         # For now, return the partially filled output (with just maroon) 
         # wrapped back into a 2D array
         return np.array([output_row])

    # Calculate the new starting index for the block
    new_block_start_index = maroon_index + 2

    # Check bounds before placing the block
    if new_block_start_index + block_length > grid_length:
        # Handle cases where the block would go out of bounds
        # Option 1: Truncate the block (might not be correct based on examples)
        # Option 2: Error or return unchanged? Let's place what fits.
        placeable_length = grid_length - new_block_start_index
    else:
        placeable_length = block_length
        
    # Place the colored block in the output row
    for i in range(placeable_length):
        idx = new_block_start_index + i
        output_row[idx] = block_color

    # Convert the output row list back to a 2D numpy array as required by ARC
    output_grid = np.array([output_row])

    return output_grid