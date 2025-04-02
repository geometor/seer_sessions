
## train_1

**input:**
```
0 4 4 4 0 0 0 4 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 4 4 0 0 4 4 4 0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 9 9 9 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 9 9 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 5 5 5 0 0 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 5 5 0 5 5 5 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output grids are single rows (1D arrays).
    *   Each input contains a primary non-white color (e.g., yellow, maroon, gray) interspersed with white (0).
    *   The input starts with a sequence of three consecutive pixels of the primary color, followed by one or more single pixels of the same primary color, separated by white pixels.
    *   The output retains the initial three-pixel block in its original position.
    *   Each subsequent single pixel of the primary color in the input is replaced in the output by a copy of the initial three-pixel block. The replacement block starts at the same position where the single pixel was located in the input.
    *   The primary color remains consistent between the input and output for each example.

*   **YAML Facts:**
    
```yaml
    task_description: Replace specific single pixels with a pattern derived from the beginning of the input row.
    elements:
      - object: grid
        property:
          - type: 1D array (single row)
          - background_color: white (0)
          - primary_color: varies (yellow, maroon, gray)
      - object: pattern_block
        property:
          - location: beginning of the sequence of primary_color pixels
          - composition: three consecutive pixels of the primary_color
          - role: template for replacement
      - object: target_pixel
        property:
          - type: single pixel
          - color: same as primary_color
          - location: appears after the pattern_block in the input row
          - role: placeholder to be replaced
    actions:
      - name: identify_primary_color
        input: input_grid
        output: the non-white color present
      - name: find_pattern_block
        input: input_grid, primary_color
        output: the first sequence of three consecutive primary_color pixels
      - name: find_target_pixels
        input: input_grid, primary_color, pattern_block
        output: list of positions of single primary_color pixels appearing after the pattern_block
      - name: generate_output_grid
        based_on: input_grid, pattern_block, target_pixel_positions
        steps:
          - Initialize output grid as a copy of the input grid (or all white).
          - Place the pattern_block at its original position in the output grid.
          - For each target_pixel position:
            - Place a copy of the pattern_block into the output grid, starting at that target_pixel position.
    relationships:
      - type: spatial
        description: The pattern_block always appears before the target_pixels in the input row.
      - type: identity
        description: The color of the pattern_block and the target_pixels is the same (primary_color).
      - type: transformation
        description: Target_pixels in the input are replaced by the pattern_block in the output. The starting position is preserved.
    ```


*   **Natural Language Program:**
    1.  Identify the primary non-white color (`C`) present in the input row.
    2.  Scan the input row from left to right to find the first occurrence of three consecutive pixels of color `C`. This is the "pattern block" (`P`).
    3.  Initialize the output row as a copy of the input row (or as an all-white row of the same length).
    4.  Place the identified pattern block (`P`) into the output row at the same starting position it had in the input row.
    5.  Continue scanning the input row from the position immediately *after* the pattern block.
    6.  For each position `i` encountered *after* the pattern block:
        a.  If the pixel at position `i` in the input row has the color `C` AND it is a single occurrence (i.e., `input[i-1]` is not `C` and `input[i+1]` is not `C`, considering boundary conditions), then it is a "target pixel".
        b.  Replace the pixel(s) in the output row starting at position `i` with the pattern block (`P`). Ensure the pattern block fits within the grid boundaries if placed starting at `i`. (Note: Based on examples, the replacement overwrites existing pixels, and the pattern block is always 3 pixels long).
    7.  Return the modified output row.
```python
import numpy as np
import collections

"""
Identifies the primary non-white color (C) in the input row.
Finds the first sequence of three consecutive pixels of color C (the pattern block P).
Initializes the output row as a copy of the input row.
Scans the input row after the pattern block.
For each single pixel of color C found after the pattern block (where its immediate neighbors are not C), 
replaces the corresponding three pixels in the output row, starting at the single pixel's position, with the pattern block P.
"""

def find_primary_color(grid):
    """Finds the first non-zero color in the grid."""
    for pixel in grid:
        if pixel != 0:
            return pixel
    return None # Should not happen based on examples

def find_pattern_block(grid, primary_color):
    """Finds the start index of the first sequence of three consecutive primary color pixels."""
    n = len(grid)
    for i in range(n - 2):
        if grid[i] == primary_color and grid[i+1] == primary_color and grid[i+2] == primary_color:
            return i, [primary_color] * 3
    return -1, None # Should not happen based on examples

def transform(input_grid_list):
    """
    Transforms the input grid according to the rule.
    
    Args:
        input_grid_list: A list representing the single row input grid.

    Returns:
        A list representing the single row output grid.
    """
    # Convert list to numpy array for easier manipulation if needed, though list ops are fine here.
    input_grid = np.array(input_grid_list)
    output_grid = np.copy(input_grid)
    n = len(input_grid)

    # 1. Identify the primary non-white color (C)
    primary_color = find_primary_color(input_grid)
    if primary_color is None:
        return output_grid.tolist() # Return copy if no primary color found

    # 2. Find the first sequence of three consecutive pixels of color C (the pattern block P)
    pattern_start_index, pattern_block = find_pattern_block(input_grid, primary_color)
    if pattern_start_index == -1:
        # If no pattern block found, return the original grid (or handle as error)
        # Based on examples, pattern block always exists.
        return output_grid.tolist() 
        
    pattern_end_index = pattern_start_index + 2 # Inclusive end index of the pattern

    # 3. Initialize the output row as a copy of the input row (already done)

    # 4. Scan the input row starting *after* the pattern block.
    # 5. Find target pixels (single occurrences of C)
    # 6. Apply transformation
    for i in range(pattern_end_index + 1, n):
        if input_grid[i] == primary_color:
            # Check if it's a single occurrence
            is_single = True
            # Check left neighbor (handle boundary)
            if i > 0 and input_grid[i-1] == primary_color:
                is_single = False
            # Check right neighbor (handle boundary)
            if i < n - 1 and input_grid[i+1] == primary_color:
                is_single = False
                
            if is_single:
                # This is a target pixel. Replace output segment with the pattern block.
                # Ensure the replacement does not go out of bounds.
                if i + len(pattern_block) <= n:
                    output_grid[i : i + len(pattern_block)] = pattern_block
                # else: Handle cases where pattern doesn't fit (optional based on ARC constraints)
                # Based on examples, pattern always fits.

    # Return the modified output row as a list
    return output_grid.tolist()
```
