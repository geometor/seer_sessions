import numpy as np

"""
Transforms an input grid based on the following rules:
1. Identifies the central row and central column (the "central cross"). Pixels in this cross remain unchanged.
2. Iterates through pixels *outside* the central cross.
3. If an outside pixel is orange (7):
    a. Checks its 8 neighbors (orthogonal and diagonal).
    b. If any neighbor is gray (5), the pixel changes to white (0).
    c. If no neighbor is gray (5), the pixel changes to gray (5).
4. If an outside pixel is *not* orange (7), it remains unchanged.
"""

def get_neighbors(grid, r, c):
    """
    Gets the values of the 8 neighbors (orthogonal and diagonal) of a cell at (r, c).
    Handles boundary conditions.
    """
    neighbors = []
    height, width = grid.shape
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = r + dr, c + dc
            
            # Check if the neighbor coordinates are within the grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append(grid[nr, nc])
    return neighbors

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Determine the indices of the central row and column
    center_row = height // 2
    center_col = width // 2
    
    # Define the color codes
    ORANGE = 7
    GRAY = 5
    WHITE = 0
    
    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Skip pixels that are part of the central cross
            if r == center_row or c == center_col:
                continue
                
            # Check if the current pixel is orange
            if input_np[r, c] == ORANGE:
                # Get the values of the 8 neighbors
                neighbors = get_neighbors(input_np, r, c)
                
                # Check if any neighbor is gray
                has_gray_neighbor = any(neighbor == GRAY for neighbor in neighbors)
                
                # Apply the transformation based on neighbor check
                if has_gray_neighbor:
                    output_grid[r, c] = WHITE
                else:
                    output_grid[r, c] = GRAY
            # Non-orange pixels outside the cross remain unchanged (already copied)

    # Return the modified output grid
    # Convert back to list of lists if the original format is required, 
    # but numpy array is generally more convenient for ARC tasks.
    # return output_grid.tolist() 
    return output_grid
