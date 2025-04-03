
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
