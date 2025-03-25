"""
The transformation rule is to double the width of each row in the input grid.
If a row contains only zeros, the output row will be double the length, filled with zeros.
If a row contains any non-zero values, identify contiguous sequences of identical numbers and repeat them to form the new row.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    
    # Initialize the output grid as a list
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_array:
        # Check if the row contains only zeros
        if np.all(row == 0):
            # Create a new row of zeros with double the width
            new_row = [0] * (2 * cols)
        else:
            # Identify contiguous sequences of identical numbers
            sequences = []
            current_sequence = []
            for i in range(len(row)):
                if i == 0:
                  current_sequence.append(row[i])
                elif row[i] == row[i-1]:
                  current_sequence.append(row[i])
                else:
                  sequences.append(current_sequence)
                  current_sequence = [row[i]]
            sequences.append(current_sequence) #append last sequence

            # Create the new row by repeating the sequence once.
            new_row = []
            for seq in sequences:
                new_row.extend(seq)
            for seq in sequences:
                new_row.extend(seq)          
        
        # Add new row to output
        output_grid.append(new_row)
    
    return output_grid