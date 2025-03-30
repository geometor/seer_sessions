```python
import numpy as np

"""
Identify all white (0) pixels in the input grid.
For each white pixel, check its four cardinal neighbors (up, down, left, right).
If any of the neighbors is also a white pixel, change the original white pixel to azure (8) in the output grid.
All other pixels retain their original color.
"""

def transform(input_grid):
    """
    Transforms the input grid by changing white pixels adjacent to other white pixels to azure.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Iterate through each cell in the grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell is white (0)
            if input_grid[r, c] == 0:
                # Check its cardinal neighbors
                has_white_neighbor = False
                # Check Up
                if r > 0 and input_grid[r - 1, c] == 0:
                    has_white_neighbor = True
                # Check Down
                if not has_white_neighbor and r < height - 1 and input_grid[r + 1, c] == 0:
                    has_white_neighbor = True
                # Check Left
                if not has_white_neighbor and c > 0 and input_grid[r, c - 1] == 0:
                    has_white_neighbor = True
                # Check Right
                if not has_white_neighbor and c < width - 1 and input_grid[r, c + 1] == 0:
                    has_white_neighbor = True

                # If any neighbor is white, change the cell in the output grid to azure (8)
                if has_white_neighbor:
                    output_grid[r, c] = 8

    return output_grid
```