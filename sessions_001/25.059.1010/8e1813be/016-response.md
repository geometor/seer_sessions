# 8e1813be • 016 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves selecting specific rows from the input grid to form the output grid.
Rows that do not begin with 0 or 5 are kept.  All elements of the selected rows are included in the output.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by selecting rows that do not start with 0 or 5."""

    # Convert input_grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Initialize an empty list to store the selected rows
    selected_rows = []

    # Iterate through each row of the input array
    for row in input_array:
        # Check if the first element of the row is not 0 and not 5
        if row[0] != 0 and row[0] != 5:
            # If the condition is met, append the row to the selected_rows list
            selected_rows.append(row)

    # Convert the list of selected rows to a NumPy array
    output_array = np.array(selected_rows)
    
    # get the first element of each selected row
    first_elements = output_array[:,0:1]

    # Determine how many time to repeat these
    num_repeats = output_array.shape[1] // first_elements.shape[1]

    #tile the first elements to match the size of the original rows
    output_array = np.tile(first_elements, num_repeats)

    return output_array.tolist()
```
