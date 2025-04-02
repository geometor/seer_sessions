
## train_1

**input:**
```
0 4 4 4 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 4 4 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 1 1 1 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 1 1 1 0 0 0 1 1 1 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 8 8 8 0 0 0 0 8 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 8 8 0 0 0 8 8 8 0 8 8 8 0 0 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task operates on single-row grids (1xN). Each example uses white (0) as a background color and one other color (yellow, blue, or azure). The transformation involves modifying sequences of the non-white color. Specifically, isolated non-white pixels (pixels surrounded by white pixels on both sides) are expanded horizontally into a sequence of three identical pixels, overwriting the adjacent white pixels. Existing sequences of three or more non-white pixels remain unchanged.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_dimensionality: 1D # All examples are single rows
    background_color: 0 # White
    objects:
      - type: pixel_sequence
        color: non-white # Yellow (4), Blue (1), Azure (8) in examples
        properties:
          - length: Integer (number of contiguous pixels)
          - position: Start and end indices
          - context: Neighboring pixels (especially if they are white)
    transformation:
      action: conditional_expansion
      target: isolated_pixels # Non-white pixels with white neighbors on both sides
      condition: pixel is non-white AND left_neighbor is white AND right_neighbor is white
      effect: replace the sequence [white, pixel, white] with [pixel, pixel, pixel]
      preservation: non-white pixel sequences of length >= 3 are unchanged
    output_grid: Same dimensions as input, modified according to the transformation rule.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each pixel of the input grid from the second pixel (index 1) up to the second-to-last pixel (index width-2).
    3.  For the current pixel at index `i`:
        a.  Check if the pixel is non-white (value > 0).
        b.  Check if the pixel to its left (index `i-1`) is white (value 0).
        c.  Check if the pixel to its right (index `i+1`) is white (value 0).
    4.  If all three conditions (non-white current pixel, white left neighbor, white right neighbor) are true:
        a.  Get the color of the current pixel.
        b.  Set the pixel at index `i-1` in the output grid to this color.
        c.  Set the pixel at index `i` in the output grid to this color.
        d.  Set the pixel at index `i+1` in the output grid to this color.
    5.  Return the modified output grid.
```python
import copy

"""
Transforms a 1D input grid by expanding isolated non-white pixels.

An isolated non-white pixel is defined as a pixel with a value greater than 0 
that has white (0) pixels immediately to its left and right.

When such an isolated pixel is found at index 'i', the sequence of three pixels 
[white (i-1), non-white (i), white (i+1)] in the input grid is replaced by 
[non-white (i), non-white (i), non-white (i)] in the output grid, using the 
color of the original pixel at index 'i'.

Pixels at the edges (index 0 and index width-1) cannot be the center of 
such a sequence and are therefore never expanded. Existing sequences of 
non-white pixels (length >= 2) are not affected by this rule unless they 
contain an isolated pixel satisfying the condition within a larger white gap.
"""

def transform(input_grid):
    """
    Applies the isolated pixel expansion transformation to a 1D grid.

    Args:
        input_grid: A list of lists representing the 1xN input grid.

    Returns:
        A list of lists representing the 1xN output grid after transformation.
    """
    # Ensure the input is treated as a 1D array (list of lists with one row)
    if not input_grid or len(input_grid) != 1:
         # Handle invalid input if necessary, or assume valid 1xN grid
         # For now, proceed assuming input_grid[0] is the row data
         pass # Or raise an error, depending on expected robustness

    input_row = input_grid[0]
    width = len(input_row)

    # Initialize output_grid as a deep copy of the input_grid
    # Working on a copy prevents modifying the input directly and avoids issues
    # where a change affects subsequent checks in the same iteration.
    output_grid = copy.deepcopy(input_grid)
    output_row = output_grid[0]

    # Iterate through the pixels, checking for the isolated non-white pattern
    # We only need to check indices from 1 up to width-2, as the pattern requires
    # neighbors on both sides.
    for i in range(1, width - 1):
        # Get the current pixel and its left and right neighbors from the original input
        current_pixel_color = input_row[i]
        left_neighbor_color = input_row[i-1]
        right_neighbor_color = input_row[i+1]

        # Check the condition: non-white pixel surrounded by white pixels
        if current_pixel_color > 0 and left_neighbor_color == 0 and right_neighbor_color == 0:
            # Apply the transformation to the output grid
            # Replace the [white, pixel, white] sequence with [pixel, pixel, pixel]
            output_row[i-1] = current_pixel_color
            output_row[i]   = current_pixel_color
            output_row[i+1] = current_pixel_color
            # Note: We continue iterating. If the expansion creates a new pattern,
            # it won't be caught in this pass because we read from the *original*
            # input_row. This matches the observed behavior in examples where
            # expansions don't chain reaction within a single transform step.

    return output_grid
```
