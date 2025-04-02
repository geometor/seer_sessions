import numpy as np

"""
Identifies the last occurrence of the sequence [0, 0, 0, 9] (three white pixels followed by a maroon pixel) in a 1D input grid. 
If found, it checks the color 'C' of the pixel immediately preceding this sequence. 
If this preceding pixel exists (the sequence doesn't start at index 0) and its color 'C' is not white (0), it replaces the three white pixels [0, 0, 0] within the sequence with three pixels of color 'C' ([C, C, C]). 
Otherwise, the grid remains unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the rule described above.

    Args:
        input_grid (list): A 1D list representing the input grid pixels.

    Returns:
        list: The transformed 1D list representing the output grid.
    """
    # Convert input list to a numpy array for efficient searching and slicing
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify, ensuring the original remains untouched if no transformation occurs
    output_grid = grid.copy()
    n = len(grid)
    
    # Define the target sequence we are looking for
    target_sequence = np.array([0, 0, 0, 9], dtype=int)
    sequence_len = len(target_sequence)
    
    # Initialize variable to store the starting index of the last found match
    # -1 indicates no match found yet
    last_match_index = -1
    
    # Scan the grid from left to right to find all occurrences of the target sequence
    # We iterate up to n - sequence_len to avoid index out of bounds errors
    for i in range(n - sequence_len + 1):
        # Check if the slice of the grid matches the target sequence
        if np.array_equal(grid[i : i + sequence_len], target_sequence):
            # If it matches, update last_match_index to the current index i
            # This ensures we always store the index of the rightmost (last) match
            last_match_index = i
            
    # After scanning the entire grid, check if a match was found
    if last_match_index != -1:
        # A match was found. Check if this match has a preceding pixel
        # (i.e., the match does not start at the very beginning of the grid)
        if last_match_index > 0:
            # Get the color of the pixel immediately preceding the sequence
            preceding_color = grid[last_match_index - 1]
            
            # Check if the preceding color is not white (0)
            if preceding_color != 0:
                # All conditions met: Replace the [0, 0, 0] part of the sequence
                # The [0, 0, 0] part starts at last_match_index and has length 3
                output_grid[last_match_index : last_match_index + 3] = preceding_color

    # Convert the potentially modified numpy array back to a list before returning
    return output_grid.tolist()