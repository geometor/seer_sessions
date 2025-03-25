"""
The initial colored pixels in the input are repeated to form a longer sequence. This extended sequence is then used to create multiple rows, resulting in a rectangular output grid. The zero's at the end of the input is maintained. The number of output rows generated is dependent on number of colored pixels in input.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify the non-zero sequence
    non_zero_indices = np.where(input_grid != 0)[0]
    if len(non_zero_indices) == 0:  # Handle the case where the input is all zeros.
        return input_grid
    last_non_zero_index = non_zero_indices[-1]
    non_zero_sequence = input_grid[:last_non_zero_index + 1]
    zero_sequence = input_grid[last_non_zero_index + 1:]


    # 2. Determine Repetition Count and Row Count
    repetition_count = len(non_zero_sequence)
    row_count = len(non_zero_sequence) + 1

    # 3. Horizontal Expansion & 4. Vertical Replication
    output_grid = []
    for _ in range(row_count):
      expanded_row = []
      #append a copy of the input non-zero color elements.
      for i in range(repetition_count):
        expanded_row.extend(non_zero_sequence)
      expanded_row.extend(zero_sequence)
      output_grid.append(expanded_row)
    
    return output_grid