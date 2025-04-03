import numpy as np

"""
Transformation Rule:

Identify contiguous horizontal segments of non-white pixels in the input grid (which is always a single row).
For each segment found:
  - If the length of the segment is greater than 2 pixels:
    - Keep the first pixel (start of the segment) and the last pixel (end of the segment) unchanged.
    - Change all pixels strictly *between* the start and end pixels to white (0).
  - If the length of the segment is 2 or less, leave the segment unchanged.
Keep all background white pixels (0) unchanged.
The output grid has the same dimensions as the input grid.
"""

def find_non_white_segments(row):
    """
    Finds contiguous segments of non-white pixels in a 1D numpy array (row).

    Args:
        row: A 1D numpy array representing a row of the grid.

    Returns:
        A list of tuples, where each tuple represents a segment
        and contains (start_index, end_index, color).
        Returns an empty list if no non-white segments are found.
    """
    segments = []
    in_segment = False
    segment_start = -1
    segment_color = -1
    width = len(row)

    for i in range(width):
        pixel = row[i]
        is_non_white = pixel != 0

        if is_non_white and not in_segment:
            # Start of a new segment
            in_segment = True
            segment_start = i
            segment_color = pixel
        elif (not is_non_white or i == width - 1) and in_segment:
            # End of the current segment
            segment_end = i - 1 if not is_non_white else i
            segments.append((segment_start, segment_end, segment_color))
            in_segment = False
            segment_start = -1
            segment_color = -1
        elif is_non_white and in_segment and pixel != segment_color:
             # End of the previous segment (color changed)
            segment_end = i - 1
            segments.append((segment_start, segment_end, segment_color))
            # Start of a new segment immediately
            segment_start = i
            segment_color = pixel


    return segments


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Identifies horizontal segments of non-white pixels. If a segment's length
    is greater than 2, it blanks out the interior pixels (changes them to white/0),
    keeping only the start and end pixels of the segment.

    Args:
        input_grid: A 2D numpy array representing the input grid (single row).

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Ensure input is a numpy array
    input_grid_np = np.array(input_grid)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    
    # Since the task description and examples imply a single row, process only the first row.
    # If grids could have multiple rows, this would need adjustment.
    if input_grid_np.shape[0] == 1:
        row = output_grid[0]
        segments = find_non_white_segments(row)

        # Process each found segment
        for start, end, color in segments:
            length = end - start + 1
            
            # If segment length is greater than 2, blank out the middle
            if length > 2:
                for i in range(start + 1, end):
                    output_grid[0, i] = 0 # Set interior pixels to white
    else:
        # Handle potential multi-row cases if needed in the future,
        # though current examples are single-row.
        # For now, just return the copy if not a single row grid.
        print("Warning: Input grid has more than one row. This specific transformation logic assumes a single row.")
        pass # Or implement multi-row logic if required

    return output_grid.tolist() # Return as list of lists per ARC standard