# 2dee498d • 008 • example_1 • investigate_coder

---
```python
"""
The transformation extracts specific columns from the input grid to create the output grid. Specifically, it takes the first, third, and last (ninth) columns of the input grid and arranges them sequentially to form the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the first, third, and last columns of the input grid to form the output grid.
    """
    # Convert input_grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Get the height and width of the input grid
    height, width = input_array.shape

    # Identify the columns to extract: first (0), third (2), and last (width - 1)
    selected_columns = [0, 2, width - 1]

    # Initialize an empty output grid (using a list of lists for now)
    output_grid = []

    # Iterate through the rows of the input grid
    for row in input_array:
        # Create a new row for the output grid
        output_row = []
        # Add the pixels from the selected columns to the output row
        for col_index in selected_columns:
            output_row.append(row[col_index])
        # Add the output row to the output grid
        output_grid.append(output_row)
        
    return output_grid
```

