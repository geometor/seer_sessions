import numpy as np

"""
Identify all contiguous horizontal segments of non-white pixels in the input grid.
Find the maximum length among these segments.
Select the segment(s) with this maximum length.
If there is a tie in length, select the segment that is lowest in the grid (highest row index).
Create an output grid of the same dimensions as the input, initialized to white (0).
Copy the pixels of the single selected segment from the input grid to the output grid at their original positions.
"""

def find_horizontal_segments(grid):
    """
    Identifies all contiguous horizontal segments of non-white pixels.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a segment
              with keys 'color', 'length', 'row_index', 'start_col', 'end_col'.
              Returns an empty list if no non-white pixels are found.
    """
    segments = []
    rows, cols = grid.shape
    for r in range(rows):
        current_segment = None
        for c in range(cols):
            color = grid[r, c]
            if color != 0:  # Non-white pixel
                if current_segment is None:
                    # Start a new segment
                    current_segment = {'color': color, 'length': 1, 'row_index': r, 'start_col': c}
                elif color == current_segment['color']:
                     # Continue the current segment
                    current_segment['length'] += 1
                else:
                    # Different color found, end previous segment and start new one
                    current_segment['end_col'] = c - 1
                    segments.append(current_segment)
                    current_segment = {'color': color, 'length': 1, 'row_index': r, 'start_col': c}

            elif current_segment is not None:
                 # White pixel found, end the current segment
                current_segment['end_col'] = c - 1
                segments.append(current_segment)
                current_segment = None

        # End of row, check if a segment was active
        if current_segment is not None:
            current_segment['end_col'] = cols - 1
            segments.append(current_segment)

    return segments

def transform(input_grid):
    """
    Transforms the input grid by isolating the longest horizontal segment,
    prioritizing the lowest segment in case of ties in length.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid with the same shape as input, filled with white (0)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find all horizontal segments of non-white pixels
    segments = find_horizontal_segments(input_grid)

    # If no segments are found, return the all-white grid
    if not segments:
        return output_grid

    # Find the maximum length among all segments
    max_length = 0
    for segment in segments:
        if segment['length'] > max_length:
            max_length = segment['length']

    # Filter segments to keep only those with the maximum length
    longest_segments = [s for s in segments if s['length'] == max_length]

    # If there's only one longest segment, select it
    if len(longest_segments) == 1:
        selected_segment = longest_segments[0]
    else:
        # If there's a tie in length, find the one with the highest row index (lowest position)
        max_row_index = -1
        selected_segment = None
        for segment in longest_segments:
            if segment['row_index'] > max_row_index:
                max_row_index = segment['row_index']
                selected_segment = segment

    # Copy the pixels of the selected segment to the output grid
    if selected_segment:
        r = selected_segment['row_index']
        color = selected_segment['color']
        start_c = selected_segment['start_col']
        end_c = selected_segment['end_col']
        output_grid[r, start_c : end_c + 1] = color # Use original color from input

    return output_grid