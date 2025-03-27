```python
"""
Create a copy of the input grid. Iterate through each pixel in the input grid. If a pixel's color is red (2), identify its 8 neighbouring pixels (horizontally, vertically, and diagonally adjacent). For each neighbour that exists within the grid boundaries and is white (0) in the original input grid, change the color of the corresponding pixel in the output grid to blue (1). All other pixels retain their original color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing white pixels adjacent to red pixels to blue.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        numpy.ndarray: The transformed grid as a NumPy array.
    """
    # Convert input_grid to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Create a copy of the input grid to serve as the output grid
    output_grid = np.copy(input_np)
    
    # Get the dimensions of the grid
    height, width = input_np.shape

    # Define the relative coordinates for the 8 neighbours (including diagonals)
    neighbours = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each pixel in the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is red (2)
            if input_np[r, c] == 2:
                # Iterate through the 8 neighbours
                for dr, dc in neighbours:
                    nr, nc = r + dr, c + dc
                    
                    # Check if the neighbour coordinates are within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbour pixel in the *original* input grid is white (0)
                        if input_np[nr, nc] == 0:
                            # Change the corresponding pixel in the *output* grid to blue (1)
                            output_grid[nr, nc] = 1
                            
    # Return the modified output grid
    return output_grid

```