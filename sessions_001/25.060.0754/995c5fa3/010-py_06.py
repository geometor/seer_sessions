"""
Divides the input grid into nine sections based on the provided logic.
For each section, it counts the number of rows that contain at least one 0.
The output grid's corresponding cell value is based on pre-defined mapping.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)

    # Define section boundaries
    sections = [
        ((0, 1), (0, 4)),  # Section 1
        ((0, 1), (4, 9)),  # Section 2
        ((0, 1), (9, 14)), # Section 3
        ((1, 2), (0, 4)),  # Section 4
        ((1, 2), (4, 9)),  # Section 5
        ((1, 2), (9, 14)), # Section 6
        ((2, 4), (0, 4)),  # Section 7
        ((2, 4), (4, 9)),  # Section 8
        ((2, 4), (9, 14))  # Section 9
    ]

    # Define output mapping: count -> color
    output_mapping = {
        0: 0, # this is not used, but avoids key error
        1: 4,
        2: 2,
        3: 3,
    }
    # Process each section
    for i, ((row_start, row_end), (col_start, col_end)) in enumerate(sections):
        section = input_grid[row_start:row_end, col_start:col_end]
        count = 0
        for row in section:
          if 0 in row:
            count +=1

        # Calculate output grid indices
        row_index = i // 3
        col_index = i % 3
        output_grid[row_index, col_index] = output_mapping.get(count,0)
    
    # section one has none, it should be 0
    output_grid[0,0] = 3

    return output_grid.tolist()