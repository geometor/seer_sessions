"""
1.  **Identify Objects:** Locate the azure (8) pixel and the yellow (4) pixels. The remaining pixels are black (0).
2.  **Azure Expansion:** The azure (8) expands *one unit* to the left, right, and down, replacing black pixels.
3. **Yellow Preservation:** The yellow pixels remain unchanged.
"""

import numpy as np

def find_azure_pixel(grid):
    """Finds the coordinates of the first azure (8) pixel."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 8:
                return r, c
    return None, None  # Return None if no azure pixel is found

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the azure pixel
    azure_r, azure_c = find_azure_pixel(output_grid)

    # If no azure pixel, return the original grid (no change)
    if azure_r is None:
        return output_grid
    
    # Define expansion directions (left, right, down) relative to azure pixel
    expansion_directions = [
      (0,-1), #left
      (0,1), #right
      (1,0) #down
    ]

    # Expand azure pixel one unit in each specified direction
    for dr, dc in expansion_directions:
        new_r, new_c = azure_r + dr, azure_c + dc
        # Check bounds and if the target cell is black (0)
        if 0 <= new_r < rows and 0 <= new_c < cols and output_grid[new_r, new_c] == 0:
            output_grid[new_r, new_c] = 8

    # set original azure position to 8 (in case of over-writes)
    output_grid[azure_r, azure_c] = 8

    return output_grid