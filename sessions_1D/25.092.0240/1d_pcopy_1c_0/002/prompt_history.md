
## train_1

**input:**
```
0 0 1 1 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 1 1 1 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 3 3 3 0 0 0 0 3 0 0 0 0 0 3 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 3 3 3 0 0 0 3 3 3 0 0 0 3 3 3 0 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 7 7 7 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 7 7 7 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The inputs and outputs are 1-dimensional grids (or rows).
    *   Each grid contains mostly white pixels (0) and some pixels of a single non-white color (blue=1, green=3, or orange=7).
    *   The non-white pixels appear either as isolated single pixels or as contiguous horizontal lines of three pixels.
    *   In the output grid, the original lines of three non-white pixels are preserved.
    *   Each isolated non-white pixel in the input grid is expanded into a horizontal line of three pixels of the same color in the output grid. This expansion is centered on the original pixel's position, changing the pixel itself and its immediate left and right neighbors (if they exist within the grid bounds) to the non-white color.
    *   White pixels remain white unless they are adjacent to an isolated non-white pixel and become part of the expanded 3-pixel line.

*   **Facts:**
    
```yaml
    task_type: grid_transformation_1d
    grid_dimensionality: 1
    background_color: white (0)
    objects:
      - type: pixel
        properties:
          - color: non-white (1, 3, or 7 in examples)
          - configuration: 
              - isolated (white neighbors on both sides)
              - part_of_line (at least one neighbor has the same non-white color)
      - type: pixel
        properties:
          - color: white (0)
    actions:
      - name: expand_pixel
        input: isolated non-white pixel at index i
        output: change pixels at indices i-1, i, i+1 to the non-white color
        constraints: apply within grid boundaries
      - name: copy_pixel
        input: 
          - white pixel
          - non-white pixel that is part_of_line
        output: pixel with the same color at the same index
    relationships:
      - type: adjacency
        description: Pixels to the immediate left and right (index i-1 and i+1) are relevant for determining if a pixel is isolated.
    transformation_rule:
      - Identify the primary non-white color (C).
      - Create an output grid initialized as a copy of the input grid.
      - Iterate through each pixel of the input grid at index i.
      - If the pixel at index i has color C and its neighbors at i-1 and i+1 (within bounds) are white (0), then it's an 'isolated pixel'.
      - For each identified isolated pixel at index i with color C:
          - Set the pixel at index i in the output grid to C.
          - If i > 0, set the pixel at index i-1 in the output grid to C.
          - If i < grid_length - 1, set the pixel at index i+1 in the output grid to C.
      - Pixels that are not isolated non-white pixels, and white pixels not overwritten by expansion, retain their original color in the output grid.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Determine the primary non-white color (let's call it `object_color`) present in the input grid.
    3.  Iterate through each cell (pixel) of the input grid using its index `i`.
    4.  For each cell at index `i`:
        a.  Check if the color of the cell is `object_color`.
        b.  If it is `object_color`, check if its left neighbor (at `i-1`) and right neighbor (at `i+1`) are both white (color 0). Handle boundary conditions: if `i` is 0, consider the left neighbor condition met; if `i` is the last index, consider the right neighbor condition met.
        c.  If both neighbors are white (meaning the pixel at `i` is isolated), then modify the *output* grid:
            i.  Set the color of the cell at index `i` in the output grid to `object_color`.
            ii. If `i > 0`, set the color of the cell at index `i-1` in the output grid to `object_color`.
            iii. If `i` is not the last index, set the color of the cell at index `i+1` in the output grid to `object_color`.
    5.  Return the modified output grid.
```python
"""
Transforms a 1D input grid by expanding isolated non-white pixels into 3-pixel horizontal lines.

Specifically:
1. Copies the input grid to an output grid.
2. Identifies the primary non-white color present in the input.
3. Iterates through the input grid.
4. If a pixel has the non-white color and both its left and right neighbors are white (or are outside the grid boundaries), it is considered "isolated".
5. For each isolated pixel found at index i, the corresponding pixels at indices i-1, i, and i+1 in the output grid are set to the non-white color (respecting grid boundaries).
6. Pixels that are not part of an expansion or were already part of a non-white sequence remain unchanged from the initial copy.
"""

import numpy as np

def find_non_white_color(grid):
  """Finds the first non-white color in the grid."""
  for pixel in grid:
    if pixel != 0:
      return pixel
  return None # Return None if grid is all white

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
      input_grid: A list representing the 1D input grid.

    Returns:
      A list representing the transformed 1D output grid.
    """
    # Convert list to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    
    # Handle empty input case
    if input_array.size == 0:
        return []

    # Initialize output_grid as a copy of the input_grid
    output_array = np.copy(input_array)
    width = len(input_array)

    # Determine the primary non-white color
    object_color = find_non_white_color(input_array)

    # If there's no non-white color, return the copy
    if object_color is None:
        return output_array.tolist()

    # Iterate through each cell of the input grid
    for i in range(width):
        # Check if the current pixel is the object color
        if input_array[i] == object_color:
            # Check if it's isolated
            # Check left neighbor (handle boundary)
            is_left_white = (i == 0) or (input_array[i - 1] == 0)
            # Check right neighbor (handle boundary)
            is_right_white = (i == width - 1) or (input_array[i + 1] == 0)

            # If both neighbors are white, it's isolated
            if is_left_white and is_right_white:
                # Modify the output grid: expand the pixel
                # The center pixel (i) is already correct due to the copy
                # Change left neighbor if it exists
                if i > 0:
                    output_array[i - 1] = object_color
                # Change right neighbor if it exists
                if i < width - 1:
                    output_array[i + 1] = object_color

    # Convert back to list before returning
    return output_array.tolist()
```
