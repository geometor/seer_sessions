```python
"""
Iterate through each pixel of the input grid. If a pixel's color is orange (7), check its 8 neighbors (orthogonal and diagonal). If any neighbor is blue (1), change the color of that pixel to gray (5) in the output grid. Otherwise, keep the original color. All non-orange pixels retain their original color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the rule: orange pixels adjacent to blue pixels become gray.

    Args:
        input_grid (list of lists of int): The input grid representing pixel colors.

    Returns:
        list of lists of int: The transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Get grid dimensions
    height, width = input_array.shape
    # Initialize output_grid as a copy of the input_grid
    output_array = np.copy(input_array)

    # Define the offsets for the 8 neighbors (horizontal, vertical, diagonal)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    # Iterate through each pixel in the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is orange (7)
            if input_array[r, c] == 7:
                # Assume initially that no blue neighbor is found
                found_blue_neighbor = False
                # Check all 8 neighbors
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor coordinates are within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor is blue (1)
                        if input_array[nr, nc] == 1:
                            found_blue_neighbor = True
                            # No need to check other neighbors once one is found
                            break 
                
                # If at least one blue neighbor was found, change the pixel in the output grid to gray (5)
                if found_blue_neighbor:
                    output_array[r, c] = 5
            
            # If the pixel is not orange (7), or if it is orange but has no blue neighbors,
            # its value in the output_array remains unchanged (as it was copied initially).

    # Convert the output NumPy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid

```