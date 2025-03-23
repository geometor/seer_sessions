```python
"""
Transforms the input grid by extracting the first element of each unique row, preserving their original order, and constructing the output grid from these elements.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting the first element of each unique row.
    """
    unique_first_elements = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Convert the row to a list to make it hashable for comparison
        row_list = list(row)

        # Check if this row's first element is already in the unique_first_elements list
        is_unique = True
        if len(row) > 0: # Handle empty row case
            first_element = row_list[0]
            if first_element in unique_first_elements:
                is_unique = False


        # If the row's first element is unique, add it to the list
        if is_unique and len(row) > 0: # consider empty rows.
            unique_first_elements.append(first_element)

    # Convert the list of unique first elements to a NumPy array of shape (N,1)
    return np.array(unique_first_elements).reshape(-1, 1)
```