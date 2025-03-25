"""
The transformation rule works as follows:
1. Analyze Rows: Examine each row of the input grid. Count the number of non-zero pixels in each row.
2. Sort Rows: Sort the rows based on the count of non-zero pixels, in descending order (rows with more non-zero pixels come first). If any rows are empty, place them at the end.
3. Consolidate within Rows: Iterate through the sorted rows. Within each row, shift the non-zero pixels to the "left", adjacent to each other, removing any gaps of zeros between them.
4. Rebuild Grid: create a new, empty output grid with same dimensions as the input.
5. Populate Output: Copy each of the processed rows to the output grid starting from the top row.
"""

import numpy as np

def count_non_zero(row):
    """Counts the number of non-zero elements in a row."""
    return np.count_nonzero(row)

def consolidate_row(row):
    """Shifts non-zero pixels to the left within a row."""
    new_row = [pixel for pixel in row if pixel != 0]
    new_row.extend([0] * (len(row) - len(new_row)))  # Pad with zeros
    return new_row

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape

    # Analyze and sort rows
    row_data = []
    for i, row in enumerate(input_grid_np):
        non_zero_count = count_non_zero(row)
        row_data.append((non_zero_count, list(row),i))  # Store count, original row, original index

    row_data.sort(key=lambda x: x[0], reverse=True)  # Sort by non-zero count

    # rebuild grid
    output_grid = np.zeros((rows, cols), dtype=int)

    # Consolidate and populate output grid
    for i, (count, row, original_index) in enumerate(row_data):
        
        output_grid[i] = consolidate_row(row)
        
    return output_grid.tolist()