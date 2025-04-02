
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
```python
import numpy as np
import collections

"""
Construct an output row by placing a 3-pixel pattern based on positions identified in the input row.

1.  Accept the input grid (which is a 1xN 2D array). Extract the single row for processing.
2.  Determine the dimensions (length `N`) of the input row.
3.  Initialize a new output row of length `N` filled entirely with white pixels (0).
4.  Identify the primary non-white color (`C`) present in the input row.
5.  Scan the input row from left to right to find the first occurrence of three consecutive pixels of color `C`. Record this 3-pixel sequence as the "pattern block" (`P`) and its starting index (`pattern_start_index`).
6.  Copy the pattern block (`P`) into the output row, starting at `pattern_start_index`.
7.  Define the search region in the input row as starting from the index immediately *after* the end of the identified pattern block (`pattern_start_index + 3`).
8.  Scan the input row within this search region. For each position `i`:
    a.  Check if the pixel `input[i]` has color `C`.
    b.  Check if this pixel is isolated horizontally: `input[i-1]` is not `C` (if `i > 0`) AND `input[i+1]` is not `C` (if `i < N-1`).
    c.  If both conditions (a and b) are true, then `i` is a "target index".
9.  For each identified target index `t`:
    a.  Copy the pattern block (`P`) into the output row, starting at index `t`. Ensure the placement respects the row boundary.
10. Return the final output row (formatted as a 1xN 2D array).
"""


def find_primary_color(row):
    """Finds the first non-zero color in the row."""
    for pixel in row:
        if pixel != 0:
            return pixel
    return None # Should not happen based on examples

def find_pattern_block(row, primary_color):
    """
    Finds the start index and the block ([C, C, C]) of the first sequence 
    of three consecutive primary color pixels.
    """
    n = len(row)
    for i in range(n - 2):
        if row[i] == primary_color and row[i+1] == primary_color and row[i+2] == primary_color:
            return i, [primary_color] * 3
    return -1, None # Should not happen based on examples

def find_target_indices(row, primary_color, search_start_index):
    """
    Finds indices of single occurrences of primary_color after search_start_index.
    A single occurrence means its immediate neighbors are not the primary_color.
    """
    target_indices = []
    n = len(row)
    for i in range(search_start_index, n):
        if row[i] == primary_color:
            # Check left neighbor (handle boundary and start of search)
            left_is_primary = (i > 0 and row[i-1] == primary_color)
            # Check right neighbor (handle boundary)
            right_is_primary = (i < n - 1 and row[i+1] == primary_color)
            
            if not left_is_primary and not right_is_primary:
                target_indices.append(i)
    return target_indices

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    
    Args:
        input_grid: A list of lists representing the input grid (expected 1xN).

    Returns:
        A list of lists representing the transformed output grid (1xN).
    """
    # Convert input to numpy array and extract the single row
    input_array = np.array(input_grid, dtype=int)
    if input_array.shape[0] != 1:
        # Handle unexpected input shape if necessary, though ARC grids are 2D
        # For this task, we strictly expect a 1xN grid.
        raise ValueError("Input grid must have exactly one row.")
        
    input_row = input_array[0]
    n = len(input_row)

    # Initialize output grid (1xN) filled with white (0)
    output_array = np.zeros_like(input_array)
    output_row = output_array[0] # Get a view of the output row for modification

    # Identify primary color
    primary_color = find_primary_color(input_row)
    if primary_color is None:
        return output_array.tolist() # Return blank grid if no color found

    # Find the pattern block and its start index in the input
    pattern_start_index, pattern_block = find_pattern_block(input_row, primary_color)
    if pattern_start_index == -1:
        # If no pattern block found, return the blank grid (or handle as error)
        # Based on examples, pattern block always exists.
        return output_array.tolist() 
        
    pattern_length = len(pattern_block)
    pattern_end_index = pattern_start_index + pattern_length # index *after* the pattern

    # Copy the initial pattern block to the output row
    if pattern_start_index + pattern_length <= n:
        output_row[pattern_start_index : pattern_end_index] = pattern_block
    else:
         # Handle cases where pattern doesn't fit (unlikely based on constraints/examples)
        pass 

    # Define the search start index for target pixels (after the initial pattern)
    search_start_index = pattern_end_index 

    # Find target indices in the input row
    target_indices = find_target_indices(input_row, primary_color, search_start_index)

    # Copy the pattern block to the output row at each target index
    for t_index in target_indices:
        # Ensure the placement fits within the grid boundaries
        if t_index + pattern_length <= n:
            output_row[t_index : t_index + pattern_length] = pattern_block
        else:
            # Handle cases where pattern doesn't fit (unlikely based on constraints/examples)
            # Option 1: Truncate pattern (less likely)
            # Option 2: Don't place if it doesn't fit (more likely)
            # Option 3: Error (if constraints guarantee fit)
            # Based on examples, it seems to always fit.
            pass 

    # Return the modified output grid as a list of lists
    return output_array.tolist()
```
```python
import numpy as np

"""
Constructs an output row by placing copies of an initial 3-pixel pattern based on locations identified in the input row.

1.  Accepts the input grid (a single row).
2.  Initializes a new output row of the same length filled with white (0).
3.  Identifies the primary non-white color (C).
4.  Finds the starting index (idx_p) and the sequence [C, C, C] (pattern block P) of the first occurrence of three consecutive pixels of color C in the input.
5.  Places the pattern block P into the output row starting at idx_p.
6.  Identifies all indices (t) in the input row *after* the initial pattern block where the pixel has color C and is horizontally isolated (neighbors are not C). These are target marker indices.
7.  For each target marker index t, calculates the output placement start index as t-1.
8.  Places a copy of the pattern block P into the output row starting at this calculated index (t-1), ensuring it fits within boundaries.
9.  Returns the constructed output row.
"""

def find_primary_color(row):
    """Finds the first non-zero (non-white) color in the row."""
    for pixel in row:
        if pixel != 0:
            return pixel
    return None # Should not happen based on examples, but good practice

def find_pattern_block(row, primary_color):
    """
    Finds the start index and the block ([C, C, C]) of the first sequence 
    of three consecutive primary color pixels.
    Returns (start_index, pattern_block_list) or (-1, None) if not found.
    """
    n = len(row)
    for i in range(n - 2):
        if row[i] == primary_color and row[i+1] == primary_color and row[i+2] == primary_color:
            return i, [primary_color] * 3
    return -1, None # Pattern block not found

def find_target_indices(row, primary_color, search_start_index):
    """
    Finds indices of single occurrences of primary_color at or after search_start_index.
    A single occurrence means its immediate neighbors are not the primary_color.
    """
    target_indices = []
    n = len(row)
    # Ensure search_start_index is within bounds
    if search_start_index >= n:
        return target_indices
        
    for i in range(search_start_index, n):
        if row[i] == primary_color:
            # Check left neighbor (handle boundary and start of search)
            left_is_primary = (i > 0 and row[i-1] == primary_color)
            # Check right neighbor (handle boundary)
            right_is_primary = (i < n - 1 and row[i+1] == primary_color)
            
            # Check if it's isolated
            if not left_is_primary and not right_is_primary:
                target_indices.append(i)
    return target_indices

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    
    Args:
        input_grid: A list of lists representing the input grid (expected 1xN).

    Returns:
        A list of lists representing the transformed output grid (1xN).
    """
    # 1. Accept input grid and extract the row
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
         raise ValueError("Input grid must be a non-empty list of lists.")
    if len(input_grid) != 1:
       # This task specifically deals with 1-row grids based on examples
       # Adjust if multi-row grids with this pattern are possible
       raise ValueError("Input grid must have exactly one row for this task.")
       
    input_row = np.array(input_grid[0], dtype=int)
    n = len(input_row)

    # 2. Initialize output row with background color (0)
    output_row = np.zeros(n, dtype=int)

    # 3. Identify primary color
    primary_color = find_primary_color(input_row)
    if primary_color is None:
        # If input is all white, output is all white
        return [output_row.tolist()] 

    # 4. Find the initial pattern block and its start index
    pattern_start_index, pattern_block = find_pattern_block(input_row, primary_color)
    if pattern_start_index == -1:
        # If no pattern block found, something is wrong based on examples, 
        # but returning the blank grid might be safest.
        # Consider raising an error if the pattern is guaranteed.
        return [output_row.tolist()] 
        
    pattern_length = len(pattern_block)
    
    # 5. Place the initial pattern block in the output row
    # Check boundaries: ensure pattern fits from the start index
    if pattern_start_index + pattern_length <= n:
        output_row[pattern_start_index : pattern_start_index + pattern_length] = pattern_block
    else:
        # Handle error or unexpected case: initial pattern doesn't fit
        # For now, place what fits (though unlikely based on examples)
        fit_length = n - pattern_start_index
        if fit_length > 0:
             output_row[pattern_start_index : n] = pattern_block[:fit_length]

    # 6. Define search region start index (after the initial block)
    search_start_index = pattern_start_index + pattern_length 

    # 7. Find target marker indices in the input row
    target_indices = find_target_indices(input_row, primary_color, search_start_index)

    # 8. For each target marker index, place the pattern block in the output
    for t_index in target_indices:
        # a. Calculate placement start index for output
        output_idx = t_index - 1 
        
        # b. Place pattern block, checking boundaries
        if output_idx >= 0 and output_idx + pattern_length <= n:
            output_row[output_idx : output_idx + pattern_length] = pattern_block
        # Optional: Handle cases where pattern doesn't fit due to edge placement
        # else: print(f"Warning: Pattern placement skipped for target {t_index} due to boundary.") 
        # (Examples suggest this won't happen)

    # 9. Return the constructed output row (wrapped in a list for 2D grid format)
    return [output_row.tolist()]
```
