"""
The transformation rule is: For each row, identify colored sequences. If a
sequence has one or more '0' pixels anywhere to its right within the same row,
then copy the sequence until the end of the row. The final length of the output
row is always the same as the input row, filled with repetitions of the colored
sequence to consume available 0's.
"""

import numpy as np

def get_colored_sequences(row):
    """Identifies and returns colored sequences in a row."""
    sequences = []
    i = 0
    while i < len(row):
        if row[i] != 0:
            start = i
            while i < len(row) and row[i] == row[start]:
                i += 1
            sequences.append((start, i - start, row[start]))  # (start_index, length, color)
        else:
            i += 1
    return sequences

def replicate_and_fill_to_length(row, sequences):
    """Replicates sequences to fill the entire row if zeros are present."""
    new_row = np.copy(row)  # Start with a copy
    
    for start, length, color in reversed(sequences):  # Iterate in reverse to simplify updates
        has_zeros_right = np.any(row[start + length:] == 0)
        
        if has_zeros_right:
            output_length = len(row)
            
            # Create new sequence:
            new_seq = []
            current_pos = start

            while len(new_seq) < output_length:
                for _ in range(length):
                  if len(new_seq) < output_length:
                      new_seq.append(color)

            
            # Convert to numpy array and replace the portion of new_row
            new_row = np.array(new_seq)



    return new_row



def transform(input_grid):
    # initialize output_grid
    output_grid = []

    # change output pixels
    for row in input_grid:
        sequences = get_colored_sequences(row)
        new_row = replicate_and_fill_to_length(row, sequences)
        output_grid.append(new_row)

    return np.array(output_grid)