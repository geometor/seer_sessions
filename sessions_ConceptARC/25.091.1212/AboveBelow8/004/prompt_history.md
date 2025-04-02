
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 8 8 3 3 3 3 3 3 3 3 0
0 3 3 8 3 3 3 3 3 3 3 3 0
0 6 6 8 6 6 6 6 6 6 6 6 0
0 6 6 8 6 6 6 6 6 6 6 6 0
0 7 7 8 8 8 7 7 7 7 7 7 0
0 7 7 7 7 8 7 7 7 7 7 7 0
0 4 4 4 4 8 8 4 4 4 4 4 0
0 4 4 4 4 4 8 8 8 8 4 4 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0
```


## train_2

**input:**
```
3 3 3 3 8 8 8 8 8 8 3
3 3 3 3 8 3 3 3 3 3 3
2 2 2 2 8 8 8 8 2 2 2
2 2 2 2 2 2 2 8 2 2 2
7 7 7 7 7 7 7 8 7 7 7
7 7 7 7 7 7 7 8 7 7 7
7 7 7 7 8 8 8 8 7 7 7
9 9 9 8 8 9 9 9 9 9 9
1 1 1 8 1 1 1 1 1 1 1
1 1 1 8 8 1 1 1 1 1 1
1 1 1 1 8 8 8 1 1 1 1
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 8 8 8 8 0 0 0
0 0 0 8 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 8 8 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 8 8 8 3 3 3 3 0
0 3 3 3 8 3 3 3 3 0
0 3 8 8 8 3 3 3 3 0
0 3 8 3 3 3 3 3 3 0
0 3 8 3 3 3 3 3 3 0
0 1 8 8 1 1 1 1 1 0
0 1 1 8 1 1 1 1 1 0
0 1 1 8 8 8 8 1 1 0
0 1 1 1 1 1 8 1 1 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Perception**

The task involves processing an input grid containing various colors and producing an output grid of the same dimensions. Observing the input-output pairs reveals a consistent pattern: the output grid retains only the pixels that were 'azure' (color 8) in the input grid, keeping them in their original positions. All other pixels in the input grid, regardless of their original color (including 'white' or color 0), are replaced with 'white' (color 0) in the output grid. The transformation acts as a color filter, specifically isolating the 'azure' pixels against a 'white' background.

**Facts**


```yaml
Task: Color Filtering

Input:
  - Grid: 2D array of pixels with colors 0-9.
  - Contains various colored objects/pixels.
  - Contains 'azure' (8) colored pixels.

Output:
  - Grid: 2D array of pixels with the same dimensions as the input.
  - Contains only 'white' (0) and 'azure' (8) pixels.

Transformation:
  - Rule: Isolate 'azure' pixels.
  - Process: Iterate through each pixel of the input grid.
  - Condition: Check if the pixel color is 'azure' (8).
  - Action_True: If the pixel is 'azure', copy its color (8) to the corresponding position in the output grid.
  - Action_False: If the pixel is not 'azure', set the corresponding position in the output grid to 'white' (0).

Relationships:
  - The position of 'azure' pixels is preserved from input to output.
  - All non-'azure' pixels in the input map to 'white' pixels in the output.
  - The dimensions of the input and output grids are identical for each example pair.
```


**Natural Language Program**

1.  Initialize an output grid with the same height and width as the input grid, filling it entirely with 'white' pixels (color 0).
2.  Examine each pixel in the input grid, row by row, column by column.
3.  For each pixel, check if its color is 'azure' (color 8).
4.  If the input pixel's color is 'azure', update the pixel at the corresponding position (same row and column) in the output grid to 'azure' (color 8).
5.  If the input pixel's color is not 'azure', leave the corresponding pixel in the output grid as 'white' (color 0).
6.  After checking all pixels in the input grid, the resulting output grid is the final result.
```python
"""
Isolate 'azure' pixels (color 8) from the input grid.

The transformation function creates an output grid of the same dimensions as the input grid. It iterates through each pixel of the input grid. If a pixel's color is 'azure' (8), its color is copied to the corresponding position in the output grid. All other pixels in the output grid are set to 'white' (0).
"""

import numpy as np

def transform(input_grid):
    """
    Filters the input grid to keep only 'azure' (8) pixels, replacing others with 'white' (0).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid with only 'azure' pixels
                  preserved against a 'white' background.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid with the same dimensions, filled with 'white' (0)
    output_grid = np.zeros((height, width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel's color is 'azure' (8)
            if input_grid[r, c] == 8:
                # If it is 'azure', set the corresponding pixel in the output grid to 'azure' (8)
                output_grid[r, c] = 8
            # Otherwise, the output grid pixel remains 'white' (0) as initialized

    # Return the resulting output grid
    return output_grid
```
```python
"""
Transforms the input grid by identifying the 'core' structure of the azure (8) object.

The transformation first identifies all azure (8) pixels in the input grid.
It then applies a filter based on the local neighborhood of each azure pixel.
Specifically, an azure pixel is kept (retains its color 8) in the output grid
if it has at least 3 neighbors (including diagonals, i.e., 8-way connectivity)
that are also azure in the input grid.
All other pixels in the input grid (non-azure pixels, and azure pixels that
do not meet the neighbor threshold) are set to white (0) in the output grid.

Note: While this rule attempts to capture the "core" extraction observed in
the examples, testing indicates it does not perfectly replicate the output for
all provided training cases. It serves as an approximation of the observed
pattern of removing "thin" parts of the azure shape.
"""

import numpy as np

def get_neighbors(r, c, height, width):
    """
    Generates coordinates of 8-way adjacent neighbors for a given cell (r, c)
    within the grid boundaries (height, width).
    """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def count_azure_neighbors(grid, r, c):
    """
    Counts the number of azure (8) neighbors for a cell (r, c) in the grid,
    using 8-way adjacency.
    """
    height, width = grid.shape
    count = 0
    # Iterate through all 8 potential neighbors
    for nr, nc in get_neighbors(r, c, height, width):
        # If neighbor is azure, increment count
        if grid[nr, nc] == 8:
            count += 1
    return count

def transform(input_grid):
    """
    Filters the input grid to keep only 'core' azure pixels.

    An azure pixel is considered part of the 'core' if it has 3 or more
    azure neighbors (8-way adjacency).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid containing
                  the 'core' azure pixels against a white background.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Define the target color and neighbor threshold
    azure_color = 8
    neighbor_threshold = 3

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is azure
            if input_grid[r, c] == azure_color:
                # Count its azure neighbors
                num_neighbors = count_azure_neighbors(input_grid, r, c)
                # If the neighbor count meets the threshold, keep the pixel
                if num_neighbors >= neighbor_threshold:
                    output_grid[r, c] = azure_color
            # Otherwise, the output grid pixel remains white (0) as initialized

    # Return the resulting output grid
    return output_grid
```
