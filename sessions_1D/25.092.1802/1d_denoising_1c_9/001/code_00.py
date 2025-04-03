import numpy as np

"""
Identify all contiguous horizontal segments of non-white pixels in the input row.
Select the segment with the maximum length.
Create an output row of the same dimensions as the input, filled with the background color (white, 0).
Copy the pixels corresponding to the longest segment found in the input into the same positions in the output row.
"""

def find_segments(row):
    """
    Finds all contiguous segments of non-white pixels in a 1D array (row).

    Args:
        row (np.array): A 1D numpy array representing the input row.

    Returns:
        list: A list of tuples, where each tuple represents a segment
              (start_index, end_index, length, color). Returns an empty list
              if no non-white segments are found.
    """
    segments = []
    current_segment_start = -1
    current_segment_color = 0
    width = len(row)

    for i, pixel in enumerate(row):
        is_non_white = pixel != 0

        # Start of a new segment
        if is_non_white and current_segment_start == -1:
            current_segment_start = i
            current_segment_color = pixel
        # End of the current segment (found white or different color)
        elif (not is_non_white or pixel != current_segment_color) and current_segment_start != -1:
            start = current_segment_start
            end = i # end is exclusive for slicing later, but inclusive for index
            length = end - start
            segments.append((start, end -1, length, current_segment_color))
            current_segment_start = -1
            current_segment_color = 0
            # Check if the current pixel starts a *new* segment immediately
            if is_non_white:
                current_segment_start = i
                current_segment_color = pixel


    # Handle segment that goes to the end of the row
    if current_segment_start != -1:
        start = current_segment_start
        end = width
        length = end - start
        segments.append((start, end - 1, length, current_segment_color))

    return segments

def transform(input_grid):
    """
    Transforms the input grid by keeping only the longest contiguous horizontal
    segment of non-white pixels and setting all other pixels to white (0).

    Args:
        input_grid (list): A list containing a single list (the row) of integers.

    Returns:
        list: The transformed grid in the same format.
    """
    # Ensure input is a numpy array for easier processing
    # The input is a list containing one list (the row)
    input_row = np.array(input_grid[0])
    height = 1
    width = len(input_row)

    # Initialize output_grid with background color (white, 0)
    output_row = np.zeros_like(input_row)

    # Find all contiguous non-white segments in the input row
    segments = find_segments(input_row)

    # If no segments found, return the all-white grid
    if not segments:
        return [output_row.tolist()] # Return in the original list-of-lists format

    # Find the longest segment
    longest_segment = None
    max_length = 0
    for segment in segments:
        start, end, length, color = segment
        if length > max_length:
            max_length = length
            longest_segment = segment

    # Copy the pixels of the longest segment to the output grid
    if longest_segment:
        start, end, length, color = longest_segment
        # Note: end index from find_segments is inclusive, slicing is exclusive
        output_row[start : end + 1] = color 

    # Convert the numpy row back to the required list-of-lists format
    output_grid = [output_row.tolist()]

    return output_grid