import copy
import numpy as np # Using numpy for potential convenience, though list operations suffice

"""
Identify all contiguous horizontal sequences of blue (1) pixels in the input row. 
Determine the maximum length (L_max) among these sequences. 
Change all blue sequences whose length equals L_max to orange (7). 
Leave all other pixels (white pixels and blue sequences with length != L_max) unchanged.
"""

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
    Transforms the input grid based on the rule: change the longest blue sequences to orange.

    Args:
        input_grid (list[list[int]]): A grid represented as a list of lists of integers.
                                      Expected to have only one row.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Handle empty or invalid input
    if not input_grid or not input_grid[0]:
        return []

    input_row = input_grid[0]
    output_row = list(input_row) # Create a mutable copy for the output

    # Step 1 & 2: Find all blue sequences and their lengths
    blue_sequences = find_blue_sequences(input_row)

    # Step 3: Determine the maximum length
    max_length = 0
    if blue_sequences:
        max_length = max(seq['length'] for seq in blue_sequences)

    # Step 4 & 5 & 6: Apply transformation based on max length
    if max_length > 0: # Only proceed if there are blue sequences
        for seq in blue_sequences:
            # If the sequence length is the maximum length
            if seq['length'] == max_length:
                start = seq['start']
                length = seq['length']
                # Change the corresponding pixels in the output row to orange (7)
                for k in range(start, start + length):
                    # Check bounds just in case, though logic should prevent overrun
                    if k < len(output_row): 
                        output_row[k] = 7

    # Step 7 & 8: Return the modified row in grid format
    return [output_row]
