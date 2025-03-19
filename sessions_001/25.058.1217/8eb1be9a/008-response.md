# 8eb1be9a • 008 • refine_coder

---
```python
"""
1.  **Identify Azure Rows:** Iterate through each row of the input grid. A row is classified as an "azure row" if it contains at least one azure (value 8) pixel.

2.  **Triple Replicate with Spacing:** For *each* identified azure row:
    *   Replicate the entire row (including the azure pixels in their original positions) and add it to the output grid.
    *   Add a blank row (all cells set to 0) immediately below this replicated row in the output grid.
    *   Replicate the original azure row again and add it to the output grid.
    *   Add another blank row immediately below the second replication.
    *   Replicate the original azure row a third time and append to output.

3.  **Output:** The output grid comprises only the tripled azure rows, with each set of replications separated by a single blank row. Non-azure rows from the input are discarded.
"""

import numpy as np

def get_azure_rows(grid):
    """Finds the indices of rows containing azure pixels."""
    azure_rows = []
    for i, row in enumerate(grid):
        if 8 in row:
            azure_rows.append(i)
    return azure_rows

def replicate_row(row):
    """Replicates a row (creates a copy)."""
    return row.copy()

def create_blank_row(width):
    """Creates a row of zeros with the specified width."""
    return np.zeros(width, dtype=int)

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    # Get the width of the input grid.
    width = input_grid.shape[1]

    # Identify azure rows.
    azure_rows_indices = get_azure_rows(input_grid)
    
    # Initialize an empty list to hold the output rows.
    output_rows = []

    # Triple replicate with spacing.
    for row_index in azure_rows_indices:
        original_row = input_grid[row_index]
        
        # Replicate and add blank row three times.
        output_rows.append(replicate_row(original_row))
        output_rows.append(create_blank_row(width))
        output_rows.append(replicate_row(original_row))
        output_rows.append(create_blank_row(width))
        output_rows.append(replicate_row(original_row))


    # Stack the rows to create the output grid.
    output_grid = np.stack(output_rows)

    return output_grid
```
