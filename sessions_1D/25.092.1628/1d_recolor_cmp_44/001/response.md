```python
import numpy as np
from typing import List, Dict, Tuple

"""
Identify the single longest contiguous horizontal sequence of azure (8) pixels 
in the input grid (represented as a 1D list) and replace its pixels with green (3). 
All other pixels remain unchanged. If multiple sequences share the maximum length, 
the first one encountered is chosen. If no azure pixels are present, the output 
is identical to the input.
"""

def find_contiguous_sequences(grid_row: List[int], target_color: int) -> List[Dict]:
    """
    Finds all contiguous sequences of a target color in a 1D list (grid row).

    Args:
        grid_row: A list of integers representing a row of the grid.
        target_color: The integer color value to search for.

    Returns:
        A list of dictionaries, where each dictionary represents a sequence
        and contains 'start' index, 'end' index (inclusive), and 'length'.
    """
    sequences = []
    start_index = -1
    for i, pixel in enumerate(grid_row):
        if pixel == target_color:
            # Start of a new sequence
            if start_index == -1:
                start_index = i
        else:
            # End of the current sequence (if one was active)
            if start_index != -1:
                sequences.append({
                    'start': start_index,
                    'end': i - 1,
                    'length': i - start_index
                })
                start_index = -1  # Reset for the next sequence

    # Handle sequence ending at the very end of the row
    if start_index != -1:
        sequences.append({
            'start': start_index,
            'end': len(grid_row) - 1,
            'length': len(grid_row) - start_index
        })

    return sequences

def transform(input_grid: List[int]) -> List[int]:
    """
    Transforms the input grid by finding the longest sequence of azure pixels (8)
    and replacing them with green pixels (3).

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = list(input_grid) # Use list() for explicit copy

    # Define target and replacement colors
    target_color = 8  # azure
    replacement_color = 3  # green

    # Find all contiguous sequences of the target color (azure)
    azure_sequences = find_contiguous_sequences(input_grid, target_color)

    # If no azure sequences were found, return the original grid copy
    if not azure_sequences:
        return output_grid

    # Find the sequence with the maximum length
    longest_sequence = None
    max_length = 0
    for seq in azure_sequences:
        if seq['length'] > max_length:
            max_length = seq['length']
            longest_sequence = seq
        # Note: This implicitly handles ties by keeping the first one found
        # with the maximum length encountered so far.

    # If a longest sequence was identified, perform the replacement
    if longest_sequence:
        start = longest_sequence['start']
        end = longest_sequence['end']
        # Iterate through the indices of the longest sequence in the output grid
        for i in range(start, end + 1):
            # Change the pixel color to the replacement color
            output_grid[i] = replacement_color

    # Return the modified output grid
    return output_grid
```