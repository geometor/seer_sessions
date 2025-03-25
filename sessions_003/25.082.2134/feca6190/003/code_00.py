"""
Transforms a 1x5 input grid into a square output grid by replicating non-zero elements
diagonally and anti-diagonally. The output grid's size is determined by the number of
non-zero digits and the number of elements in input. Zeros in the input influence the
starting position of the replication.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_array = np.array(input_grid)

    # Count non-zero digits
    non_zero_count = np.count_nonzero(input_array)

    # Determine output grid size
    output_size = max(2 * non_zero_count - 1, input_array.size)
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Iterate through non-zero digits
    for i in range(input_array.size):
        digit = input_array[0][i]
        if digit != 0:
            # Count preceding zeros
            preceding_zeros = np.count_nonzero(input_array[0, :i] == 0)
            row_index = preceding_zeros

            # Place initial digit
            if 0 <= row_index < output_size and 0<= i < output_size:
                output_grid[row_index][i] = digit

            # Diagonal replication
            r, c = row_index + 1, i + 1
            while r < output_size and c < output_size:
                if output_grid[r][c] == 0:
                    output_grid[r][c] = digit
                r += 1
                c += 1

            # Anti-diagonal replication
            r, c = row_index + 1, i - 1
            while r < output_size and c >= 0:
                if output_grid[r][c] == 0:
                   output_grid[r][c] = digit

                r += 1
                c -= 1

    return output_grid