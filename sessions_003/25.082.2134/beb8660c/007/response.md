```python
"""
Transforms the input grid by identifying rows with non-black pixels ("data rows"), compressing the non-black pixels within each data row to the right, and stacking the modified data rows at the bottom of the output grid. Remaining rows at the top are filled with black pixels.
"""

import numpy as np

def _is_data_row(row):
    """Checks if a row contains at least one non-black pixel."""
    return np.any(row != 0)

def _compress_row(row):
    """Compresses non-black pixels to the right, maintaining order."""
    non_black_pixels = row[row != 0]
    compressed_row = np.zeros_like(row)
    compressed_row[-len(non_black_pixels):] = non_black_pixels
    return compressed_row

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Identify Data Rows
    data_rows = []
    data_rows_indices = []
    for i, row in enumerate(input_grid):
        if _is_data_row(row):
            data_rows.append(row)
            data_rows_indices.append(i)


    # Compress Data Rows
    compressed_rows = []
    for row in data_rows:
        compressed_rows.append(_compress_row(row))

    # Stack Modified Rows
    start_row = rows - len(compressed_rows)
    for i, row in enumerate(compressed_rows):
        output_grid[start_row + i, :] = row

    return output_grid.tolist()
```