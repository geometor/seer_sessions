```python
"""
Transforms an input grid by identifying a "seed" pixel (the first non-zero pixel), drawing a frame of the seed's color around the output grid, and setting the seed and its immediate neighbors in the *input* grid to 0, then copying the input grid to the output, leaving the frame intact.
"""

import numpy as np

def get_seed_pixel(grid):
    # Find the coordinates and value of the first non-zero pixel (seed).
    non_zero_indices = np.nonzero(grid)
    if len(non_zero_indices[0]) > 0:
       x = non_zero_indices[0][0]
       y = non_zero_indices[1][0]
       color = grid[x, y]
       return x, y, color
    return None, None, None

def clear_neighbors(grid, x, y):
    # Set the value of the seed pixel and its orthogonal neighbors to 0 *in place*.
    rows, cols = grid.shape
    if x > 0:
        grid[x - 1, y] = 0  # Above
    if x < rows - 1:
        grid[x + 1, y] = 0  # Below
    if y > 0:
        grid[x, y - 1] = 0  # Left
    if y < cols - 1:
        grid[x, y + 1] = 0  # Right
    grid[x,y] = 0

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Get the seed pixel information
    seed_x, seed_y, seed_color = get_seed_pixel(input_grid)

    if seed_x is None:  # No seed pixel, return original grid
        return input_grid.tolist()

    # Create the frame with the seed color
    output_grid[0, :] = seed_color          # Top row
    output_grid[-1, :] = seed_color         # Bottom row
    output_grid[:, 0] = seed_color          # Left column
    output_grid[:, -1] = seed_color         # Right column
    
    #clear neighbors *in the input grid*
    clear_neighbors(input_grid, seed_x, seed_y)

    # Copy the modified input grid to the output grid, *except* where the frame was set
    for i in range(rows):
        for j in range(cols):
            if not (i == 0 or i == rows - 1 or j == 0 or j == cols-1):
                output_grid[i,j] = input_grid[i,j]

    return output_grid.tolist()
```