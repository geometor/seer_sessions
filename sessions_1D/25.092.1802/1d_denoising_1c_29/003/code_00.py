import numpy as np
import sys

"""
Transforms a single-row input grid (represented as a 1xN NumPy array) by:
1. Identifying the primary non-white color present.
2. Finding all contiguous horizontal segments of this color.
3. Determining the longest segment. If there are multiple segments with the same maximum length, the one starting at the smallest column index is chosen.
4. Creating an output grid of the same dimensions, initially filled with white (0).
5. Copying only the pixels corresponding to the selected longest segment from the input to the output grid, preserving their position and color. All other pixels in the output remain white (0).
If the input grid contains no non-white color, an all-white grid of the same size is returned.
"""

def find_segments(row, color):
    """
    Finds all contiguous segments of a specific color in a 1D list or NumPy array.

    Args:
        row (list | np.ndarray): The input row.
        color (int): The color to find segments of.

    Returns:
        list: A list of dictionaries, where each dictionary represents a segment
              and contains 'start' (index) and 'length'. Returns an empty list
              if no segments are found or the color is 0.
    """
    if color == 0:
        return []

    segments = []
    in_segment = False
    start_index = -1
    row_len = len(row)

    for i, pixel in enumerate(row):
        # Start of a new segment
        if pixel == color and not in_segment:
            in_segment = True
            start_index = i
        # End of the current segment
        elif pixel != color and in_segment:
            in_segment = False
            segments.append({"start": start_index, "length": i - start_index})

    # Handle case where segment extends to the end of the row
    if in_segment:
        segments.append({"start": start_index, "length": row_len - start_index})

    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by keeping only the longest contiguous segment
    of the non-white color, breaking length ties with the leftmost segment.

    Args:
        input_grid (np.ndarray): A NumPy array of shape (1, Width).

    Returns:
        np.ndarray: The transformed grid, a NumPy array of the same shape.
    """
    # Validate input shape
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
        # Handle unexpected input shape if necessary, though ARC examples usually conform
        print(f"Warning: Input grid shape {input_grid.shape} is not (1, N). Returning input.", file=sys.stderr)
        return input_grid

    input_row = input_grid[0]
    height, width = input_grid.shape # height will be 1

    # Initialize output grid
    output_grid = np.zeros_like(input_grid)
    output_row = output_grid[0] # Get a view of the output row

    # --- Workflow ---

    # 1. Identify the primary non-white color
    non_white_color = 0
    unique_colors = np.unique(input_row)
    for color in unique_colors:
        if color != 0:
            non_white_color = color
            break # Assume only one non-white color as per examples

    # If the grid is all white, return the initialized all-white output grid
    if non_white_color == 0:
        return output_grid

    # 2. Find all contiguous segments of the non-white color
    # Pass the input row directly to find_segments
    segments = find_segments(input_row, non_white_color)

    # 3. Determine the segment with the maximum length, breaking ties with start index
    longest_segment = None
    max_length = -1 # Use -1 to handle cases where no segments are found
    min_start_for_max_length = width # Initialize with a value larger than any possible index

    if segments:
        # First pass: find the maximum length
        for segment in segments:
            if segment["length"] > max_length:
                max_length = segment["length"]

        # Second pass: find the segment with max_length and the minimum start index
        for segment in segments:
            if segment["length"] == max_length:
                if segment["start"] < min_start_for_max_length:
                    min_start_for_max_length = segment["start"]
                    # Keep the entire segment dictionary for clarity
                    longest_segment = segment

    # 4. Copy the longest segment to the output grid
    if longest_segment:
        start = longest_segment["start"]
        length = longest_segment["length"]
        # Iterate through the indices of the longest segment and update output row
        for i in range(start, start + length):
            # Check bounds just in case, though segment logic should prevent issues
            if 0 <= i < width:
                output_row[i] = non_white_color

    # 5. Return the completed output grid (already modified in place via output_row view)
    return output_grid