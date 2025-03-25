```python
"""
1.  Iterate through each row of the input grid.
2.  Extract the non-zero elements of the current row to form an "input sequence."
3.  Reverse the "input sequence" to create a "reversed sequence."
4.  Determine Output Sequence by looking ahead:
    *   Examine all following rows and select the *first* row which also contains non-zero values.
        *   If that row's reversed sequence exists, then it becomes the current row's output sequence
        *.  If that selected row's reversed sequence does not exist:
            * if current rows reversed sequence is not empty - it becomes the output sequence
            * otherwise an empty output sequence is produced
    *   If no following rows contain non-zero values:
        *   if the current rows reversed sequence is not empty - the current reversed sequence is the output sequence
        *   otherwise an empty output sequence is produced
5.  Create Output Row: Create an output row of the same width as the input row.
6.  Fill Output Row: Populate the output row by repeating the determined "output sequence". Truncate or repeat the "output sequence" as needed to match the output row width.
7.  All Empty Rows Edge Case: If all input rows are empty (all zeros), then create an output grid of the same dimensions filled with zeros.
"""

import numpy as np

def extract_non_zero(row):
    """Extracts non-zero elements from a row."""
    return [cell for cell in row if cell != 0]

def reverse_sequence(sequence):
    """Reverses a sequence."""
    return sequence[::-1]

def get_output_sequence(input_grid, current_row_index):
    """Determines the output sequence for a given row."""
    current_row = input_grid[current_row_index]
    current_sequence = extract_non_zero(current_row)
    current_reversed_sequence = reverse_sequence(current_sequence)
    
    #look ahead
    for next_row_index in range(current_row_index + 1, len(input_grid)):
        next_row = input_grid[next_row_index]
        next_sequence = extract_non_zero(next_row)
        next_reversed_sequence = reverse_sequence(next_sequence)
        if next_reversed_sequence:
            return next_reversed_sequence
    
    return current_reversed_sequence
    

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through Rows
    for i in range(height):
        # Determine the output sequence for this row
        output_sequence = get_output_sequence(input_grid, i)
        
        # Fill Output Row
        for j in range(width):
            if output_sequence:  # Prevent index error with empty sequences
                output_grid[i, j] = output_sequence[j % len(output_sequence)]

    return output_grid
```