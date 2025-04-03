import numpy as np
import copy

"""
Identifies contiguous horizontal sequences of non-white pixels (color > 0) in a 1D input array (represented as a 1xN grid). 
For each sequence found:
If the sequence length is greater than 2, it keeps the first and last pixels of the sequence and changes all pixels strictly between them to white (color 0).
If the sequence length is 1 or 2, it leaves the sequence unchanged.
White background pixels (color 0) remain unchanged.
The input is expected to be a grid with exactly one row.
"""

def find_sequences_1d(row):
    """
    Finds start index, end index, color, and length of contiguous 
    non-zero sequences in a 1D numpy array.

    Args:
        row (np.array): A 1D numpy array of integers representing pixel colors.

    Returns:
        list: A list of dictionaries, where each dictionary contains 
              'start', 'end', 'color', and 'length' for a sequence.
    """
    sequences = []
    i = 0
    n = len(row)
    while i < n:
        # Skip background pixels (color 0)
        if row[i] == 0:
            i += 1
            continue
        
        # Found the start of a non-zero sequence
        start_index = i
        color = row[i] 
        
        # Find the end of the sequence (where color changes or end of row)
        j = i
        # Note: The original logic used row[j] == color, which finds sequences
        # of the *same* non-zero color. The task description just says "non-white".
        # Let's stick to the stricter "same non-zero color" as implied by examples,
        # but this could be relaxed to row[j] != 0 if needed.
        while j < n and row[j] == color: 
            j += 1
        end_index = j - 1 # The last index included in the sequence
        length = end_index - start_index + 1
        
        sequences.append({'start': start_index, 'end': end_index, 'color': color, 'length': length})
        
        # Move the main index past this sequence
        i = j # Start searching for the next sequence from here
        
    return sequences

def transform(input_grid):
    """
    Applies the sequence hollowing transformation to the input grid.

    Args:
        input_grid (list of lists or numpy array): A grid containing one row (1xN).

    Returns:
        list of lists: The transformed grid (1xN).
    """
    
    # Ensure input is a NumPy array and handle potential empty/invalid input
    try:
        input_array = np.array(input_grid, dtype=int)
        if input_array.ndim != 2 or input_array.shape[0] != 1 or input_array.shape[1] == 0:
             # Expecting a 2D array with exactly 1 row and at least 1 column
             # Return empty list for invalid formats based on task constraints
             # Or potentially raise an error depending on desired behavior
             # For ARC, often returning the input or an empty representation is safer
             return input_grid # Or potentially [] or [[ ]] if appropriate
        input_row = input_array[0]
    except:
        # Handle cases where conversion to numpy array fails
        return input_grid # Return original input if conversion fails

    # Create a copy of the input row to modify
    output_row = input_row.copy()
    
    # Find all contiguous sequences of the same non-zero color
    sequences = find_sequences_1d(input_row)
    
    # Process each sequence based on its length
    for seq in sequences:
        start = seq['start']
        end = seq['end']
        length = seq['length']
        
        # Apply the transformation rule: if length > 2, hollow out the middle
        if length > 2:
            # Iterate from the second element (index start + 1) 
            # up to (but not including) the last element (index end)
            # Set these intermediate pixels to the background color (0)
            output_row[start + 1 : end] = 0 
            # Note: output_row[end] is already correct (preserved)
            # Note: output_row[start] is already correct (preserved)

    # Convert the modified NumPy row back to the required list of lists format
    output_grid = [output_row.tolist()]
    
    return output_grid