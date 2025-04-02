
## train_1

**input:**
```
0 6 6 6 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 6 6 6 0 0 6 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 6 6 6 0 6 6 6 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 6 6 6 0 0 0 6 0 0 0 0 6 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 0 0 6 6 6 0 0 6 6 6 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The task operates on single-row grids containing primarily white (0) pixels and some magenta (6) pixels.
    *   The core pattern involves sequences of three consecutive magenta pixels (`6 6 6`) and isolated single magenta pixels (`0 6 0`).
    *   The transformation replaces isolated magenta pixels with the three-pixel sequence.
    *   Existing three-pixel sequences in the input are preserved in the output.

*   **YAML Facts:**
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # Effectively 1D as inputs are single rows
    colors_present:
      - white (0)
      - magenta (6)
    objects:
      - type: sequence
        color: magenta (6)
        value: [6, 6, 6]
        behavior: preserved if present in input
      - type: isolated_pixel
        color: magenta (6)
        context: surrounded by white (0) pixels (pattern [0, 6, 0])
        behavior: transformed
    transformation:
      action: replacement
      target: isolated_pixel (magenta 6)
      replacement_pattern: sequence [6, 6, 6]
      placement_rule: The replacement sequence [6, 6, 6] overwrites the original [0, 6, 0] pattern centered on the original isolated pixel's position.
    background_color: white (0)
    grid_size_change: none
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input row to serve as the output row.
    2.  Iterate through the input row, examining each pixel from the second position up to the second-to-last position. Let the current index be `i`.
    3.  Check if the pattern `[white, magenta, white]` (i.e., `[0, 6, 0]`) exists starting at index `i-1` in the *input* row.
    4.  If this pattern is found, modify the *output* row by setting the pixels at indices `i-1`, `i`, and `i+1` to magenta (6).
    5.  After checking all relevant positions, return the modified output row.
```python
import numpy as np # Use numpy for easier array manipulation if needed, though list slicing might suffice

"""
Transforms a single-row input grid by replacing isolated magenta pixels 
(pattern [white, magenta, white] or [0, 6, 0]) with a sequence of three 
magenta pixels ([magenta, magenta, magenta] or [6, 6, 6]). Existing sequences 
of three magenta pixels are preserved.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A list containing a single list which represents the input row.

    Returns:
        list of lists: A list containing a single list which represents the transformed output row.
    """
    # Ensure input is a list of lists and extract the single row
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
         raise ValueError("Input must be a list containing at least one list (row)")
    input_row = input_grid[0]
    
    # Initialize output_row as a copy of the input_row
    output_row = list(input_row)
    row_length = len(input_row)

    # Iterate through the input row to find the pattern [0, 6, 0]
    # We need to check indices i-1, i, and i+1, so the loop runs from 1 to length-2
    for i in range(1, row_length - 1):
        # Check if the pattern [white, magenta, white] exists in the *original* input row
        if input_row[i-1] == 0 and input_row[i] == 6 and input_row[i+1] == 0:
            # If the pattern is found, modify the *output* row
            # Replace the [0, 6, 0] pattern with [6, 6, 6]
            output_row[i-1] = 6
            output_row[i] = 6
            output_row[i+1] = 6
            
            # Optional optimization: Skip the next two indices as they are now part of the replaced sequence
            # and cannot be the center of another isolated '6'. However, the current logic works
            # correctly even without this skip, as the original input_row is used for pattern checking.

    # Return the modified row wrapped in a list of lists format
    return [output_row]

```
