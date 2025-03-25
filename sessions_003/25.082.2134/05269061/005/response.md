```python
"""
1. **Iterate through Rows:** Process the input grid row by row.
2. **Extract Row Sequence:** For each row, create a list of the non-zero digits, preserving their order.
3. **Reverse Row Sequence:** Reverse the extracted sequence for the current row.
4. **Handle Empty Sequences:**
    - If a row has a non-zero sequence, remember this sequence as the "default" sequence.
    - if there is no default sequence and a row has an empty sequence use an empty sequence.
    - If a row has an empty sequence, use the "default" sequence if available.
5. **Create Output Row:** Create an output row of the same width as the input row.
6. **Fill Output Row:** Fill the output row by repeating the (potentially reversed) sequence.  The sequence might need to be repeated multiple times or truncated to fit the row width.
7.  if all rows are empty, create an output grid with the same shape filled with zeros.
"""

import numpy as np

def extract_non_zero(row):
    """Extracts non-zero elements from a row."""
    return [cell for cell in row if cell != 0]

def reverse_sequence(sequence):
    """Reverses a sequence."""
    return sequence[::-1]

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid)
    default_sequence = []
    found_default = False

    # Iterate through Rows
    for i, row in enumerate(input_grid):
        # Extract Row Sequence
        row_sequence = extract_non_zero(row)

        # Reverse Row Sequence
        reversed_row_sequence = reverse_sequence(row_sequence)

        # Handle Empty Sequences
        if reversed_row_sequence and not found_default:
            default_sequence = reversed_row_sequence
            found_default = True
        elif not reversed_row_sequence:
            reversed_row_sequence = default_sequence

        #Fill Output Row
        for j in range(width):
           if reversed_row_sequence: #prevent index error
                output_grid[i,j] = reversed_row_sequence[j % len(reversed_row_sequence)]
    return output_grid
```