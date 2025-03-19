"""
The transformation extracts the unique digits from the input grid, sorts them in descending order, and then arranges them vertically in the output grid. The output grid's width corresponds to the number of unique digits, and its height is determined based on the original grid dimensions. Unfilled cells in the output grid are set to zero.
"""

import numpy as np

def transform(input_grid):
    # Find unique digits in the input grid.
    unique_digits = np.unique(input_grid)

    # Sort the unique digits in descending order.
    sorted_digits = sorted(unique_digits, reverse=True)

    # Determine output grid dimensions.
    num_unique_digits = len(sorted_digits)
    num_input_rows = input_grid.shape[0]
    num_input_cols = input_grid.shape[1]
    output_rows = num_input_cols + 1
    output_cols = num_unique_digits
    
    # Initialize the output grid with zeros.
    output_grid = np.zeros((output_rows * num_input_rows, output_cols), dtype=int)
    
    row_offset = 0

    # Iterate and list each digit into columns.
    for i, digit in enumerate(sorted_digits):
        for row_index in range(output_rows):
            if row_index < num_input_cols:
                output_grid[row_index + row_offset, i] = sorted_digits[row_index] if row_index<num_unique_digits else 0
        
        row_offset += output_rows
        
        # Adjust the row starting point for the next set of rows
        new_start = (i + 1) % len(sorted_digits)  # Wrap around for the columns

        output_grid[:output_rows,i] = np.concatenate((sorted_digits[new_start:num_unique_digits], sorted_digits[0:new_start]))
        output_grid[output_rows:,i] = [0] * (output_grid.shape[0] - output_rows)

    return output_grid