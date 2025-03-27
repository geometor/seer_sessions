"""
Transforms an input grid based on the cardinal adjacency of Green (3) and Red (2) pixels.
1. If a pixel is Green (3) and has at least one cardinal (up, down, left, right) neighbor that is Red (2) in the input grid, it becomes Azure (8) in the output grid.
2. If a pixel is Red (2) and has at least one cardinal (up, down, left, right) neighbor that is Green (3) in the input grid, it becomes White (0) in the output grid.
3. All other pixels retain their original color.
The evaluation is based solely on the input grid state; changes are applied simultaneously to create the output grid.
"""

import numpy as np

# Define color constants for clarity
GREEN = 3
RED = 2
AZURE = 8
WHITE = 0

def _has_cardinal_neighbor_with_color(grid, r, c, target_color):
    """
    Checks if any of the 4 cardinal neighbors (up, down, left, right) 
    of the cell at (r, c) in the grid has the specified target_color. 
    Handles boundary conditions.
    
    Args:
        grid (np.array): The input grid.
        r (int): Row index of the cell.
        c (int): Column index of the cell.
        target_color (int): The color to look for in the neighbors.

    Returns:
        bool: True if at least one cardinal neighbor has the target_color, False otherwise.
    """
    rows, cols = grid.shape
    # Define cardinal directions (dr, dc) for row and column changes
    cardinal_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # right, left, down, up
    
    # Iterate through the cardinal directions
    for dr, dc in cardinal_directions:
        # Calculate neighbor coordinates
        nr, nc = r + dr, c + dc
        
        # Check if the neighbor is within the grid boundaries
        if 0 <= nr < rows and 0 <= nc < cols:
            # Check if the neighbor has the target color
            if grid[nr, nc] == target_color:
                return True
                
    # No cardinal neighbor with the target color was found
    return False

def transform(input_grid):
    """
    Applies the transformation rules based on Green-Red cardinal adjacency to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize the output grid as a copy of the input grid. 
    # Pixels that don't meet transformation conditions will retain their original color.
    output_grid = input_np.copy()

    # Iterate through each pixel (cell) of the input grid
    for r in range(rows):
        for c in range(cols):
            # Get color from the original input grid
            current_color = input_np[r, c] 

            # Apply Green Pixel Transformation rule
            if current_color == GREEN:
                # Check for cardinal Red neighbors in the input grid
                if _has_cardinal_neighbor_with_color(input_np, r, c, RED):
                    # Update the corresponding pixel in the output grid
                    output_grid[r, c] = AZURE 

            # Apply Red Pixel Transformation rule
            elif current_color == RED:
                # Check for cardinal Green neighbors in the input grid
                if _has_cardinal_neighbor_with_color(input_np, r, c, GREEN):
                    # Update the corresponding pixel in the output grid
                    output_grid[r, c] = WHITE 

            # No transformation needed for other colors, they remain as copied initially

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()