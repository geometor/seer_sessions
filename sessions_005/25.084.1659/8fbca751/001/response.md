```python
"""
This module transforms an input grid based on the following rules:
1. Create an output grid of the same dimensions as the input grid.
2. Iterate through each pixel of the input grid.
3. If the input pixel is azure (8), the corresponding output pixel is also azure (8).
4. If the input pixel is white (0):
    a. Check its direct neighbors (up, down, left, right).
    b. If any direct neighbor is azure (8), the corresponding output pixel becomes red (2).
    c. If no direct neighbors are azure (8), the corresponding output pixel remains white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing white pixels adjacent to azure pixels to red.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Initialize the output grid as a copy of the input grid
    # We will modify the white pixels that need to change to red
    output_array = np.copy(input_array)

    # Define the offsets for direct neighbors (up, down, left, right)
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Define color constants
    WHITE = 0
    AZURE = 8
    RED = 2

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is white
            if input_array[r, c] == WHITE:
                # Assume no azure neighbor initially
                has_azure_neighbor = False
                # Check all direct neighbors
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor is within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor is azure
                        if input_array[nr, nc] == AZURE:
                            has_azure_neighbor = True
                            # Found an azure neighbor, no need to check further for this pixel
                            break 
                
                # If at least one direct neighbor was azure, change the output pixel to red
                if has_azure_neighbor:
                    output_array[r, c] = RED
            
            # If the pixel is not white (i.e., it's azure), it remains unchanged (already copied)
            # If the pixel is white but has no azure neighbors, it also remains unchanged (white)

    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_array.tolist()

    return output_grid
```