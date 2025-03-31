
## train_1

**input:**
```
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 5 9 0 0 0
0 0 0 0 0 5 5 9 0 0
0 0 0 0 0 5 5 5 9 0
0 0 0 0 0 5 5 5 5 9
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 9 0 0 0 0
9 0 0 0 0 0 9 0 0 0
0 9 0 0 0 0 0 9 0 0
0 0 9 0 0 0 0 0 9 0
0 0 0 9 0 0 0 0 0 9
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 9 0
```


## train_2

**input:**
```
7 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 7 5 5 0 0 0 0
0 0 0 0 7 5 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7
```


**output:**
```
7 0 0 0 7 0 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 0 7 0 0 0 7 0 0 0
0 0 0 7 0 0 0 7 0 0
0 0 0 0 7 0 0 0 7 0
0 0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 2 5 5 0 0 0 0 0
0 0 0 2 5 0 0 0 0 0
0 0 0 5 2 0 0 0 0 0
0 0 0 5 5 2 0 0 0 0
0 0 0 5 5 5 2 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0
```


**output:**
```
0 0 0 2 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 2 0 0 0 2 0 0
0 0 0 0 2 0 0 0 2 0
2 0 0 0 0 2 0 0 0 2
0 2 0 0 0 0 2 0 0 0
0 0 2 0 0 0 0 2 0 0
0 0 0 2 0 0 0 0 2 0
```

```python
import numpy as np
import sys
import os

# Add the directory containing helper_functions.py to the Python path
# Assuming helper_functions.py is in the same directory as the script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Attempt to import helper functions, handle potential ImportError
try:
    from helper_functions import find_objects, get_color_distribution, most_common_color
except ImportError:
    # Define dummy functions or print a message if helper_functions is not available
    print("Warning: helper_functions.py not found. Using placeholder functions.")
    find_objects = lambda grid, color: []
    get_color_distribution = lambda grid: {}
    most_common_color = lambda grid: 0 # Default to background color

# Define color constants (optional, but can improve readability)
COLOR_BACKGROUND = 0
COLOR_OBSTACLE = 5

"""
Transformation Rule Description:

1. Identify the primary 'shape' color in the input grid. This is the most frequent non-background (non-zero) color, excluding gray (color 5). If no such color exists, the output is an empty grid of the same size.
2. Create an output grid of the same dimensions as the input grid, initialized entirely with the background color (0).
3. Find all locations (row, column) of the identified shape color in the input grid.
4. For each location (r, c) where the shape color was found in the input:
    a. Iterate downwards from this row `r` to the bottom of the grid (last row).
    b. For each row `nr` in this downward path (from `r` to `height - 1`), set the pixel at `output_grid[nr][c]` to the shape color.
5. The gray pixels (color 5) from the input grid do not directly influence the placement of the shape color in the output grid; they are effectively ignored, and their original positions become background color unless overwritten by a projected shape color.
6. Return the final output grid.
"""

def find_shape_color(grid):
    """Finds the primary shape color (most frequent non-zero, non-gray color)."""
    counts = {}
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color != COLOR_BACKGROUND and color != COLOR_OBSTACLE:
                counts[color] = counts.get(color, 0) + 1
    
    if not counts:
        return None # No shape color found

    # Find the color with the maximum count
    shape_color = max(counts, key=counts.get)
    return shape_color

def transform(input_grid):
    """
    Applies the transformation rule: projects the shape color downwards from each
    of its initial positions to the bottom of the grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Identify the shape color
    shape_color = find_shape_color(input_np)

    # Handle cases where no shape color is found (e.g., grid is all background or gray)
    if shape_color is None:
        return np.zeros_like(input_np).tolist() # Return grid of background color

    # 2. Initialize output grid with background color
    output_np = np.full_like(input_np, COLOR_BACKGROUND)

    # 3. Find all locations of the shape color
    shape_locations = []
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == shape_color:
                shape_locations.append((r, c))

    # 4. Project shape color downwards for each location
    for r_start, c in shape_locations:
        for nr in range(r_start, height): # Iterate from starting row to bottom
            # Set the pixel in the output grid to the shape color
            output_np[nr, c] = shape_color
            
    # 5. Gray pixels are implicitly handled by starting with a background grid.

    # 6. Return the final output grid
    return output_np.tolist()

```
