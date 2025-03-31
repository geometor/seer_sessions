```python
"""
Transforms an input grid based on the following rule:
1. Initialize an output grid as a copy of the input grid.
2. Iterate through each pixel of the input grid.
3. If a pixel is white (0), check its cardinal neighbors (up, down, left, right) in the input grid.
4. If any cardinal neighbor is blue (1), change the corresponding pixel in the output grid to yellow (4).
5. Pixels that are not white (0) in the input grid, or white pixels without any blue cardinal neighbors, remain unchanged in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing white pixels (0) to yellow (4) 
    if they are cardinally adjacent to a blue pixel (1).

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    height, width = input_np.shape

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the input grid is white (0)
            if input_np[r, c] == 0:
                # Define cardinal neighbor offsets
                neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
                found_blue_neighbor = False
                # Check each cardinal neighbor
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor is within grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor in the *input* grid is blue (1)
                        if input_np[nr, nc] == 1:
                            found_blue_neighbor = True
                            break # Found one, no need to check others
                
                # If a blue cardinal neighbor was found, change the pixel in the output grid to yellow (4)
                if found_blue_neighbor:
                    output_grid[r, c] = 4

    # Pixels that were not white (0) or white pixels without blue neighbors 
    # retain their original value because output_grid was initialized as a copy.
    return output_grid.tolist() # Return as list of lists if required by ARC standard

```