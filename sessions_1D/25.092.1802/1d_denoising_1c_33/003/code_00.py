import numpy as np
from itertools import groupby

"""
Transforms the input grid (a single row) by keeping only the longest contiguous horizontal 
segment of the non-background color (any color other than 0). All other pixels, 
including shorter segments or isolated pixels of the non-background color, 
are replaced with the background color (white=0). The output dimensions match 
the input row length (presented as a 1xN grid).
"""

def find_segments_groupby(row):
    """
    Finds contiguous segments of any non-background color using groupby.

    Args:
        row (iterable): A 1D list or NumPy array representing the grid row.

    Returns:
        list: A list of dictionaries, where each dictionary represents a 
              non-background segment and contains 'start', 'end', 'length', 
              and 'color' keys. Returns an empty list if no non-background 
              segments are found.
    """
    segments = []
    index = 0
    background_color = 0
    # Iterate through the row, grouping consecutive identical elements
    for color, group in groupby(row):
        # Calculate the length of the current segment
        length = len(list(group))
        # If the segment is not the background color, record its details
        if color != background_color:
             segments.append({
                 'start': index, 
                 'end': index + length - 1, 
                 'length': length, 
                 'color': color
             })
        # Update the starting index for the next segment
        index += length
    return segments


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or numpy.ndarray): The input grid, expected 
                                                     to represent a single row.

    Returns:
        list of lists: The transformed grid, as a list containing one list (the row).
                       Returns an empty list of lists ([[]]) if input is invalid.
    """
    
    # Convert input to numpy array for consistent handling
    input_np = np.array(input_grid, dtype=int)

    # Validate input shape - should be 1xN or just N
    if input_np.ndim == 0: # Handle scalar input if necessary, though unlikely for ARC
         return [[]] 
    elif input_np.ndim == 1: # Input is already a 1D array
        input_row = input_np
    elif input_np.ndim == 2 and input_np.shape[0] == 1: # Input is a 2D array with one row
        input_row = input_np[0]
    elif input_np.ndim == 2 and input_np.shape[1] == 1: # Input is a 2D array with one column
         input_row = input_np.flatten() # Treat Nx1 as N
    elif input_np.size == 0: # Handle empty array
         return [[]]
    else:
        # Handle unexpected shapes if necessary, or assume valid input based on task description
        # For now, attempt to flatten if it's unexpected but might be a row
        # raise ValueError(f"Input grid has unexpected shape: {input_np.shape}")
        # Let's try flattening as a fallback, might work for some edge cases
         if input_np.size > 0:
              input_row = input_np.flatten()
         else:
              return [[]]


    height = 1 # Output is always 1 row high
    width = len(input_row)
    background_color = 0

    # Initialize the output row with the background color
    output_row = [background_color] * width

    # Find all non-background segments in the input row
    all_segments = find_segments_groupby(input_row)

    # If no non-background segments exist, return the background grid
    if not all_segments:
        return [output_row] # Return as list of lists

    # Find the longest segment among all non-background segments
    # max() finds the first element in case of ties in length
    longest_segment = max(all_segments, key=lambda s: s['length'])

    # Copy the longest segment to the output row
    start = longest_segment['start']
    end = longest_segment['end']
    color = longest_segment['color']
    for i in range(start, end + 1):
        # Ensure index is within bounds (should be guaranteed by segment finding)
        if 0 <= i < width:
            output_row[i] = color

    # Return the output grid (as a list of lists)
    return [output_row]