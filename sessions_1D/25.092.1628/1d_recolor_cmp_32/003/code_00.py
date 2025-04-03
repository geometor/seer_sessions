"""
Transforms an input grid by identifying all horizontal contiguous sequences of 
azure (8) pixels. It selects the sequence with the maximum length. If there 
are multiple sequences with the same maximum length, it applies tie-breaking: 
first, by choosing the sequence in the lowest row (highest row index), and second, 
if a tie remains, by choosing the sequence that starts furthest to the right 
(highest start column index). The pixels of the selected sequence are changed 
from azure (8) to blue (1) in the output grid. All other pixels remain unchanged.
"""

import numpy as np

def find_horizontal_azure_sequences(grid):
    """
    Finds all horizontal contiguous sequences of azure (8) in a 2D grid.

    Args:
        grid (np.array): The input 2D grid of pixel values.

    Returns:
        list: A list of dictionaries, each representing a sequence with
              'row', 'start_col', 'end_col', and 'length' keys. Returns an 
              empty list if no azure sequences are found.
    """
    sequences = []
    azure_color = 8
    rows, cols = grid.shape

    # Iterate through each row
    for r in range(rows):
        in_sequence = False
        start_col = -1
        current_length = 0
        # Scan across the columns in the current row
        for c in range(cols):
            if grid[r, c] == azure_color:
                if not in_sequence:
                    # Start of a new sequence
                    in_sequence = True
                    start_col = c
                    current_length = 1
                else:
                    # Continue the current sequence
                    current_length += 1
            else:
                # End of a sequence (if we were in one)
                if in_sequence:
                    sequences.append({
                        'row': r,
                        'start_col': start_col,
                        'end_col': c - 1, # End index is inclusive of last azure pixel
                        'length': current_length
                    })
                    in_sequence = False
                    # Reset sequence tracking
                    start_col = -1
                    current_length = 0
            
            # Handle sequence ending exactly at the right edge of the grid
            if c == cols - 1 and in_sequence:
                 sequences.append({
                        'row': r,
                        'start_col': start_col,
                        'end_col': c, # End index is the last column
                        'length': current_length
                    })

    return sequences

def find_longest_sequence_with_tiebreak(sequences):
    """
    Selects the longest sequence from a list, applying tie-breaking rules.
    Tie-breaking: 1. Lowest row (highest index), 2. Rightmost start (highest index).

    Args:
        sequences (list): A list of sequence dictionaries.

    Returns:
        dict or None: The dictionary of the selected sequence, or None if the 
                      input list is empty.
    """
    if not sequences:
        return None

    # Initialize with the first sequence
    longest_seq = sequences[0]
    max_len = longest_seq['length']

    # Iterate through the rest of the sequences to find the target one
    for seq in sequences[1:]:
        # Check if current sequence is longer
        if seq['length'] > max_len:
            max_len = seq['length']
            longest_seq = seq
        # Check for tie in length
        elif seq['length'] == max_len:
            # Tie-break 1: Lower row (higher row index)
            if seq['row'] > longest_seq['row']:
                 longest_seq = seq
            # Tie-break 2: Same row, rightmost start (higher start col index)
            elif seq['row'] == longest_seq['row']:
                 if seq['start_col'] > longest_seq['start_col']:
                     longest_seq = seq
                     
    return longest_seq


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): The 2D input grid.

    Returns:
        np.array: The 2D output grid with the transformation applied.
    """
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Find all horizontal sequences of azure pixels
    azure_sequences = find_horizontal_azure_sequences(input_grid)

    # If no azure sequences exist, return the original grid copy
    if not azure_sequences:
        return output_grid

    # Select the target sequence based on length and tie-breaking rules
    target_sequence = find_longest_sequence_with_tiebreak(azure_sequences)

    # If a target sequence is found (should always be true if sequences exist)
    if target_sequence:
        # Define the color to change to
        blue_color = 1
        # Get the location of the target sequence
        row = target_sequence['row']
        start_col = target_sequence['start_col']
        end_col = target_sequence['end_col']
        
        # Change the pixels in the selected sequence to blue in the output grid
        # Slicing includes start_col up to (but not including) end_col + 1
        output_grid[row, start_col:end_col + 1] = blue_color

    # Return the modified grid
    return output_grid