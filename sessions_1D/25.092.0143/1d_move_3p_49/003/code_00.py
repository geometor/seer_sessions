import numpy as np
import copy

"""
Accept the input grid (a 2D NumPy array with shape 1xN). Identify the single 
contiguous horizontal block of non-white pixels in the first row (index 0). 
Calculate the new starting column index for the block by adding 3 to its 
original starting column index. Create a new output grid of the same shape, 
filled with white pixels (0), and copy the identified block into the first 
row of the output grid at the calculated new starting column index.
"""

def find_colored_block_row0(grid):
    """
    Finds the start column index, end column index (exclusive), and color 
    of the first contiguous block of non-white pixels in the first row 
    (index 0) of a 2D grid.

    Args:
        grid (np.array): A 2D numpy array representing the grid.

    Returns:
        tuple: (start_col, end_col, color) or (None, None, None) 
               if no block is found in the first row.
    """
    if grid.shape[0] == 0: # Handle empty grid case
        return None, None, None
        
    first_row = grid[0, :]
    start_col = None
    color = None
    
    # Find the start of the block and its color
    for i, pixel in enumerate(first_row):
        if pixel != 0:
            start_col = i
            color = pixel
            break
    
    # If no non-white pixel found, return None
    if start_col is None:
        return None, None, None

    # Find the end of the block
    end_col = start_col
    for i in range(start_col, len(first_row)):
        if first_row[i] == color:
            end_col = i + 1  # end_col is exclusive
        else:
            break  # End of the block
            
    return start_col, end_col, color

def transform(input_grid):
    """
    Shifts the single contiguous non-white block in the first row of the 
    input grid 3 positions (columns) to the right.

    Args:
        input_grid (np.array): A 2D numpy array (shape 1xN) representing 
                               the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed grid.
    """
    
    # Find the properties of the colored block in the input grid's first row
    start_col, end_col, color = find_colored_block_row0(input_grid)

    # Handle case where no block is found (return a copy of the input)
    if start_col is None:
        return copy.deepcopy(input_grid) 

    # Get the shape and dimensions
    rows, cols = input_grid.shape
    block_length = end_col - start_col
    
    # Initialize the output grid with the background color (white/0)
    output_grid = np.zeros_like(input_grid)

    # Calculate the new starting position by shifting right by 3 columns
    new_start_col = start_col + 3
    new_end_col = new_start_col + block_length

    # Check if the new position goes out of bounds (optional but safe)
    # If it does, part of the block might be cut off, or it might wrap,
    # but based on examples, we assume it fits.
    actual_end_col = min(new_end_col, cols) # Ensure we don't write past the grid width
    actual_length = actual_end_col - new_start_col

    # Place the block in the new position in the output grid's first row
    # Only attempt to write if the new start position is valid
    if new_start_col < cols and actual_length > 0:
        # Write the block (or the part that fits) to the first row
        output_grid[0, new_start_col:actual_end_col] = color 
            
    return output_grid