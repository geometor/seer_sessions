
## train_1

**input:**
```
0 0 0 3 3 0 3 3 3 0 0 0 3 0 0 3 0 0
```


**output:**
```
0 0 0 4 4 0 8 8 8 0 0 0 6 0 0 6 0 0
```


## train_2

**input:**
```
0 0 3 3 0 3 0 0 3 3 3 0 0 0 3 3 0 0
```


**output:**
```
0 0 4 4 0 6 0 0 8 8 8 0 0 0 4 4 0 0
```


## train_3

**input:**
```
0 0 3 3 3 0 0 0 3 3 0 0 0 3 0 3 0 0
```


**output:**
```
0 0 8 8 8 0 0 0 4 4 0 0 0 6 0 6 0 0
```

*   **Perception of Task Elements:**
    *   The input and output grids are one-dimensional arrays (or single rows).
    *   The input grids contain only white (0) and green (3) pixels.
    *   The output grids contain white (0) pixels and pixels of other colors (yellow=4, magenta=6, azure=8).
    *   The white pixels in the input remain white and in the same position in the output.
    *   The green pixels in the input are replaced by other colors in the output.
    *   Contiguous groups (or "blobs") of green pixels in the input are replaced by a single, uniform color in the output.
    *   The replacement color depends on the size (length) of the contiguous green group in the input.
        *   A green group of size 1 is replaced by magenta (6).
        *   A green group of size 2 is replaced by yellow (4).
        *   A green group of size 3 is replaced by azure (8).

*   **YAML Facts:**
    
```yaml
    task_type: color_transformation
    grid_dimensionality: 1D # or treated as 1xN 2D
    input_colors:
      - white (0)
      - green (3)
    output_colors:
      - white (0)
      - yellow (4)
      - magenta (6)
      - azure (8)
    objects:
      - type: contiguous_group
        color: green (3)
        properties:
          - size (number of pixels)
      - type: background
        color: white (0)
    actions:
      - name: identify_groups
        input: input_grid
        target_color: green (3)
        output: list of green groups (position, size)
      - name: map_color_by_size
        input: green_group
        conditions:
          - if size == 1: output_color = magenta (6)
          - if size == 2: output_color = yellow (4)
          - if size == 3: output_color = azure (8)
      - name: update_grid
        input: input_grid, identified_groups, mapped_colors
        output: output_grid
        logic: Replace pixels of each green group with its corresponding mapped color. Keep white pixels unchanged.
    relationships:
      - The output color of a group depends solely on the size of that group in the input.
      - The positions of non-white pixels are preserved from input to output.
      - White pixels remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid identical to the input grid.
    2.  Iterate through the input grid to identify contiguous horizontal groups of green (3) pixels. Record the starting position and size (length) of each group.
    3.  For each identified green group:
        a.  Determine the size of the group.
        b.  Select a replacement color based on the size:
            *   If size is 1, the replacement color is magenta (6).
            *   If size is 2, the replacement color is yellow (4).
            *   If size is 3, the replacement color is azure (8).
        c.  Update the corresponding segment in the output grid by replacing the original green pixels with the selected replacement color.
    4.  Return the modified output grid. White (0) pixels remain unaffected throughout the process.
```python
import numpy as np

"""
Identifies contiguous horizontal groups of green (3) pixels in the input grid (treated as a single row).
Replaces each green group with a new color based on the group's size (length):
- Size 1: Replace with magenta (6)
- Size 2: Replace with yellow (4)
- Size 3: Replace with azure (8)
White (0) pixels remain unchanged. Assumes input is a 1D list.
"""

def find_contiguous_groups(row, target_color):
    """
    Finds contiguous groups of a target color in a 1D list (row).

    Args:
        row (list): The input row (list of integers).
        target_color (int): The color value to search for groups of.

    Returns:
        list: A list of tuples, where each tuple contains (start_index, length).
    """
    groups = []
    n_cols = len(row)
    col = 0
    while col < n_cols:
        if row[col] == target_color:
            # Found the start of a potential group
            start_col = col
            group_size = 0
            # Count contiguous target_color pixels
            while col < n_cols and row[col] == target_color:
                group_size += 1
                col += 1
            # Record the found group
            groups.append((start_col, group_size))
            # col is already advanced past the group, continue loop from here
        else:
            # Not the target color, move to the next column
            col += 1
    return groups

def map_size_to_color(size):
    """
    Maps the size of a green group to its corresponding output color.

    Args:
        size (int): The number of pixels in the green group.

    Returns:
        int: The mapped color code (6, 4, or 8), or None if size is not 1, 2, or 3.
    """
    if size == 1:
        return 6  # magenta
    elif size == 2:
        return 4  # yellow
    elif size == 3:
        return 8  # azure
    else:
        # According to examples, only sizes 1, 2, 3 are mapped.
        # Return None or handle unexpected sizes as needed. 
        # Based on the examples, other sizes don't seem to occur or map.
        return None 

def transform(input_grid):
    """
    Transforms the input grid row based on the size of contiguous green groups.

    Args:
        input_grid (list): A 1D list representing the input row.

    Returns:
        list: A 1D list representing the transformed output row.
    """
    # Ensure input is treated as a single row (list)
    if isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list):
        # Handle case where input might be [[...]]
         if len(input_grid) == 1:
             row = input_grid[0]
         else:
             # This specific task seems to work on 1D input based on examples.
             # Raise error or handle multi-row input if necessary for generalization.
             raise ValueError("Input grid has unexpected dimensions for this task.")
    elif isinstance(input_grid, list):
         row = input_grid
    else:
        raise TypeError("Input grid must be a list or list of lists.")

    # Initialize output_grid as a copy of the input row
    output_row = list(row)
    
    # Define the target color to find groups of
    target_color = 3 # green

    # Find all contiguous groups of the target color
    green_groups = find_contiguous_groups(row, target_color)

    # Iterate through the identified groups and update the output row
    for start_index, size in green_groups:
        # Determine the replacement color based on group size
        replacement_color = map_size_to_color(size)
        
        # If a valid replacement color is found, update the output row
        if replacement_color is not None:
            for i in range(size):
                output_row[start_index + i] = replacement_color
                
    # Return the modified row
    return output_row
```
