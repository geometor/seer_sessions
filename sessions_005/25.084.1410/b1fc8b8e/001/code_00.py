"""
Transforms a 6x6 input grid containing white (0) and azure (8) pixels into a 5x5 output grid based on the count of azure pixels on the input grid's border.

1. Count the number of azure (8) pixels located on the perimeter (border) of the 6x6 input grid.
2. If the count of azure border pixels is greater than 2:
   - Generate a 5x5 grid where the middle row (index 2) and middle column (index 2) are white (0), and all other pixels are azure (8).
3. If the count of azure border pixels is 2 or less:
   - Generate a 5x5 grid where the middle row (index 2) and middle column (index 2) are white (0).
   - All other pixels are azure (8), except for the pixels at coordinates (0,0), (0,3), (3,0), and (3,3), which are set to white (0).
"""

import numpy as np

def count_border_azure_pixels(grid):
    """Counts the number of azure (8) pixels on the border of the grid."""
    rows, cols = grid.shape
    count = 0
    
    # Top row
    for c in range(cols):
        if grid[0, c] == 8:
            count += 1
            
    # Bottom row
    for c in range(cols):
        if grid[rows-1, c] == 8:
            count += 1
            
    # Left column (excluding corners)
    for r in range(1, rows - 1):
        if grid[r, 0] == 8:
            count += 1
            
    # Right column (excluding corners)
    for r in range(1, rows - 1):
        if grid[r, cols-1] == 8:
            count += 1
            
    return count

def create_base_output():
    """Creates the base 5x5 output grid with azure background and white cross."""
    output_grid = np.full((5, 5), 8, dtype=int) # Fill with azure
    output_grid[2, :] = 0 # Set middle row to white
    output_grid[:, 2] = 0 # Set middle column to white
    return output_grid

def transform(input_grid):
    """
    Applies the transformation rule based on border azure pixel count.
    """
    # Convert input list of lists to numpy array for easier indexing
    input_np = np.array(input_grid, dtype=int)
    
    # Count azure pixels on the border of the 6x6 input grid
    border_count = count_border_azure_pixels(input_np)
    
    # Create the base output grid (Pattern A initially)
    output_grid = create_base_output()
    
    # Check the condition based on the border count
    if border_count <= 2:
        # Modify the base grid to match Pattern B
        output_grid[0, 0] = 0
        output_grid[0, 3] = 0
        output_grid[3, 0] = 0
        output_grid[3, 3] = 0
        
    # If border_count > 2, the output_grid is already correct (Pattern A)
    
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
