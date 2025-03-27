```python
"""
Transforms an input grid based on the adjacency of Green (3) and Red (2) pixels.
1. If a pixel is Green (3) and has at least one adjacent Red (2) pixel (including diagonals) in the input grid, it becomes Azure (8) in the output grid.
2. If a pixel is Red (2) and has at least one adjacent Green (3) pixel (including diagonals) in the input grid, it becomes White (0) in the output grid.
3. All other pixels retain their original color.
The evaluation is based solely on the input grid state; changes are applied simultaneously to create the output grid.
"""

import numpy as np

# Define color constants for clarity
GREEN = 3
RED = 2
AZURE = 8
WHITE = 0

def _has_neighbor_with_color(grid, r, c, target_color):
    """
    Checks if any of the 8 neighbors of the cell at (r, c) in the grid 
    has the specified target_color. Handles boundary conditions.
    
    Args:
        grid (np.array): The input grid.
        r (int): Row index of the cell.
        c (int): Column index of the cell.
        target_color (int): The color to look for in the neighbors.

    Returns:
        bool: True if at least one neighbor has the target_color, False otherwise.
    """
    rows, cols = grid.shape
    # Iterate through the 3x3 neighborhood around the cell (r, c)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            
            # Calculate neighbor coordinates
            nr, nc = r + dr, c + dc
            
            # Check if the neighbor is within the grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor has the target color
                if grid[nr, nc] == target_color:
                    return True
    # No neighbor with the target color was found
    return False

def transform(input_grid):
    """
    Applies the transformation rules based on Green-Red adjacency to the input grid.

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
            current_color = input_np[r, c] # Get color from the original input grid

            # Apply Transformation_Rule_1: Green becomes Azure if adjacent to Red
            if current_color == GREEN:
                if _has_neighbor_with_color(input_np, r, c, RED):
                    output_grid[r, c] = AZURE # Modify the output grid

            # Apply Transformation_Rule_2: Red becomes White if adjacent to Green
            elif current_color == RED:
                if _has_neighbor_with_color(input_np, r, c, GREEN):
                    output_grid[r, c] = WHITE # Modify the output grid

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()
```