"""
Modifies horizontal segments of non-background pixels (non-zero) in a single-row grid 
by hollowing them out, keeping only the endpoints. 
Specifically, for segments of length greater than 2, the pixels between the first 
and last pixel of the segment are set to the background color (0).
Segments of length 1 or 2 remain unchanged.
Background pixels (0) are also unchanged.
"""

import numpy as np

def find_segments(row):
    """
    Finds contiguous horizontal segments of non-zero pixels in a 1D list (row).

    Args:
        row: A list of integers representing a row of the grid.

    Returns:
        A list of tuples, where each tuple represents a segment and contains
        (start_index, end_index, color). Returns an empty list if no segments
        are found.
    """
    segments = []
    start_index = -1
    segment_color = -1

    for i, pixel in enumerate(row):
        if pixel != 0:
            # Start of a new segment or continuation of the current one
            if start_index == -1:
                start_index = i
                segment_color = pixel
            # Ensure contiguous segments are of the same color (though not strictly required by examples, good practice)
            elif pixel != segment_color:
                # End the previous segment of a different color
                segments.append((start_index, i - 1, segment_color))
                # Start the new segment
                start_index = i
                segment_color = pixel
        elif start_index != -1:
            # End of the current segment (encountered a 0)
            segments.append((start_index, i - 1, segment_color))
            start_index = -1
            segment_color = -1

    # Handle segment that goes to the end of the row
    if start_index != -1:
        segments.append((start_index, len(row) - 1, segment_color))

    return segments

def transform(input_grid):
    """
    Applies the hollowing transformation to segments in the input grid.

    Args:
        input_grid: A list of lists representing the input grid (assumed 1xN).

    Returns:
        A list of lists representing the transformed grid.
    """
    # Ensure input is treated as a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Handle empty input case
    if input_np.size == 0:
        return []

    # Assume the grid is 1xN as per examples
    if input_np.shape[0] != 1:
        # Or raise an error if unexpected shape
        print("Warning: Expected a 1xN grid, processing only the first row.")

    # Work on a copy to avoid modifying the original input
    output_np = np.copy(input_np)
    row = output_np[0] # Get the first (and only) row

    # Find all non-zero segments in the row
    segments = find_segments(row.tolist()) # find_segments expects a list

    # Iterate through the identified segments
    for start, end, color in segments:
        length = end - start + 1
        # Apply hollowing only if the segment length is greater than 2
        if length > 2:
            # Iterate from the pixel after the start to the pixel before the end
            for i in range(start + 1, end):
                # Set the inner pixels to background color (0)
                row[i] = 0

    # Update the output array (in case changes were made directly to 'row')
    output_np[0] = row

    # Return the result as a list of lists
    return output_np.tolist()