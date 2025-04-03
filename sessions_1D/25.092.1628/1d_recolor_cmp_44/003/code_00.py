"""
Identify the single longest contiguous horizontal sequence of azure pixels (8) 
within the entire input grid (represented as a 2D NumPy array) and replace 
its pixels with green (3). If multiple sequences share the maximum length, 
the sequence encountered first (scanning rows top-to-bottom, then columns 
left-to-right) is chosen. If no azure sequences are found, the original grid 
is returned.
"""

import numpy as np
from typing import List, Dict, Optional, Tuple

def find_horizontal_sequences(grid_row: np.ndarray, target_color: int, row_index: int) -> List[Dict]:
    """
    Finds all contiguous horizontal sequences of a target color in a 1D numpy array (grid row).

    Args:
        grid_row: A 1D numpy array representing a row of the grid.
        target_color: The integer color value to search for.
        row_index: The index of this row in the original grid.

    Returns:
        A list of dictionaries, where each dictionary represents a sequence
        and contains 'row' index, 'start' column, 'end' column (inclusive), and 'length'.
    """
    sequences = []
    start_col = -1
    width = len(grid_row)
    
    for c_idx, pixel in enumerate(grid_row):
        if pixel == target_color:
            # Start of a new sequence or continuation
            if start_col == -1:
                start_col = c_idx
        else:
            # End of the current sequence (if one was active)
            if start_col != -1:
                sequences.append({
                    'row': row_index,
                    'start': start_col,
                    'end': c_idx - 1,
                    'length': c_idx - start_col
                })
                start_col = -1  # Reset for the next potential sequence

    # Handle a sequence ending at the very end of the row
    if start_col != -1:
        sequences.append({
            'row': row_index,
            'start': start_col,
            'end': width - 1,
            'length': width - start_col
        })

    return sequences

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by finding the longest horizontal sequence of 
    azure pixels (8) and replacing them with green pixels (3).

    Args:
        input_grid: A 2D NumPy array representing the input grid.

    Returns:
        A 2D NumPy array representing the transformed output grid.
    """
    # Initialize variables to track the overall longest sequence found
    max_length = 0
    longest_sequence_details: Optional[Dict] = None
    target_color = 8  # azure
    replacement_color = 3  # green

    # Iterate through each row of the input grid
    for r_idx, row in enumerate(input_grid):
        # Find all azure sequences in the current row
        row_sequences = find_horizontal_sequences(row, target_color, r_idx)
        
        # Check if any sequence in this row is longer than the current max
        for seq in row_sequences:
            # Update if this sequence is strictly longer
            # This naturally handles the tie-breaking rule (first encountered wins)
            if seq['length'] > max_length:
                max_length = seq['length']
                longest_sequence_details = seq

    # If no azure sequence was found anywhere in the grid, return a copy
    if longest_sequence_details is None:
        return np.copy(input_grid)

    # Initialize output_grid as a copy of the input to modify
    output_grid = np.copy(input_grid)

    # Retrieve details of the longest sequence
    target_row = longest_sequence_details['row']
    start_col = longest_sequence_details['start']
    end_col = longest_sequence_details['end'] # end column is inclusive

    # Modify the output grid by replacing the pixels of the longest sequence
    # Slicing in NumPy: [row_index, start_column:end_column + 1]
    output_grid[target_row, start_col : end_col + 1] = replacement_color

    # Return the modified output grid
    return output_grid