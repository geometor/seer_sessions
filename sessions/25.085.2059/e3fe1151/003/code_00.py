"""
Transforms an input grid based on the following rules applied to orange (7) pixels located *outside* the central cross (middle row and middle column):

1.  Identify the central row and central column. Pixels in this cross remain unchanged.
2.  Iterate through pixels outside the central cross.
3.  If an outside pixel is orange (7):
    a.  Examine its 8 neighbors (orthogonal and diagonal).
    b.  Check for a gray (5) neighbor:
        i.  If a gray (5) neighbor exists AND a yellow (4) neighbor also exists, change the pixel to yellow (4).
        ii. If a gray (5) neighbor exists BUT NO yellow (4) neighbor exists, change the pixel to white (0).
    c.  If NO gray (5) neighbor exists:
        i.  Check for a red (2) neighbor. If present, change the pixel to green (3).
        ii. Else, check for a maroon (9) neighbor. If present, change the pixel to red (2).
        iii. Else, check for a blue (1) or azure (8) neighbor. If present, change the pixel to gray (5).
        iv. Else, check if BOTH a yellow (4) AND a green (3) neighbor exist. If present, change the pixel to gray (5).
        v.  Otherwise, the orange pixel remains unchanged.
4.  Pixels outside the central cross that are not orange remain unchanged.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """
    Gets the values of the 8 neighbors (orthogonal and diagonal) of a cell at (r, c).
    Handles boundary conditions by excluding coordinates outside the grid.

    Args:
        grid: A numpy array representing the grid.
        r: The row index of the cell.
        c: The column index of the cell.

    Returns:
        A list of neighbor cell values.
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
    Applies the refined transformation rule to the input grid based on neighbor analysis of orange pixels.

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
    
    # Define the color codes for clarity
    ORANGE = 7
    GRAY = 5
    WHITE = 0
    YELLOW = 4
    RED = 2
    GREEN = 3
    MAROON = 9
    BLUE = 1
    AZURE = 8
    
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
                # Use a set for efficient checking of neighbor presence
                neighbor_set = set(neighbors)
                
                # Check condition 3b: Gray neighbor present?
                if GRAY in neighbor_set:
                    # Check condition 3b.i: Yellow neighbor also present?
                    if YELLOW in neighbor_set:
                        output_grid[r, c] = YELLOW
                    # Check condition 3b.ii: Gray present, but no Yellow
                    else:
                        output_grid[r, c] = WHITE
                # Check condition 3c: No Gray neighbor
                else:
                    # Check condition 3c.i: Red neighbor present?
                    if RED in neighbor_set:
                        output_grid[r, c] = GREEN
                    # Check condition 3c.ii: No Red, but Maroon neighbor present?
                    elif MAROON in neighbor_set:
                        output_grid[r, c] = RED
                    # Check condition 3c.iii: No Red/Maroon, but Blue or Azure present?
                    elif BLUE in neighbor_set or AZURE in neighbor_set:
                        output_grid[r, c] = GRAY
                    # Check condition 3c.iv: No Red/Maroon/Blue/Azure, but Yellow AND Green present?
                    elif YELLOW in neighbor_set and GREEN in neighbor_set:
                         output_grid[r, c] = GRAY
                    # Condition 3c.v: Otherwise, leave as orange (already copied)
                    # else: pass 
            # Non-orange pixels outside the cross remain unchanged (already copied)

    return output_grid