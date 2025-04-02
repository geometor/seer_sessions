
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 6 6 6 6 0 0
0 0 4 3 4 0 6 8 6 6 6 6
0 0 3 3 3 0 8 8 8 6 6 6
0 0 4 3 4 0 6 8 6 6 0 0
0 0 4 4 4 0 6 6 6 6 0 0
0 3 3 3 3 0 0 7 7 7 7 7
0 3 2 2 3 0 0 7 4 4 7 7
0 3 2 2 3 0 0 7 4 7 7 7
0 3 3 3 3 0 0 7 4 4 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 8 0 0 0 0
0 0 3 3 3 0 8 8 8 0 0 0
0 0 0 3 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 9 9 9 9 9
0 0 0 0 0 0 0 9 4 4 4 9
0 1 1 1 1 0 0 9 4 4 9 9
0 1 6 6 1 0 0 9 4 9 9 9
0 1 6 1 1 1 0 9 4 4 4 9
0 1 6 6 1 1 0 9 9 9 9 9
0 1 1 1 1 0 0 0 3 3 3 3
0 0 0 0 7 7 7 0 3 1 1 3
0 0 0 7 7 3 3 0 3 1 3 3
0 0 0 7 7 3 7 0 3 1 1 3
0 0 0 7 7 3 3 0 3 1 3 3
0 0 0 0 7 7 7 0 3 1 1 3
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0 0
0 0 5 5 5 5 6 6 6 6 0 0
5 5 5 4 4 5 6 3 3 6 0 0
5 5 5 4 4 5 6 3 3 6 0 0
5 5 5 4 4 5 6 6 6 6 0 0
5 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 7 8 8 7 7
0 0 0 0 0 0 0 7 8 8 7 7
0 0 0 0 0 0 0 7 8 8 7 7
0 0 0 0 0 0 0 7 7 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain multiple distinct objects composed of contiguous blocks of non-white pixels, set against a white background.
    *   These objects often consist of an outer "frame" of one color surrounding an inner "core" of a different color(s). Some objects might be solid blocks of a single color.
    *   The output grids are mostly white, retaining only specific pixels from the input grid.
    *   The pixels retained in the output correspond to the "core" pixels from certain input objects.
    *   The transformation appears to involve identifying pixels that are completely surrounded by other non-white pixels (i.e., not adjacent to any white pixels, including diagonally) and preserving only those pixels in their original positions. All other pixels, including the "frames" and solid objects, become white.

*   **Facts:**
    
```yaml
    elements:
      - type: background
        color: white (0)
      - type: object
        description: Contiguous block(s) of non-white pixels.
        properties:
          - May have an outer frame color and an inner core color.
          - May be a solid color.
      - type: pixel
        properties:
          - color: (integer 0-9)
          - position: (row, column)
          - neighbors: Set of 8 adjacent pixels (including diagonals).
    transformation:
      action: filter_pixels
      condition: A pixel is kept in the output grid if and only if all of its 8 neighboring pixels (including diagonals) in the input grid are non-white (not color 0).
      output_generation:
        - Create an output grid of the same dimensions as the input, initialized to white (0).
        - For each pixel in the input grid that meets the condition (all 8 neighbors are non-white), place that pixel's color at the corresponding position in the output grid.
    ```


*   **Natural Language Program:**
    1.  Initialize a new grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
    2.  Iterate through each pixel of the input grid, excluding pixels on the border (as they cannot be fully surrounded).
    3.  For each non-border pixel, check its 8 neighbors (up, down, left, right, and the four diagonals).
    4.  If the current pixel is not white AND *all* of its 8 neighbors are also not white (color is not 0), then copy the color of this current pixel to the corresponding position in the new grid.
    5.  All other positions in the new grid remain white.
    6.  The resulting new grid is the output.
```python
import numpy as np

"""
Identify pixels in the input grid that are completely surrounded by non-white pixels.
Specifically, a pixel is kept if and only if it and all of its 8 immediate neighbors (including diagonals) are non-white (not color 0). 
All other pixels are set to white (0) in the output grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by keeping only pixels that are fully surrounded by non-white pixels.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Iterate through each pixel of the input grid, excluding the border pixels
    # Border pixels cannot be fully surrounded by 8 neighbors within the grid.
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Check if the current pixel itself is non-white
            if input_grid[r, c] == 0:
                continue # Skip if the center pixel is white

            # Extract the 3x3 neighborhood around the current pixel
            neighborhood = input_grid[r-1 : r+2, c-1 : c+2]

            # Check if *all* pixels in the 3x3 neighborhood are non-white (not 0)
            # np.all returns True if all elements evaluate to True (non-zero in this context)
            if np.all(neighborhood != 0):
                # If all neighbors (and the center) are non-white,
                # copy the color of the current pixel to the output grid
                output_grid[r, c] = input_grid[r, c]

    # Return the resulting output grid
    return output_grid
```
