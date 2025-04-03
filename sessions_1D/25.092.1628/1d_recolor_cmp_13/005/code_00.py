"""
Identify all contiguous horizontal sequences of blue (1) pixels in the input row. 
Determine the maximum length (L_max) among these sequences. 
Change all blue sequences whose length equals L_max to orange (7). 
Leave all other pixels (white pixels and blue sequences with length != L_max) unchanged.
"""

import copy
import numpy as np # numpy can be useful for grid operations but pure lists are fine too

def find_blue_sequences(input_row):
    """
    Finds all contiguous sequences of blue (1) pixels in a row.

    Args:
        input_row (list[int]): A list representing a single row of the grid.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a 
                    sequence with keys 'start' (index) and 'length'. 
                    Returns an empty list if no blue sequences are found.
    """
    sequences = []
    cols = len(input_row)
    i = 0
    while i < cols:
        if input_row[i] == 1: # Start of a potential blue sequence
            start_index = i
            j = i
            # Find the end of the sequence
            while j < cols and input_row[j] == 1:
                j += 1
            sequence_length = j - start_index
            sequences.append({'start': start_index, 'length': sequence_length})
            i = j # Move index past the found sequence
        else:
            i += 1 # Move to the next pixel
    return sequences

def transform(input_grid):
    """
    Transforms the input grid based on the identified rule.
    """
    # Handle empty or invalid input (e.g., not a list of lists)
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        return [] # Or raise an error, depending on expected behavior

    # Assuming the task always provides a grid with at least one row,
    # and the transformation only applies to the first (and only) row based on examples.
    input_row = input_grid[0]
    
    # 1. Initialize the output grid as a copy of the input grid.
    # Make a deep copy to avoid modifying the original input structure if passed by reference elsewhere.
    # For this specific task, copying just the row is sufficient.
    output_row = list(input_row) 

    # 2. Identify all contiguous horizontal sequences of blue (1) pixels.
    blue_sequences = find_blue_sequences(input_row)

    # 3. If no blue sequences are found, return the initial output grid copy.
    if not blue_sequences:
        # Return the copied row within a list to match the grid format
        return [output_row] 

    # 4. Determine the maximum length (L_max) among all identified blue sequences.
    max_length = 0
    # Check if blue_sequences is not empty before calculating max
    if blue_sequences:
        max_length = max(seq['length'] for seq in blue_sequences)

    # 5. Iterate through the recorded list of blue sequences.
    # 6. For each blue sequence, compare its length to L_max.
    # 7. If a sequence's length is exactly equal to L_max, change the color.
    if max_length > 0: # Only proceed if there are blue sequences
        for seq in blue_sequences:
            if seq['length'] == max_length:
                start = seq['start']
                length = seq['length']
                # Change the corresponding pixels in the output row to orange (7)
                for k in range(start, start + length):
                    # Basic bounds check (though start+length should be within range)
                    if k < len(output_row): 
                        output_row[k] = 7
                        
    # 8. Pixels not part of a max-length blue sequence are already correct due to the initial copy.
    
    # 9. Return the modified output grid (row wrapped in a list).
    return [output_row]