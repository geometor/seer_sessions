"""
Identifies a contiguous sequence of non-white (non-zero) pixels in a single 
input row. It then moves the first pixel (marker) of this sequence to the 
position immediately following the last pixel of the sequence, preserving the 
internal order of the rest of the sequence (body). The surrounding white (zero) 
pixels remain unchanged. If the sequence length is less than 2, the input is 
returned unchanged.
"""

import numpy as np
from typing import List, Tuple

# Helper function to find the sequence
def find_contiguous_non_zero_sequence(row: List[int]) -> Tuple[int, int]:
    """
    Finds the start and end+1 indices of the first contiguous non-zero sequence in a list.

    Args:
        row: A list of integers representing a row of the grid.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no sequence is found.
        end_index points to the element *after* the last element of the sequence.
    """
    start_index = -1
    end_index = -1
    n = len(row)
    for i, pixel in enumerate(row):
        # Find the start of a potential sequence
        if pixel != 0 and start_index == -1:
            start_index = i
        # Find the end of the sequence (first zero after start)
        elif pixel == 0 and start_index != -1:
            end_index = i
            break # Found the first sequence, stop searching

    # Handle case where sequence goes to the end of the row
    if start_index != -1 and end_index == -1:
        end_index = n
        
    # Handle case where no sequence found
    if start_index == -1:
        return -1, -1 # Explicitly return -1, -1 for no sequence

    return start_index, end_index

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid according to the described rule.
    """
    # 1. Receive the input grid and extract the single row
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
        # Handle invalid input format if necessary, though ARC format is usually guaranteed
        # For robustness, could raise an error or return input
        print("Warning: Invalid input format received.")
        return input_grid # Return input as is if format is unexpected

    if len(input_grid) != 1:
        # Based on examples, assume single row. Handle unexpected multi-row input.
        print("Warning: Expected single-row grid, processing only the first row.")
        # Or potentially iterate/apply to all rows if logic extends? Stick to single row for now.
    
    input_row = input_grid[0]
    output_row = list(input_row) # Initialize output as a copy

    # 2. Identify the contiguous subsequence of non-white pixels
    start_index, end_index = find_contiguous_non_zero_sequence(input_row)

    # 3. If no sequence found or length < 2, return input unchanged
    sequence_len = end_index - start_index if start_index != -1 else 0
    if start_index == -1 or sequence_len < 2:
        return [output_row] # Return copy in original grid format

    # 4. Isolate the non-white sequence
    # Not strictly needed as a separate variable, we'll use indices

    # 5. Identify the "marker pixel" (first element)
    marker_pixel = input_row[start_index]

    # 6. Identify the "body sequence" (remaining elements)
    body_sequence = input_row[start_index + 1 : end_index]

    # 7. Construct the "transformed sequence"
    transformed_sequence = body_sequence + [marker_pixel]

    # 8. Construct the output row
    # Get parts before and after the original sequence
    before_sequence = input_row[:start_index]
    after_sequence = input_row[end_index:]

    # Assemble the final output row
    output_row = before_sequence + transformed_sequence + after_sequence

    # 9. Return the constructed output row, formatted as a grid
    return [output_row]
