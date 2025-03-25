"""
The transformation identifies the contiguous sequence of non-zero pixels in each row, centers this sequence in the output row, and then mirrors the sequence outwards to fill the remaining spaces.
"""

import numpy as np

def get_non_zero_sequence(row):
    """
    Extracts the non-zero sequence and its start/end indices from a row.
    """
    non_zero_indices = np.nonzero(row)[0]
    if non_zero_indices.size > 0:
        start = non_zero_indices[0]
        end = non_zero_indices[-1]
        sequence = row[start:end+1]
        return start, end, sequence
    else:
        return None, None, None

def transform(input_grid):
    """
    Transforms the input grid by centering and mirroring non-zero sequences in each row.
    """
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    for i in range(rows):
        # 1. Identify the Object
        start, end, sequence = get_non_zero_sequence(input_grid[i, :])

        if sequence is not None:  # If the row is not all zeros
            # 2. Center the Object
            center_index = (cols - 1) / 2
            start_index = int(center_index - (len(sequence) - 1) / 2)
            output_grid[i, start_index:start_index + len(sequence)] = sequence

            # 3. Mirror Outwards
            left_index = start_index - 1
            right_index = start_index + len(sequence)
            
            #mirror left
            for j in range(start_index):
                output_grid[i, j] = output_grid[i, 2*start_index - j -1]
            #mirror right    
            for j in range(right_index, cols):    
                output_grid[i, j] = output_grid[i, 2*(right_index-1) - j -1]

    return output_grid