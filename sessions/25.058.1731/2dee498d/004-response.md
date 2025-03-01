# 2dee498d • 004 • example_1 • investigate_coder

---
```python
"""
The transformation extracts unique elements from each column of the input grid to create a smaller output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting unique elements from each column.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid with unique column elements.
    """
    # Convert input_grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)
    
    # Get the number of columns in the input grid
    num_cols = input_array.shape[1]
    
    # Initialize an empty list to store the unique elements for each column
    output_cols = []
    
    # Iterate through each column
    for j in range(num_cols):
        # Extract the j-th column
        column = input_array[:, j]
        # Get unique elements in the column, preserving order using a trick with dictionaries
        unique_elements = list(dict.fromkeys(column))
        # add to list
        output_cols.append(unique_elements)

    # Find the maximum length among all unique element lists
    max_len = max(len(col) for col in output_cols)

    # Pad shorter columns with 0
    padded_cols = []
    for col in output_cols:
      padded_col = col + [0] * (max_len- len(col))
      padded_cols.append(padded_col)
      
    # convert to np array    
    output_array = np.array(padded_cols)
    # need to transpose to make unique elements into rows instead of columns
    output_array = output_array.transpose()

    # Convert the output array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
