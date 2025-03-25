```python
"""
The transformation extracts specific columns from the input grid that contain alternating azure (8) and gray (5) pixels. The selected columns are kept to produce the output. The columns are compressed by removing all the columns that only contain black(0).
"""

import numpy as np

def _is_valid_column(column):
    """
    Checks if a column is valid based on the alternating color rule.
    A valid column contains only 0, 5, and 8, with 5 and 8 alternating.
    """
    colors = set(column)
    if not colors.issubset({0, 5, 8}):
        return False

    non_zero_elements = [x for x in column if x != 0]
    for i in range(len(non_zero_elements) - 1):
        if non_zero_elements[i] == non_zero_elements[i+1]:
            return False
    return True

def _has_adjacent_eights(column):
    """Checks if a column contains adjacent azure (8) pixels."""
    for i in range(len(column) - 1):
        if column[i] == 8 and column[i+1] == 8:
            return True
    return False
    

def transform(input_grid):
    """
    Extracts columns with alternating azure (8) and gray (5) pixels, 
    then removes empty columns to form the output grid.
    """
    input_grid = np.array(input_grid)
    num_cols = input_grid.shape[1]
    valid_columns = []

    # Identify valid columns based on color alternation and adjacency rules
    for j in range(num_cols):
        column = input_grid[:, j]
        if _is_valid_column(column) and not _has_adjacent_eights(column):
            valid_columns.append(j)

    # Extract the valid columns
    extracted_grid = input_grid[:, valid_columns]
    
    # Initialize list for storing columns of the compressed grid
    compressed_columns = []    
    # Compress by removing all-black columns
    for j in range(extracted_grid.shape[1]):
      if not np.all(extracted_grid[:,j] == 0):
        compressed_columns.append(extracted_grid[:,j])

    # Convert back into a numpy grid for the output.  Handle edge case of
    # no valid columns found by not crashing.
    if len(compressed_columns) > 0:
        output_grid = np.stack(compressed_columns, axis=1)
    else:
        output_grid = np.zeros((0, 0), dtype=int)  # Return an empty grid

    return output_grid.tolist()
```