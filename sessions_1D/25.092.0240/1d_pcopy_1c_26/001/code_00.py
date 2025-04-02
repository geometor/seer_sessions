import numpy as np

"""
Identify isolated non-white pixels in the input grid. An isolated pixel is defined as a non-white pixel (value > 0) where all 8 of its adjacent neighbors (horizontal, vertical, and diagonal) are white (value 0). 
For each row containing at least one such isolated pixel, find the color of one of these isolated pixels (if multiple isolated pixels exist in the same row, any of their colors can be used, as the examples suggest they will have the same color or the effect is determined by one). 
Fill the entire corresponding row in the output grid with that color. 
Rows that do not contain any isolated non-white pixels remain unchanged from the input.
"""

def is_isolated(grid, r, c):
    """
    Checks if the pixel at (r, c) in the grid is isolated.
    An isolated pixel is non-white and has only white neighbors.
    Assumes the pixel at (r, c) is already checked to be non-white.
    """
    rows, cols = grid.shape
    # Iterate through all 8 neighbors
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the pixel itself
            if dr == 0 and dc == 0:
                continue
                
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # If a neighbor is not white (0), the pixel is not isolated
                if grid[nr, nc] != 0:
                    return False
    # If all neighbors are white (or out of bounds), the pixel is isolated
    return True

def transform(input_grid):
    """
    Transforms the input grid based on isolated pixels.
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # Keep track of rows that have already been filled to avoid redundant checks/fills
    # Although not strictly necessary based on examples, it's slightly more efficient.
    filled_rows = set() 

    # Iterate through each pixel of the input grid
    for r in range(rows):
        # If row already processed, skip
        if r in filled_rows:
            continue
            
        for c in range(cols):
            pixel_color = input_np[r, c]
            
            # Check if the pixel is non-white
            if pixel_color != 0:
                # Check if the non-white pixel is isolated
                if is_isolated(input_np, r, c):
                    # If isolated, fill the entire row in the output grid with its color
                    output_np[r, :] = pixel_color
                    # Mark row as filled and break the inner loop for this row
                    filled_rows.add(r)
                    break # Move to the next row once an isolated pixel fills this one

    # Convert the final NumPy array back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid
