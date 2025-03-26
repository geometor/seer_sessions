```python
import numpy as np

def transform(input_grid):
    """
    Identify isolated red pixels (value 2) and change their color to blue (value 1).
    A red pixel is considered isolated if none of its cardinal neighbors (up, down, left, right) are also red.
    All other pixels retain their original color.
    """

    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel in the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is red (value 2)
            if input_grid[r, c] == 2:
                # Initialize a counter for red neighbors
                red_neighbor_count = 0

                # Define the coordinates of the cardinal neighbors
                neighbors = [
                    (r - 1, c),  # Up
                    (r + 1, c),  # Down
                    (r, c - 1),  # Left
                    (r, c + 1)   # Right
                ]

                # Check each neighbor
                for nr, nc in neighbors:
                    # Check if the neighbor is within the grid boundaries
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor is red
                        if input_grid[nr, nc] == 2:
                            red_neighbor_count += 1
                            # We only need to know if *at least one* neighbor is red,
                            # so we can break early if we find one.
                            break 
                
                # If no cardinal neighbors are red, change the pixel to blue in the output grid
                if red_neighbor_count == 0:
                    output_grid[r, c] = 1
            
            # If the pixel is not red, or if it is red but has red neighbors, 
            # it keeps its original color (already set by the initial copy)

    return output_grid
```