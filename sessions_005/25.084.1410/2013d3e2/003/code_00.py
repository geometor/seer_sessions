"""
1. Identify all non-white pixels in the input grid.
2. Determine the minimum row index (`min_row`) and minimum column index (`min_col`) among all identified non-white pixels. These coordinates (`min_row`, `min_col`) define the top-left corner of the bounding box enclosing all non-white content.
3. Extract a 3x3 subgrid from the input grid starting at the position (`min_row`, `min_col`).
4. The extracted 3x3 subgrid is the output grid.
"""

import numpy as np

def find_bounding_box_top_left(grid):
    """
    Finds the top-left corner (row, col) of the bounding box containing all 
    non-white (non-zero) pixels.
    Returns (row, col) or raises an error if no non-white pixels are found.
    """
    # Find coordinates of all non-white pixels
    non_white_pixels = np.argwhere(grid != 0)
    
    # Check if any non-white pixels were found
    if non_white_pixels.size == 0:
        # Based on task examples, this case should not occur.
        # If it did, the definition of the bounding box is unclear.
        # Returning (0,0) or raising an error are options.
        # Let's raise an error for clarity, assuming valid inputs always have non-white pixels.
        raise ValueError("Input grid must contain at least one non-white pixel.")
        
    # Calculate the minimum row index
    min_row = non_white_pixels[:, 0].min()
    # Calculate the minimum column index
    min_col = non_white_pixels[:, 1].min()
    
    return int(min_row), int(min_col)

def transform(input_grid_list):
    """
    Extracts a 3x3 subgrid from the input grid starting at the top-left 
    corner of the bounding box of all non-white pixels.
    """
    # Convert list of lists to numpy array for efficient processing
    input_grid = np.array(input_grid_list, dtype=int)

    # Find the top-left corner (min_row, min_col) of the bounding box
    # containing all non-white pixels.
    try:
        min_row, min_col = find_bounding_box_top_left(input_grid)
    except ValueError as e:
        # Handle the case where no non-white pixels are found, 
        # e.g., return an empty grid or the original grid, or re-raise.
        # Based on ARC examples, input always has non-white pixels, so 
        # this is mainly defensive programming. Let's return an empty 3x3 for now.
        # print(f"Error: {e}") 
        # return [[0,0,0],[0,0,0],[0,0,0]] # Or raise e
        
        # Re-evaluating: ARC tasks usually guarantee valid transformations are possible.
        # Raising the error is better if assumptions are violated.
         raise e


    # Extract the 3x3 subgrid starting from (min_row, min_col).
    # Slicing handles boundary conditions implicitly: if the slice goes beyond
    # the grid dimensions, numpy returns only the available part. 
    # However, ARC tasks generally ensure the 3x3 extraction is possible.
    output_grid_np = input_grid[min_row : min_row + 3, min_col : min_col + 3]

    # Ensure the output is exactly 3x3, padding with 0s if necessary
    # (though based on examples, this shouldn't be needed)
    h, w = output_grid_np.shape
    if h < 3 or w < 3:
        padded_output = np.zeros((3, 3), dtype=int)
        padded_output[:h, :w] = output_grid_np
        output_grid_np = padded_output
        
    # Convert the resulting numpy array back to a list of lists for the standard output format
    output_grid = output_grid_np.tolist()

    return output_grid