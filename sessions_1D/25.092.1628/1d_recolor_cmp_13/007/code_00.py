"""
Identify all contiguous horizontal sequences of blue (1) pixels in the input row. 
Determine the maximum length (L_max) among these sequences. 
Change all blue sequences whose length equals L_max to orange (7). 
Leave all other pixels (white pixels and blue sequences with length != L_max) unchanged.
"""

import copy 

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
        # Check if the current pixel is blue (1)
        if input_row[i] == 1: 
            start_index = i
            j = i
            # Find the end of the contiguous blue sequence
            while j < cols and input_row[j] == 1:
                j += 1
            sequence_length = j - start_index
            # Record the sequence details
            sequences.append({'start': start_index, 'length': sequence_length})
            # Move the main index past this processed sequence
            i = j 
        else:
            # If not blue, move to the next pixel
            i += 1 
    return sequences

def transform(input_grid):
    """
    Transforms the input grid based on the identified rule: changes the longest
    contiguous sequences of blue pixels to orange.

    Args:
        input_grid (list[list[int]]): A grid represented as a list of lists of integers.
                                      Expected to have only one row.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Handle empty or invalid input
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        # Return empty grid for invalid input
        return [] 

    # Assuming the transformation only applies to the first (and only) row
    input_row = input_grid[0]
    
    # 1. Initialize the output row as a copy of the input row.
    output_row = list(input_row) 

    # 2. Identify all contiguous horizontal sequences of blue (1) pixels.
    blue_sequences = find_blue_sequences(input_row)

    # 3. If no blue sequences are found, return the initial output grid copy.
    if not blue_sequences:
        # Return the unchanged row wrapped in a list
        return [output_row] 

    # 4. Determine the maximum length (L_max) among all identified blue sequences.
    max_length = 0
    # Check if blue_sequences is not empty before calculating max
    if blue_sequences:
        # Find the maximum value of the 'length' key in the list of sequence dictionaries
        max_length = max(seq['length'] for seq in blue_sequences)

    # 5. Iterate through the recorded list of blue sequences.
    # 6. If a sequence's length equals L_max, change its pixels to orange (7) in the output row.
    if max_length > 0: # Proceed only if there are blue sequences and max_length is positive
        for seq in blue_sequences:
            # Check if the current sequence's length matches the maximum length found
            if seq['length'] == max_length:
                start = seq['start']
                length = seq['length']
                # Iterate through the indices of this specific max-length sequence
                for k in range(start, start + length):
                    # Update the pixel color in the output row to orange (7)
                    # Bounds check is implicitly handled by the range derived from find_blue_sequences
                    output_row[k] = 7
                        
    # 7. Pixels not part of a max-length blue sequence remain unchanged due to the initial copy.
    
    # 8. Return the modified output row, formatted as a single-row grid.
    return [output_row]