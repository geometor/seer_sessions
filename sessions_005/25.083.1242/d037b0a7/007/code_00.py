"""
1. Identify Source Rows: Scan the input grid row by row. A row is considered a "source row" if it contains *any* non-zero values.

2. Propagate Source Rows:
   - If a row is a source row, copy it directly to the output grid.
   - For all subsequent rows, replace the *entire* row with the content of the *last encountered* source row.
   - Continue this replacement until another source row is found or the end of the input grid is reached.

3. Handle Non-Source Initial Rows: If rows at the beginning of the grid are *not* source rows, copy to the output unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = []

    # Identify source rows (rows where any element is not zero)
    source_rows_indices = [i for i, row in enumerate(input_grid) if np.any(row != 0)]

    last_source_row = None

    for i, row in enumerate(input_grid):
        if i in source_rows_indices:
            # Copy the source row to output and update last_source_row
            output_grid.append(row.tolist())
            last_source_row = row.tolist()
        else:
            # If not a source row, check if we have a last_source_row
            if last_source_row is not None:
                # Replace the entire row with the last_source_row
                output_grid.append(last_source_row)
            else:
                # If no last_source_row (initial rows), copy as is
                output_grid.append(row.tolist())
    return output_grid