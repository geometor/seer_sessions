"""
Transforms the input grid based on the following rule:
Find isolated non-white pixels in the input grid. An isolated pixel is a single 
non-white pixel whose immediate neighbors (up, down, left, right, within bounds) 
are all white (0).
For each isolated pixel found at position (row, col) with color C, change the 
color of the pixels at (row, col+1) and (row, col+2) in the output grid to C, 
provided these positions are within the grid bounds. Pixels that are part of 
larger non-white blocks remain unchanged.
"""

import numpy as np

def is_isolated(grid, r, c):
    """
    Checks if the pixel at (r, c) is isolated.
    An isolated pixel is a non-white pixel whose neighbors (up, down, left, right)
    are all white (0) or out of bounds.
    """
    height, width = grid.shape
    pixel_color = grid[r, c]

    # Must be non-white to be potentially isolated in the context of the rule
    if pixel_color == 0:
        return False

    # Define neighbor directions
    neighbors = [
        (r - 1, c),  # Up
        (r + 1, c),  # Down
        (r, c - 1),  # Left
        (r, c + 1)   # Right
    ]

    # Check each neighbor
    for nr, nc in neighbors:
        # Check if neighbor is within bounds
        if 0 <= nr < height and 0 <= nc < width:
            # If neighbor is non-white, the current pixel is not isolated
            if grid[nr, nc] != 0:
                return False
                
    # If all valid neighbors are white (0), the pixel is isolated
    return True

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list representing the flattened input grid.

    Returns:
        A numpy array representing the transformed grid.
    """
    # --- Input Preprocessing ---
    # Determine grid dimensions (assuming 3 rows based on examples)
    num_elements = len(input_grid)
    if num_elements == 0:
        return np.array([[]]) # Handle empty input
    # Assuming 3 rows for the given examples (33 elements -> 3x11)
    # A more general approach might try different factors or require explicit dimensions
    height = 3
    if num_elements % height != 0:
         # Fallback or error for non-divisible elements - let's try to infer width
         # This part might need adjustment if grids aren't always 3 rows high
         factors = [i for i in range(1, 31) if num_elements % i == 0]
         if not factors: return np.array(input_grid).reshape(1, -1) # Cannot determine, treat as 1 row
         # Heuristic: Choose a height <= 30 if possible. Maybe pick smallest reasonable height?
         # For 33, factors are 1, 3, 11, 33. 3x11 is the only reasonable 2D grid.
         height = 3 # Stick with 3 for this problem based on examples
         
    width = num_elements // height
    
    # Reshape the flattened input into a 2D numpy array
    try:
      grid = np.array(input_grid).reshape((height, width))
    except ValueError:
        # Handle cases where reshaping isn't possible with inferred dims
        print(f"Warning: Could not reshape input of size {num_elements} into {height}x{width}. Returning as 1D.")
        grid = np.array(input_grid).reshape(1, -1) # Treat as single row
        height, width = grid.shape

    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()

    # --- Transformation Logic ---
    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is non-white
            if grid[r, c] != 0:
                # Check if the pixel is isolated
                if is_isolated(grid, r, c):
                    # Get the color of the isolated pixel
                    color_to_expand = grid[r, c]

                    # Expand right by 1 position
                    if c + 1 < width:
                        output_grid[r, c + 1] = color_to_expand

                    # Expand right by 2 positions
                    if c + 2 < width:
                        output_grid[r, c + 2] = color_to_expand
                        
    # Return the transformed grid (as a numpy array)
    # If the original input was expected as a list of lists, convert back:
    # return output_grid.tolist() 
    # For now, returning numpy array is standard in ARC contexts.
    return output_grid
