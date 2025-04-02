
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

Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 4 4 4 0 0 0 4 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 4 4 4 0 0 4 4 4 0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 4 4 4 0 0 0 4 4 4 0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 18.75

## Example 2:
Input:
```
0 0 9 9 9 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 9 9 9 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 9 9 9 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 6.25

## Example 3:
Input:
```
0 5 5 5 0 0 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 5 5 5 0 5 5 5 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 5 5 5 0 0 5 5 5 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 12.5
**Assessment and Strategy**

The previous attempt failed because the placement logic for the pattern block was incorrect. The code placed the 3-pixel pattern starting at the index of the single target pixel identified in the input. However, analysis of the expected outputs reveals that the single target pixel in the input actually marks the *middle* position of the 3-pixel pattern in the output. Therefore, the pattern should be placed starting one position *before* the identified target index.

The strategy is to:
1.  Keep the methods for identifying the primary color, the initial 3-pixel pattern block, and the subsequent single target pixels.
2.  Modify the final step: when placing the pattern block corresponding to a target pixel found at index `t`, place it in the output grid starting at index `t-1`.
3.  Ensure the output grid is initialized as white (all zeros) before placing any patterns.

**Metrics**


*code_execution:*
```python
import numpy as np

def find_primary_color(row):
    for pixel in row:
        if pixel != 0:
            return pixel
    return None

def find_pattern_block(row, primary_color):
    n = len(row)
    for i in range(n - 2):
        if row[i] == primary_color and row[i+1] == primary_color and row[i+2] == primary_color:
            return i, [primary_color] * 3
    return -1, None

def find_target_indices(row, primary_color, search_start_index):
    target_indices = []
    n = len(row)
    for i in range(search_start_index, n):
        if row[i] == primary_color:
            left_is_primary = (i > 0 and row[i-1] == primary_color)
            right_is_primary = (i < n - 1 and row[i+1] == primary_color)
            if not left_is_primary and not right_is_primary:
                target_indices.append(i)
    return target_indices

inputs = {
    "train_1": [0, 4, 4, 4, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "train_2": [0, 0, 9, 9, 9, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "train_3": [0, 5, 5, 5, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
expected_outputs = {
    "train_1": [0, 4, 4, 4, 0, 0, 4, 4, 4, 0, 0, 4, 4, 4, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "train_2": [0, 0, 9, 9, 9, 0, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "train_3": [0, 5, 5, 5, 0, 5, 5, 5, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

results = []
for name, input_row in inputs.items():
    primary_color = find_primary_color(input_row)
    pattern_start_index, pattern_block = find_pattern_block(input_row, primary_color)
    pattern_end_index = pattern_start_index + len(pattern_block) if pattern_start_index != -1 else 0
    target_indices = find_target_indices(input_row, primary_color, pattern_end_index)
    
    # Determine expected placement indices based on the correct rule
    output_placement_indices = []
    if pattern_start_index != -1:
        output_placement_indices.append(pattern_start_index) # Initial pattern placement
    for t in target_indices:
        # Place pattern starting one index BEFORE the target index
        placement_start = t - 1 
        if placement_start >= 0: # Basic boundary check
             output_placement_indices.append(placement_start)
             
    results.append({
        "example": name,
        "input_length": len(input_row),
        "primary_color": primary_color,
        "pattern_start_index_input": pattern_start_index,
        "pattern_block": pattern_block,
        "target_indices_input": target_indices,
        "output_pattern_start_indices": sorted(list(set(output_placement_indices))) # Ensure uniqueness and order
    })

import json
print(json.dumps(results, indent=2))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
[
  {
    "example": "train_1",
    "input_length": 32,
    "primary_color": 4,
    "pattern_start_index_input": 1,
    "pattern_block": [
      4,
      4,
      4
    ],
    "target_indices_input": [
      7,
      12,
      18
    ],
    "output_pattern_start_indices": [
      1,
      6,
      11,
      17
    ]
  },
  {
    "example": "train_2",
    "input_length": 32,
    "primary_color": 9,
    "pattern_start_index_input": 2,
    "pattern_block": [
      9,
      9,
      9
    ],
    "target_indices_input": [
      7
    ],
    "output_pattern_start_indices": [
      2,
      6
    ]
  },
  {
    "example": "train_3",
    "input_length": 32,
    "primary_color": 5,
    "pattern_start_index_input": 1,
    "pattern_block": [
      5,
      5,
      5
    ],
    "target_indices_input": [
      6,
      11
    ],
    "output_pattern_start_indices": [
      1,
      5,
      10
    ]
  }
]

```
**YAML Facts**


```yaml
task_description: Construct an output row by placing copies of an initial 3-pixel pattern based on locations identified in the input row.
elements:
  - object: grid
    property:
      - type: 1D array (single row)
      - background_color: white (0)
      - primary_color: varies (yellow, maroon, gray) - the single non-white color present.
  - object: initial_pattern_block
    property:
      - composition: sequence of three consecutive pixels of the primary_color.
      - location_rule: the first occurrence of such a sequence in the input row.
      - role: template pattern to be copied to the output.
  - object: target_marker_pixel
    property:
      - color: same as primary_color.
      - context: appears *after* the initial_pattern_block in the input row.
      - condition: must be horizontally isolated (immediate left and right neighbors are not the primary_color).
      - role: indicates a location for placing the pattern_block in the output.
  - object: output_grid
    property:
      - dimensions: same as input grid (1xN).
      - initial_state: all white (0) pixels.
      - final_state: constructed by placing pattern blocks.
actions:
  - name: identify_primary_color
    input: input_grid
    output: the non-white color `C`.
  - name: find_initial_pattern_block
    input: input_grid, primary_color `C`
    output:
      - pattern: the sequence `[C, C, C]`.
      - start_index: the starting index `idx_p` of this sequence in the input.
  - name: find_target_marker_indices
    input: input_grid, primary_color `C`, start_index_after_pattern (`idx_p + 3`)
    output: list of indices `T = [t1, t2, ...]` where single, isolated pixels of color `C` are found.
  - name: construct_output_grid
    based_on: input_grid_dimensions, initial_pattern_block, start_index `idx_p`, target_marker_indices `T`.
    steps:
      - Initialize output grid (1xN) with white (0).
      - Place the initial_pattern_block into the output grid starting at `idx_p`.
      - For each target marker index `t` in `T`:
        - Calculate the placement start index for the output: `output_idx = t - 1`.
        - Place a copy of the initial_pattern_block into the output grid starting at `output_idx`. (Handle boundary conditions if `output_idx` is less than 0 or placement exceeds grid length, though examples suggest this won't happen).
relationships:
  - type: spatial_mapping
    description: A target_marker_pixel at index `t` in the input row corresponds to the *center* pixel of a pattern_block placed in the output row. The output pattern block starts at index `t-1`.
  - type: origin
    description: The first instance of the pattern_block in the input dictates the pattern to be used for all subsequent placements. Its position is preserved directly in the output.
  - type: construction
    description: The output grid is built constructively by placing pattern blocks onto a blank canvas, not by modifying the input grid directly.
```


**Natural Language Program**

1.  Accept the input grid (which is a single row). Let its length be `N`.
2.  Initialize a new output row of length `N` filled with the background color (white, 0).
3.  Identify the primary non-white color (`C`) present in the input row.
4.  Scan the input row to find the starting index (`idx_p`) of the first sequence of three consecutive pixels of color `C`. Define this sequence `[C, C, C]` as the "pattern block" (`P`).
5.  Copy the pattern block (`P`) into the output row, starting at index `idx_p`.
6.  Define a search region in the input row starting from the index immediately after the initial pattern block (i.e., from index `idx_p + 3`).
7.  Scan the input row within this search region. Identify all indices `t` where the pixel `input[t]` has color `C` and is horizontally isolated (i.e., `input[t-1]` is not `C` and `input[t+1]` is not `C`, considering boundary conditions). These are the "target marker indices".
8.  For each identified target marker index `t`:
    a.  Calculate the placement start index for the output: `output_idx = t - 1`.
    b.  Copy the pattern block (`P`) into the output row, starting at `output_idx`. (Ensure placement starts at or after index 0 and the pattern fits within the row length `N`).
9.  Return the constructed output row.
