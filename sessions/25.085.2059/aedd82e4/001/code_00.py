"""
Iterate through each pixel in the input grid. If a pixel's color is red (2), 
check its 8 neighbors (up, down, left, right, and diagonals). If all existing 
neighbors are white (0), change the pixel's color to blue (1) in the output grid. 
Otherwise, keep the original color. The output grid has the same dimensions as 
the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing isolated red pixels to blue.
    A red pixel is considered isolated if all its existing neighbors (8-way adjacency) 
    are white.
    
    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape

    # Define neighbor offsets (8 directions: up, down, left, right, diagonals)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each pixel in the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is red (2)
            if input_np[r, c] == 2:
                is_isolated = True # Assume isolated initially
                
                # Check all 8 neighbors
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc

                    # Check if the neighbor coordinates are within grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # If a neighbor exists and is NOT white (0)
                        if input_np[nr, nc] != 0:
                            is_isolated = False
                            break # No need to check other neighbors
                
                # If the pixel is red and isolated (all existing neighbors are white)
                if is_isolated:
                    # Change the color of the pixel to blue (1) in the output grid
                    output_grid[r, c] = 1
            
            # If the pixel is not red, or it's red but not isolated, 
            # its color remains unchanged (already handled by copying the input)

    return output_grid.tolist() # Return as list of lists as per ARC standard