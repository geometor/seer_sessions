"""
Transforms a single-row input grid into a multi-row output grid. Non-zero
elements in the input expand downwards and rightwards, forming a triangular
pattern. Zero elements remain unchanged. The number of rows in the output grid
is determined by the longest sequence of non-zero digits.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    input_grid = np.array(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]

    # Calculate the number of rows for the output grid
    max_expansion = 0
    current_expansion = 0
    for col in range(cols):
        if input_grid[0, col] != 0:
            current_expansion += 1
        else:
            max_expansion = max(max_expansion, current_expansion)
            current_expansion = 0
    max_expansion = max(max_expansion, current_expansion) #ensure we get length
    
    output_rows = max_expansion + (1 if max_expansion > 0 else 0) #add one extra row

    output_grid = np.zeros((output_rows, cols), dtype=int)

    # Iterate through the input grid and populate the output grid
    for col in range(cols):
        element = input_grid[0, col]
        if element != 0:
           #count length of nonzero sequence
            seq_length = 0
            for j in range(col, cols):
              if input_grid[0, j] != 0:
                seq_length+=1
              else:
                break;

            #expand vertically
            for row in range(seq_length):
                for i in range(row + 1):  # Fill diagonally within the seq
                  if (col + i) < cols: #check bounds
                    output_grid[row, col + i] = element

        else:
            for row in range(output_rows):
                output_grid[row, col] = element

    return output_grid.tolist()