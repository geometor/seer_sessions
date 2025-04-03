
## train_1

**input:**
```
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 5 0 0 0 0 5 0 0 0 0 5 0 0 0 0 0
```


**output:**
```
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 8 0 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 8 0 0 8 0 0 0 8 0 0 0 0 8 0
```


**output:**
```
0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 5 0 0 0 5 0 0 0 5 0 0 0 0 0 0
```


**output:**
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception

The input and output grids in all provided examples consistently have two rows. The width varies between examples. Across all examples, the first row of the input grid is preserved exactly in the output grid. The second row of the input grid, regardless of its content (colors or patterns), is completely replaced by white pixels (color 0) in the output grid. The transformation rule appears to be independent of the specific colors or patterns within the rows, focusing solely on modifying the second row.

## Facts


```yaml
task_type: grid_manipulation
grid_properties:
  dimensionality: 2D
  height: fixed at 2 rows
  width: variable
components:
  - role: static_element
    location: first row (index 0)
    description: This row is transferred unchanged from input to output.
  - role: modified_element
    location: second row (index 1)
    description: This row is replaced entirely in the output.
transformation:
  - action: copy
    source: input grid, first row
    destination: output grid, first row
  - action: replace
    source: input grid, second row
    target_value: white (0)
    destination: output grid, second row
    condition: unconditional for all cells in the second row
relationship:
  - type: positional
    focus: row index
    rule: Row 0 is copied, Row 1 is overwritten.
invariance:
  - property: grid dimensions (height, width) remain the same from input to output.
  - property: content of the first row remains the same.
  - property: specific colors/patterns in the input do not alter the fundamental rule, only the content of the preserved first row.
```


## Natural Language Program

1.  Initialize an output grid with the same dimensions (height and width) as the input grid.
2.  Copy all pixels from the first row (row index 0) of the input grid to the corresponding positions in the first row of the output grid.
3.  Fill all pixels in the second row (row index 1) of the output grid with the white color (value 0).
4.  The resulting grid is the final output.
```python
import numpy as np

"""
Transforms the input grid by copying the first row and replacing the second row with white pixels (0).

1. Initialize an output grid with the same dimensions as the input grid.
2. Copy the first row (row index 0) from the input grid to the output grid.
3. Fill the second row (row index 1) of the output grid entirely with the white color (value 0).
4. Return the modified grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Convert input to numpy array if it's not already
    input_grid_np = np.array(input_grid)

    # Get the dimensions of the input grid
    height, width = input_grid_np.shape

    # Initialize the output grid as a copy of the input grid
    # This handles copying the first row automatically
    output_grid = input_grid_np.copy()

    # Check if the grid has at least two rows
    if height >= 2:
        # Replace the second row (index 1) with white pixels (value 0)
        output_grid[1, :] = 0

    # Return the modified grid
    return output_grid.tolist() # Convert back to list of lists if necessary for ARC format

```
```python
import numpy as np

"""
Transforms the input grid by copying the first row and replacing the second row with white pixels (0).
Assumes the input grid has exactly two rows.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid. 
                    It's assumed to have exactly 2 rows.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Get the dimensions (height should be 2 based on examples)
    height, width = input_array.shape

    # Check if the grid indeed has at least two rows as expected
    if height < 2:
        # Handle unexpected input: return as is or raise error.
        # For ARC, inputs usually conform, so maybe just proceed.
        # Or simply return a copy if modification isn't possible.
        print("Warning: Input grid has fewer than 2 rows.")
        return input_grid # Return original if structure is unexpected

    # Initialize the output grid as a copy of the input grid.
    # This ensures the first row is copied correctly.
    output_array = input_array.copy()

    # Replace all elements in the second row (index 1) with 0 (white).
    # We access the second row using index 1 and set all its columns (:) to 0.
    output_array[1, :] = 0

    # Convert the NumPy array back to a list of lists format for the ARC standard
    output_grid = output_array.tolist()

    return output_grid

```
```python
import numpy as np

"""
Transforms the input grid based on the following rules:
1. The output grid has the same dimensions as the input grid.
2. The second row (index 1) of the output grid is always filled with white pixels (0).
3. A pixel in the first row (index 0) of the output grid is set to white (0) if and only if all the following conditions are met for the corresponding pixel in the input grid:
    a. The pixel itself is non-white (not 0).
    b. The pixel directly below it (in the second row) is white (0).
    c. The pixel's left horizontal neighbor in the first row is white (0). (Treat out-of-bounds as white).
    d. The pixel's right horizontal neighbor in the first row is white (0). (Treat out-of-bounds as white).
4. Otherwise, pixels in the first row retain their original color from the input grid.
"""

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to a NumPy array for easier indexing and manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Initialize the output grid as a copy of the input grid
    output_array = input_array.copy()

    # Rule 2: Replace the second row (index 1) with white pixels (0)
    # Check if the grid has at least two rows before attempting modification
    if height >= 2:
        output_array[1, :] = 0
    else:
        # If fewer than 2 rows, the rule doesn't apply as described,
        # but we can return the grid as is or potentially handle it differently.
        # Based on examples, we expect 2 rows. We'll proceed assuming 2 rows.
        pass # Or return input_grid.tolist() if strict handling is needed

    # Rule 3 & 4: Process the first row (index 0) based on conditions
    # Iterate through each column in the first row
    for c in range(width):
        # Condition 3a: Check if the current pixel is non-white
        is_non_white = input_array[0, c] != 0

        # Condition 3b: Check if the pixel below is white (only if grid has 2+ rows)
        below_is_white = False
        if height >= 2:
            below_is_white = input_array[1, c] == 0

        # Condition 3c: Check left neighbor (handle boundary)
        left_is_white = (c == 0) or (input_array[0, c-1] == 0)

        # Condition 3d: Check right neighbor (handle boundary)
        right_is_white = (c == width - 1) or (input_array[0, c+1] == 0)

        # Apply Rule 3: If all conditions met, set output pixel to white
        if is_non_white and below_is_white and left_is_white and right_is_white:
            output_array[0, c] = 0
        # Else: output_array[0, c] keeps its copied value (Rule 4 is implicitly handled by copying initially)

    # Convert the final NumPy array back to a list of lists
    return output_array.tolist()
```
