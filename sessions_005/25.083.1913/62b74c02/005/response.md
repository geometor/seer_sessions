```python
"""
The transformation mirrors the colors of non-zero pixels in each row outwards, replacing zero-valued pixels.
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
        return None, None, None  # Handle empty rows

def transform(input_grid):
    """
    Transforms the input grid by mirroring non-zero pixel sequences in each row.
    """
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    for i in range(rows):
        start, end, sequence = get_non_zero_sequence(input_grid[i, :])

        if sequence is not None:  # If the row is not all zeros
            output_grid[i,:] = mirror_sequence(sequence, cols)

    return output_grid

def mirror_sequence(sequence, cols):
    """Mirrors and fills to make sequence of length = cols"""
    
    mirrored_row = np.zeros(cols, dtype=int)
    
    # single element sequence
    if len(sequence) == 1:
        mirrored_row[:] = sequence[0]
        return mirrored_row

    # place original sequence
    start_index = (cols - len(sequence)) // 2
    mirrored_row[start_index:start_index + len(sequence)] = sequence

    # Fill to the left.
    left_index = start_index - 1
    seq_index = 1  # start with second value
    
    while left_index >= 0:
        mirrored_row[left_index] = sequence[seq_index]
        left_index -= 1
        seq_index = (seq_index + 1) % len(sequence)

    # Fill to the right.
    right_index = start_index + len(sequence)
    seq_index = len(sequence) - 2  # start with second to last
    while right_index < cols:
        mirrored_row[right_index] = sequence[seq_index]
        right_index += 1
        seq_index = (seq_index - 1) % len(sequence)


    return mirrored_row
```