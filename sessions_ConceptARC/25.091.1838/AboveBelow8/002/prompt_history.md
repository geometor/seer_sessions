
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

*   **Perception**: The task involves filtering the input grid based on pixel color. Each input grid contains various colored pixels, including a significant number of azure (8) pixels, often interspersed within or forming patterns across other colored regions. The corresponding output grid retains only the azure (8) pixels in their original positions, while all other pixels are replaced with the background color, white (0). The dimensions of the grid remain unchanged. The transformation acts as a selective filter, isolating the azure pixels against a uniform white background.

*   **YAML Facts**:
    
```yaml
    task_context:
      grid_dimensions: Consistent between input and output.
      background_color_input: Variable (white (0) in examples 1 and 3, none explicit in example 2).
      background_color_output: Consistently white (0).
    objects:
      - type: pixel_groups
        properties:
          - color: Various colors present in input (e.g., green-3, magenta-6, orange-7, yellow-4, red-2, maroon-9, blue-1, azure-8, white-0).
          - special_color: Azure (8) is the key color.
    relationships:
      - type: positional_invariance
        description: The azure (8) pixels maintain their exact (row, column) coordinates from the input to the output grid.
    actions:
      - type: filter
        input: Input grid
        output: Output grid
        rule: Keep only pixels with azure (8) color.
      - type: replace
        target_pixels: All pixels that are NOT azure (8).
        replacement_color: White (0).
        condition: Apply to all non-azure pixels in the input grid to produce the output grid.

    ```


*   **Natural Language Program**:
    1.  Initialize an output grid with the same dimensions as the input grid, filling it entirely with the white (0) color.
    2.  Iterate through each pixel of the input grid at every row and column position.
    3.  Check the color of the current pixel in the input grid.
    4.  If the color of the input pixel is azure (8), set the color of the pixel at the corresponding position in the output grid to azure (8).
    5.  If the color of the input pixel is any color other than azure (8), leave the corresponding pixel in the output grid as white (0).
    6.  Return the completed output grid.
```python
"""
Create an output grid of the same dimensions as the input grid, initialized with the background color white (0). Iterate through each pixel of the input grid. If a pixel's color is azure (8), copy its color to the corresponding position in the output grid. Otherwise, leave the output grid pixel as white (0). Return the final output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Filters the input grid to keep only azure (8) pixels, replacing all others with white (0).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid with only azure pixels preserved.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize an output grid of the same dimensions with white (0)
    output_grid = np.zeros((height, width), dtype=int)

    # Identify the locations of azure (8) pixels in the input grid
    azure_pixels = (input_grid == 8)

    # Set the corresponding locations in the output grid to azure (8)
    output_grid[azure_pixels] = 8

    return output_grid
```
