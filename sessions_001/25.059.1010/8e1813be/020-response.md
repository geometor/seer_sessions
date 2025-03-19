# 8e1813be • 020 • refine_coder

---
```python
"""
The transformation rule filters rows of the input grid based on the value of their first element. If a row starts with either 0 or 5, it is removed. Otherwise, the row is kept. The order of the remaining rows, and all the columns and their values are preserved in the output. The output grid contains only the rows that satisfy this condition.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by selecting rows that do not start with 0 or 5, preserving original row content and order."""

    # Convert input_grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Initialize an empty list to store the selected rows.
    selected_rows = []

    # Iterate through each row of the input array.
    for row in input_array:
        # Check if the first element of the row is not 0 and not 5.
        if row[0] != 0 and row[0] != 5:
            # If the condition is met, append the entire row to the selected_rows list.
            selected_rows.append(row)

    # Convert the list of selected rows to a NumPy array.
    output_array = np.array(selected_rows)

    # Convert the NumPy array back to a list of lists for the output.
    return output_array.tolist()
```

