import numpy as np
import copy

"""
Transforms a 2D grid by changing horizontal sequences of 0s to 2s if and only if:
1. The sequence of 0s has a length greater than 1 (i.e., is '0 0' or longer).
2. The sequence of 0s is immediately adjacent horizontally (left or right) 
   to a sequence of exactly two 5s ('5 5') within the same row.
Other 0s and all 5s remain unchanged.
"""

def find_sequences(row, target_value):
    """
    Finds all contiguous horizontal sequences of a target value in a row.

    Args:
        row (np.array): A single row from the grid (1D numpy array).
        target_value (int): The value to find sequences of.

    Returns:
        list: A list of dictionaries, where each dictionary represents a sequence
              and has keys 'start' (inclusive start index), 'end' (inclusive 
              end index), and 'len' (length of the sequence). Returns an empty 
              list if no sequences are found.
    """
    sequences = []
    in_sequence = False
    start_col = -1
    row_len = len(row)
    
    for col_idx, value in enumerate(row):
        is_target = (value == target_value)
        
        if is_target and not in_sequence:
            # Start of a new sequence
            in_sequence = True
            start_col = col_idx
        elif not is_target and in_sequence:
            # End of the current sequence (before the current index)
            end_col = col_idx - 1
            sequences.append({'start': start_col, 'end': end_col, 'len': end_col - start_col + 1})
            in_sequence = False
            start_col = -1
            
    # Handle sequence ending at the last element of the row
    if in_sequence:
        end_col = row_len - 1
        sequences.append({'start': start_col, 'end': end_col, 'len': end_col - start_col + 1})
        
    return sequences

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input 2D grid.

    Returns:
        list of lists: The transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation and copying
    input_np = np.array(input_grid)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # Iterate through each row independently
    for r in range(rows):
        current_row = input_np[r, :]
        
        # Find all horizontal sequences of 5s in the current row
        five_sequences_all = find_sequences(current_row, 5)
        
        # Filter 5-sequences to find only those with length exactly 2 ('5 5')
        five_five_sequences = [seq for seq in five_sequences_all if seq['len'] == 2]

        # If there are no '5 5' sequences in this row, no changes are needed, continue to next row
        if not five_five_sequences:
            continue
            
        # Find all horizontal sequences of 0s in the current row
        zero_sequences = find_sequences(current_row, 0)
        
        # Check each sequence of 0s
        for z_seq in zero_sequences:
            # Condition 1: Check if the zero sequence length is greater than 1
            if z_seq['len'] > 1:
                change_this_sequence = False
                # Condition 2: Check if it's adjacent to *any* '5 5' sequence in this row
                for f_seq in five_five_sequences:
                    # Check adjacency: zero sequence is immediately LEFT of '5 5'
                    if z_seq['end'] + 1 == f_seq['start']:
                        change_this_sequence = True
                        break # Found an adjacent '5 5', no need to check others for this zero sequence
                    # Check adjacency: zero sequence is immediately RIGHT of '5 5'
                    if f_seq['end'] + 1 == z_seq['start']:
                        change_this_sequence = True
                        break # Found an adjacent '5 5', no need to check others for this zero sequence
                
                # If both conditions met, change the 0s to 2s in the output grid
                if change_this_sequence:
                    for c in range(z_seq['start'], z_seq['end'] + 1):
                        # Modify the output grid, not the input array being iterated on
                        output_grid[r, c] = 2

    # Convert back to list of lists for the final output format
    return output_grid.tolist()