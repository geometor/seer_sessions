
## train_1

**input:**
```
0 3 3 3 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 3 3 3 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 9 9 9 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 9 9 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 5 5 5 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Perception of Elements:**

1.  **Grid Structure:** The input and output are both single-row grids (effectively 1D arrays). The dimensions appear consistent across examples (1x33).
2.  **Colors:** The primary background color is white (0). Each input contains exactly two distinct non-white colors.
3.  **Objects in Input:**
    *   There is always a contiguous block of three identical non-white pixels (e.g., green-green-green, maroon-maroon-maroon, gray-gray-gray).
    *   There is always a single isolated non-white pixel of a different color (e.g., maroon, gray, azure), located to the right of the three-pixel block.
    *   These non-white elements are separated by one or more white pixels.
4.  **Transformation:**
    *   The three-pixel block from the input remains unchanged in the output.
    *   The single isolated pixel in the input is "expanded" in the output. It becomes the starting pixel of a new three-pixel block of the *same* color as the original single pixel. This expansion occurs horizontally to the right.
    *   All white pixels remain white, except for the two pixels immediately to the right of the original single pixel, which are overwritten by the expansion.
5.  **Irrelevance:** The specific colors or the relative positions (beyond the single pixel being to the right of the triple block) of the non-white elements don't seem to affect the *type* of transformation, only *which* color is used for the expansion and *where* it occurs. The three-pixel block seems entirely unaffected and potentially irrelevant to the core transformation logic applied to the single pixel. The core operation focuses solely on the single pixel.

**Facts:**


```yaml
Grid:
  Type: 1D Array / Single Row Grid
  Dimensions: 1x33 (constant in examples)
  Background_Color: white (0)

Input_Objects:
  - Name: Source_Object # Note: This object appears irrelevant to the transformation logic observed.
    Type: Contiguous Block
    Shape: 1x3 pixels
    Color: Any non-white (variable, e.g., green, maroon, gray)
    Quantity: 1
  - Name: Target_Pixel
    Type: Single Pixel
    Shape: 1x1 pixel
    Color: Any non-white (variable, different from Source_Object, e.g., maroon, gray, azure)
    Quantity: 1
    Position: To the right of Source_Object, separated by white pixels.

Relationships:
  - Target_Pixel is located at a column index greater than any column index of the Source_Object.
  - Source_Object and Target_Pixel are separated by at least one white pixel.

Transformation:
  Action: Expansion
  Target: The Target_Pixel
  Rule:
    1. Identify the position (row 0, column X) and color (C) of the Target_Pixel.
    2. In the output grid, modify the pixels at (0, X), (0, X+1), and (0, X+2) to color C.
  Effect: The Target_Pixel becomes the leftmost pixel of a new 1x3 block of color C.
  Unaffected_Elements:
    - Source_Object
    - All white pixels not overwritten by the expansion.
```


**Natural Language Program:**

1.  Start with the input grid (a single row).
2.  Scan the grid to find the single, isolated non-white pixel (the "target pixel"). Record its color (let's call it `target_color`) and its column position (let's call it `target_col`). Ignore any blocks of three non-white pixels.
3.  Create a new grid (the output grid) initially identical to the input grid.
4.  In the output grid, set the color of the pixel at column `target_col` to `target_color`.
5.  Set the color of the pixel at column `target_col + 1` to `target_color`.
6.  Set the color of the pixel at column `target_col + 2` to `target_color`.
7.  The resulting grid is the final output.
```python
"""
1.  Start with the input grid (a single row).
2.  Scan the grid to find the single, isolated non-white pixel (the "target pixel"). 
    An isolated pixel is defined as a non-white pixel whose immediate left and right neighbors are white (or grid boundaries).
3.  Record the color of the target pixel (`target_color`) and its column position (`target_col`). 
    Ignore any blocks of three non-white pixels or other non-isolated pixels.
4.  Create a new grid (the output grid) initially identical to the input grid.
5.  In the output grid, set the color of the pixel at column `target_col` to `target_color`.
6.  Set the color of the pixel at column `target_col + 1` to `target_color`.
7.  Set the color of the pixel at column `target_col + 2` to `target_color`. 
    Assume there is always enough space to the right based on examples.
8.  The resulting grid is the final output.
"""

import numpy as np

def find_isolated_pixel(grid):
    """
    Finds the first single, isolated non-white pixel in a 1-row grid.
    An isolated pixel has white (0) neighbors (or is at a boundary).

    Args:
        grid (np.array): A 1xN numpy array representing the input grid row.

    Returns:
        tuple: (row, col, color) of the isolated pixel, or None if not found.
               Since it's a 1-row grid, row will always be 0.
    """
    if grid.shape[0] != 1:
        # This function assumes a 1-row grid based on the examples
        # Handle potential multi-row grids if necessary, though unlikely for this task
        print("Warning: Expected a 1-row grid.")
        return None # Or adapt logic for multi-row

    row = 0
    width = grid.shape[1]
    for col in range(width):
        color = grid[row, col]
        if color != 0: # Found a non-white pixel
            # Check left neighbor (or boundary)
            is_left_white = (col == 0) or (grid[row, col - 1] == 0)
            # Check right neighbor (or boundary)
            is_right_white = (col == width - 1) or (grid[row, col + 1] == 0)

            if is_left_white and is_right_white:
                # This is the isolated pixel
                return row, col, color
    return None # No isolated pixel found

def transform(input_grid):
    """
    Transforms the input grid by finding a single isolated non-white pixel
    and expanding it into a 1x3 block of the same color.

    Args:
        input_grid (np.array): A 1xN numpy array representing the input grid.

    Returns:
        np.array: The transformed grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Find the target isolated pixel
    target_info = find_isolated_pixel(input_grid)

    if target_info:
        row, target_col, target_color = target_info

        # Apply the transformation: expand the pixel to a 1x3 block
        # The pixel itself is already the correct color in the copy
        # We just need to color the next two pixels to the right
        # Ensure we don't go out of bounds (though examples suggest it's safe)
        if target_col + 1 < width:
            output_grid[row, target_col + 1] = target_color
        if target_col + 2 < width:
            output_grid[row, target_col + 2] = target_color
            
    # If no isolated pixel is found, the grid remains unchanged (per the copy)
    return output_grid

```
