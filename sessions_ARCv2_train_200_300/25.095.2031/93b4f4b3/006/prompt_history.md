
## train_1

**input:**
```
5 5 5 5 5 5 0 0 0 0 0 0
5 5 0 0 0 5 0 3 0 0 3 0
5 5 5 0 0 5 0 3 0 0 3 0
5 5 5 5 0 5 0 3 3 3 3 0
5 5 5 5 5 5 0 0 0 0 0 0
5 0 0 0 5 5 0 2 2 2 0 0
5 0 0 5 5 5 0 2 2 0 0 0
5 0 5 5 5 5 0 2 0 0 0 0
5 5 5 5 5 5 0 0 0 0 0 0
5 0 5 5 0 5 0 0 1 1 1 0
5 0 5 5 0 5 0 0 0 1 1 0
5 0 0 0 0 5 0 0 0 0 1 0
5 5 5 5 5 5 0 0 0 0 0 0
```


**output:**
```
5 5 5 5 5 5
5 5 1 1 1 5
5 5 5 1 1 5
5 5 5 5 1 5
5 5 5 5 5 5
5 2 2 2 5 5
5 2 2 5 5 5
5 2 5 5 5 5
5 5 5 5 5 5
5 3 5 5 3 5
5 3 5 5 3 5
5 3 3 3 3 5
5 5 5 5 5 5
```


## train_2

**input:**
```
1 1 1 1 1 1 0 0 0 0 0 0
1 1 0 0 1 1 0 0 2 2 0 0
1 0 0 0 0 1 0 0 2 2 0 0
1 1 1 1 1 1 0 0 0 0 0 0
1 0 0 0 0 1 0 0 3 3 0 0
1 1 0 0 1 1 0 3 3 3 3 0
1 1 1 1 1 1 0 0 0 0 0 0
1 1 0 0 1 1 0 6 6 6 6 0
1 1 0 0 1 1 0 0 6 6 0 0
1 1 1 1 1 1 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 1
1 1 3 3 1 1
1 3 3 3 3 1
1 1 1 1 1 1
1 6 6 6 6 1
1 1 6 6 1 1
1 1 1 1 1 1
1 1 2 2 1 1
1 1 2 2 1 1
1 1 1 1 1 1
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception of Elements:**

1.  **Input Structure:** The input is consistently a grid of numbers with an even number of columns. The number of rows varies.
2.  **Output Structure:** The output is a grid of numbers with the same number of rows as the input, but exactly half the number of columns.
3.  **Spatial Relationship:** The input grid appears to be composed of two distinct sub-grids placed side-by-side. The left sub-grid seems to define a structure or frame, while the right sub-grid provides content to fill parts of that structure.
4.  **Value Mapping:**
    *   The left sub-grid in the input uses a specific non-zero digit (5 in `train_1`, 1 in `train_2`) to define a frame or boundary, and the digit 0 for the areas inside this frame.
    *   The right sub-grid in the input contains various non-zero digits representing content, placed on a background of 0s.
    *   The output grid seems to be a merge operation. It retains the frame structure from the left input sub-grid. The 0s *within* the frame in the left sub-grid are replaced by the corresponding values (if non-zero) from the right sub-grid.

**YAML Fact Documentation:**


```yaml
task_name: overlay_content_onto_mask
description: Combine two halves of an input grid, using the left half as a mask and the right half as content to fill the mask's empty areas.

grid_properties:
  input_width_relation: twice the output width
  input_height_relation: same as output height
  cell_values: integers

components:
  - id: input_grid
    type: Grid
  - id: output_grid
    type: Grid
  - id: left_mask_grid
    type: Grid
    derivation: Left half of input_grid
    properties:
      - contains a frame defined by a non-zero value (mask_value)
      - contains empty areas defined by zero (fill_target_value: 0)
  - id: right_content_grid
    type: Grid
    derivation: Right half of input_grid
    properties:
      - contains content defined by non-zero values (content_values)
      - contains empty areas defined by zero (background_value: 0)

actions:
  - Split: Divide the input_grid vertically into left_mask_grid and right_content_grid.
  - Initialize: Create the output_grid as a copy of the left_mask_grid.
  - Iterate: Process each cell (row r, column c) of the output_grid.
  - Condition: Check if the value at output_grid[r][c] is equal to fill_target_value (0).
  - Replace: If the condition is true, update output_grid[r][c] with the value from right_content_grid[r][c].
  - Keep: If the condition is false, keep the original value in output_grid[r][c] (the mask_value).

relationships:
  - output_grid dimensions match left_mask_grid dimensions.
  - output_grid combines the structure of left_mask_grid with the content of right_content_grid based on cell values.
```


**Natural Language Program:**

1.  Determine the dimensions of the input grid (rows `R`, columns `C`).
2.  Calculate the width of the output grid, which is `C / 2`.
3.  Divide the input grid vertically into two halves: the `left_grid` (columns 0 to `C/2 - 1`) and the `right_grid` (columns `C/2` to `C - 1`). Both halves will have dimensions `R` x `C/2`.
4.  Initialize the `output_grid` as a direct copy of the `left_grid`.
5.  Iterate through each cell of the `output_grid` using its row index `r` (from 0 to `R-1`) and column index `c` (from 0 to `C/2 - 1`).
6.  For each cell `(r, c)`, check if the value in the `output_grid` at `output_grid[r][c]` is 0.
7.  If the value is 0, replace it with the value found in the `right_grid` at the corresponding position `right_grid[r][c]`.
8.  If the value is not 0, leave it unchanged.
9.  The final `output_grid` is the result of the transformation.
```python
"""
Combine two halves of an input grid, using the left half as a mask (frame) and the right half as content.
The output grid is initialized with the left half. Then, any '0' cells in the output grid are replaced 
by the corresponding cell value from the right half of the input grid.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by overlaying the right half onto the left half where the left half has zeros.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """

    # Determine the dimensions of the input grid
    if not input_grid:
        return []
    num_rows = len(input_grid)
    if not input_grid[0]:
        return [[] for _ in range(num_rows)]
    num_cols = len(input_grid[0])

    # Calculate the midpoint column index (width of the left/right halves)
    mid_col = num_cols // 2

    # Initialize the output grid as a deep copy of the left half of the input grid
    # Slicing creates shallow copies of rows, so iterate to get the structure correctly
    output_grid = [row[:mid_col] for row in input_grid]

    # Iterate through each cell of the initialized output grid
    for r in range(num_rows):
        for c in range(mid_col):
            # Check if the cell in the output grid (originally from the left half) is 0
            if output_grid[r][c] == 0:
                # If it's 0, replace it with the corresponding value from the right half of the input grid
                # The corresponding column in the right half is c + mid_col
                content_value = input_grid[r][c + mid_col]
                # Only replace if the content value is non-zero (optional, but seems implied by examples)
                # Re-evaluating based on examples: replace even if the right side is 0.
                # The logic is: if the left is 0, take whatever is on the right.
                output_grid[r][c] = content_value
            # If the cell in the output grid is not 0, leave it unchanged (it's part of the frame)

    return output_grid

```
```python
"""
Transforms an input grid by splitting it vertically into two halves. The left half serves as a mask or frame, 
and the right half provides content keys. The unique non-zero values from the right half (content keys) are mapped 
to new values based on a rule determined by their relationship to all unique non-zero values in the input grid. 
Specifically, if the index 0 is present among the indices of the right-half values within the sorted list of all 
non-zero values, a 'Reverse' mapping is used. Otherwise, a 'Cyclic Shift' mapping is applied. The output grid is 
initialized with the left half, and its zero cells are filled with the mapped values corresponding to the content keys 
from the right half.
"""

import copy

def _find_unique_non_zeros(grid: list[list[int]]) -> list[int]:
    """Finds and sorts unique non-zero values in a grid."""
    non_zeros = set()
    for row in grid:
        for cell in row:
            if cell != 0:
                non_zeros.add(cell)
    return sorted(list(non_zeros))

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation rule to the input grid.
    """
    # Handle empty input
    if not input_grid or not input_grid[0]:
        return []

    num_rows = len(input_grid)
    num_cols = len(input_grid[0])
    mid_col = num_cols // 2

    # Split the grid into left and right halves
    left_grid = [row[:mid_col] for row in input_grid]
    right_grid = [row[mid_col:] for row in input_grid]

    # Find all unique non-zero values in the entire input grid
    all_non_zeros_sorted = _find_unique_non_zeros(input_grid)

    # Find unique non-zero values (content keys) in the right grid
    content_keys_sorted = _find_unique_non_zeros(right_grid)

    # If there are no content keys, the output is just the left grid
    if not content_keys_sorted:
        # Need a deep copy to avoid modifying the original input structure if it were passed directly
        return copy.deepcopy(left_grid)

    # Determine the indices of content keys within the list of all non-zeros
    # Create a lookup map for faster index finding
    all_non_zeros_map = {val: idx for idx, val in enumerate(all_non_zeros_sorted)}
    indices = []
    for key in content_keys_sorted:
        if key in all_non_zeros_map:
             indices.append(all_non_zeros_map[key])
        # This case shouldn't happen if logic is correct, but added for robustness
        # else: handle error or unexpected value

    # Determine the mapping rule based on the presence of index 0
    use_reverse_mapping = 0 in indices

    # Create the value map based on the rule
    value_map = {}
    n_keys = len(content_keys_sorted)
    if use_reverse_mapping:
        # Reverse mapping
        for i in range(n_keys):
            value_map[content_keys_sorted[i]] = content_keys_sorted[n_keys - 1 - i]
    else:
        # Cyclic shift mapping
        for i in range(n_keys):
            value_map[content_keys_sorted[i]] = content_keys_sorted[(i + 1) % n_keys]

    # Initialize the output grid as a deep copy of the left grid
    output_grid = copy.deepcopy(left_grid)

    # Iterate through the output grid and apply the mapping
    for r in range(num_rows):
        for c in range(mid_col):
            # Check if the cell in the output grid (from left_grid) is 0
            if output_grid[r][c] == 0:
                # Get the corresponding content key from the right grid
                content_key = right_grid[r][c]
                # If the content key is non-zero (and thus in our map)
                if content_key in value_map:
                    # Replace the 0 in the output grid with the mapped value
                    output_grid[r][c] = value_map[content_key]
            # Otherwise (if output_grid[r][c] is not 0), leave it as part of the frame

    return output_grid
```
```python
"""
Transforms an input grid by splitting it vertically into two halves. The left half serves as a mask or frame, 
and the right half provides content keys. The unique non-zero values from the right half (content keys) are mapped 
to new values based on a rule determined by their relationship to all unique non-zero values in the input grid. 
Specifically, if the index 0 is present among the indices of the right-half values within the sorted list of all 
non-zero values, a 'Reverse' mapping is used. Otherwise, a 'Cyclic Shift' mapping is applied. The output grid is 
initialized with the left half, and its zero cells are filled with the mapped values corresponding to the content keys 
from the right half. If a cell in the right half corresponding to a zero cell in the left half is zero, the output cell remains zero.
"""

import copy

# Helper function to find unique non-zero values in a grid
def _find_unique_non_zeros(grid: list[list[int]]) -> list[int]:
    """Finds and sorts unique non-zero values in a grid."""
    non_zeros = set()
    for row in grid:
        for cell in row:
            if cell != 0:
                non_zeros.add(cell)
    return sorted(list(non_zeros))

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation rule to the input grid.
    """
    # Handle empty input case
    if not input_grid or not input_grid[0]:
        return []

    # Get dimensions
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])
    mid_col = num_cols // 2

    # 1. Split the grid into left (mask) and right (content key) halves
    left_grid = [row[:mid_col] for row in input_grid]
    right_grid = [row[mid_col:] for row in input_grid]

    # 2. Analyze: Find unique non-zero values globally and in the right grid
    all_non_zeros_sorted = _find_unique_non_zeros(input_grid)
    content_keys_sorted = _find_unique_non_zeros(right_grid)

    # If there are no content keys in the right grid, the output is just the left grid
    if not content_keys_sorted:
        # Return a deep copy to avoid modifying potential external references to input_grid
        return copy.deepcopy(left_grid)

    # 3. Determine Rule: Check indices of content keys within all non-zeros
    # Create a lookup map for efficient index finding
    all_non_zeros_map = {val: idx for idx, val in enumerate(all_non_zeros_sorted)}
    indices = []
    for key in content_keys_sorted:
        # Ensure the key exists in the map (it should, logically)
        if key in all_non_zeros_map:
             indices.append(all_non_zeros_map[key])

    # Determine the mapping rule based on the presence of index 0
    use_reverse_mapping = 0 in indices

    # 4. Build Map: Create the value map based on the determined rule
    value_map = {}
    n_keys = len(content_keys_sorted)
    if use_reverse_mapping:
        # Reverse mapping: key[i] maps to key[n-1-i]
        for i in range(n_keys):
            value_map[content_keys_sorted[i]] = content_keys_sorted[n_keys - 1 - i]
    else:
        # Cyclic Shift mapping: key[i] maps to key[(i+1) % n]
        for i in range(n_keys):
            value_map[content_keys_sorted[i]] = content_keys_sorted[(i + 1) % n_keys]

    # 5. Apply: Initialize output grid and fill based on the map
    # Initialize the output grid as a deep copy of the left grid
    output_grid = copy.deepcopy(left_grid)

    # Iterate through the output grid (which has the dimensions of the left grid)
    for r in range(num_rows):
        for c in range(mid_col):
            # Check if the cell in the output grid (originally from left_grid) is 0 (needs filling)
            if output_grid[r][c] == 0:
                # Get the corresponding content key from the right grid
                content_key = right_grid[r][c]
                # If the content key is non-zero (and thus should be in our map)
                if content_key != 0:
                    # Replace the 0 in the output grid with the mapped value
                    # Check if key is in map defensively, though it should be if logic is correct
                    if content_key in value_map:
                         output_grid[r][c] = value_map[content_key]
                    # else: # Optional: handle unexpected case where key isn't in map
                    #     pass # Or raise an error, or log
                # If the content_key is 0, the output cell remains 0 (already initialized)

            # Else (if output_grid[r][c] is not 0), it's part of the frame, leave it unchanged.

    return output_grid
```
