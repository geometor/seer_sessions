"""
Transforms the input grid by:
1. Identifying a 'source block' of rows defined by the minimum and maximum row indices containing any non-background (non-white/0) pixels.
2. Calculating a vertical 'shift' based on the starting row index (`min_row`) and the height of the source block (`height`). The shift is calculated as `(-min_row) % height`.
3. Creating an output grid of the same dimensions as the input.
4. Filling the output grid by vertically tiling the rows from the source block, applying the calculated shift. Specifically, for each output row `r`, the row copied from the source block is determined by the index `(r + shift) % height`.
If no non-background pixels are found in the input, the output is a grid of the same dimensions filled with the background color (0).
"""

import numpy as np

def find_non_background_rows(grid_np, background_color=0):
    """
    Finds the minimum and maximum row indices containing non-background pixels.

    Args:
        grid_np (np.array): The input grid as a numpy array.
        background_color (int): The value representing the background color.

    Returns:
        tuple: (min_row, max_row) indices, or (None, None) if no non-background pixels found.
    """
    # Find rows that contain at least one pixel different from the background color
    non_background_rows = np.where(np.any(grid_np != background_color, axis=1))[0]
    
    if len(non_background_rows) == 0:
        # Handle the case where the grid might be entirely background or empty
        return None, None 
        
    min_row = np.min(non_background_rows)
    max_row = np.max(non_background_rows)
    return min_row, max_row

def extract_source_block(grid_np, min_row, max_row):
    """
    Extracts the source block (rows from min_row to max_row) from the grid.

    Args:
        grid_np (np.array): The input grid as a numpy array.
        min_row (int): The starting row index of the block.
        max_row (int): The ending row index of the block.

    Returns:
        np.array: The extracted source block.
    """
    # Slice the grid to get the rows defining the source block
    source_block = grid_np[min_row : max_row + 1, :]
    return source_block

def transform(input_grid):
    """
    Transforms the input grid according to the described tiling rule with shift.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_grid_np.shape
    background_color = 0

    # 1. Identify the rows containing the non-background pattern
    min_row, max_row = find_non_background_rows(input_grid_np, background_color)

    # 2. Handle case where no pattern is found (e.g., all background)
    if min_row is None:
        # Return a grid of zeros with the same dimensions
        return np.zeros_like(input_grid_np).tolist() 

    # 3. Define the source_block and its height
    source_block = extract_source_block(input_grid_np, min_row, max_row)
    block_height = source_block.shape[0]
    
    # Ensure block_height is not zero to avoid division by zero error
    if block_height == 0:
         return np.zeros_like(input_grid_np).tolist()

    # 4. Calculate the vertical shift
    shift = (-min_row) % block_height

    # 5. Create the output grid initialized with zeros (background)
    output_grid_np = np.zeros_like(input_grid_np)

    # 6. Fill the output grid row by row using shifted tiling
    for r in range(input_height):
        # Determine the index of the row to copy from the source_block
        # using the current output row 'r', the calculated 'shift', and the block's height
        source_index = (r + shift) % block_height
        
        # Copy the corresponding row from the source_block to the output grid
        output_grid_np[r, :] = source_block[source_index, :]

    # 7. Convert the final numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid