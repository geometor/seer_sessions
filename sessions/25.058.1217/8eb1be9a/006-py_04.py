"""
1.  **Identify Azure Rows:** Examine each row in the input grid. If a row contains one or more azure (value 8) pixels, it's considered an "azure row".

2.  **Triple Replicate with Spacing:** For *each* identified azure row:
    *   Replicate the entire row, maintaining the exact positions of the azure pixels, and add it to the output grid.
    *   Add a blank row (all 0s) immediately below the replicated row in the output grid.
    *   Replicate the original azure row again.
    *   Add another blank row.
    *   Replicate the original azure row a final time.

3.  **Output:** The output grid consists of the tripled azure rows, each separated by a blank row. Non-azure rows from the input are discarded. The output height will be (number of azure rows * 4) - 1
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
        output_rows.append(create_blank_row(width)) # extra blank row

    #remove last entry since we are adding one after every row
    output_rows.pop()

    # Stack the rows to create the output grid.
    output_grid = np.stack(output_rows)

    return output_grid