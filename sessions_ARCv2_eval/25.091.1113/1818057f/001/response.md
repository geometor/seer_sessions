```python
"""
Identifies all instances where a '+' shape pattern (a central pixel and its four
cardinally adjacent neighbors) consists entirely of yellow (4) pixels in the
input grid. For each identified instance, changes the color of all five pixels
constituting that '+' shape from yellow (4) to azure (8) in the output grid.
Pixels not belonging to any such qualifying yellow '+' shape retain their
original color from the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by finding yellow '+' shapes and changing their
    color to azure.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input_grid list of lists to numpy array for easier slicing/indexing
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid_np)
    
    # Get the dimensions of the grid
    height, width = input_grid_np.shape

    # Define the colors
    YELLOW = 4
    AZURE = 8

    # Iterate through each cell that can be a center of a 3x3 '+' shape
    # We iterate from row 1 to height-2 and column 1 to width-2
    # because the '+' shape requires neighbors in all four cardinal directions.
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            
            # Check if the current cell and its cardinal neighbors form a yellow '+' shape
            center_pixel = input_grid_np[r, c]
            top_pixel = input_grid_np[r - 1, c]
            bottom_pixel = input_grid_np[r + 1, c]
            left_pixel = input_grid_np[r, c - 1]
            right_pixel = input_grid_np[r, c + 1]

            # Condition: All five pixels must be yellow
            if (center_pixel == YELLOW and
                top_pixel == YELLOW and
                bottom_pixel == YELLOW and
                left_pixel == YELLOW and
                right_pixel == YELLOW):
                
                # Action: Change the color of these five pixels in the output grid to azure
                output_grid[r, c] = AZURE      # Center
                output_grid[r - 1, c] = AZURE  # Top
                output_grid[r + 1, c] = AZURE  # Bottom
                output_grid[r, c - 1] = AZURE  # Left
                output_grid[r, c + 1] = AZURE  # Right

    # Convert the numpy array back to a list of lists if necessary for the environment
    # (Assuming the standard ARC environment expects list of lists)
    return output_grid.tolist()
```