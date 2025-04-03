"""
Transformation Rule:
1. Iterate through each row of the input grid independently.
2. For each row, identify all contiguous horizontal segments (blocks) of blue pixels (value 1).
3. Determine the length of each blue segment found.
4. Find the maximum length among these segments within the row.
5. Identify the blue segment(s) in the row that have this maximum length.
6. If there's only one segment with the maximum length, select it.
7. If multiple segments share the maximum length, select the one that appears earliest (i.e., has the smallest starting column index).
8. Change the color of all pixels within this selected segment from blue (1) to yellow (4).
9. Leave all other pixels (including other blue segments that were not selected) unchanged.
10. The output grid has the same dimensions as the input grid.
"""

import numpy as np

def find_segments(sequence, target_color):
    """
    Finds all contiguous segments of a target color in a 1D sequence (list or 1D numpy array).

    Args:
        sequence (list or np.ndarray): The input sequence of colors (integers).
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of dictionaries, where each dictionary represents a segment
              and contains 'start' (index), 'end' (index), and 'length'.
              Returns an empty list if no segments are found.
    """
    segments = []
    start_index = -1
    n = len(sequence)
    for i, color in enumerate(sequence):
        # Check if the current color matches the target color
        is_target = (color == target_color)

        if is_target and start_index == -1:
            # Start of a new segment
            start_index = i
        elif not is_target and start_index != -1:
            # End of the current segment (because color changed or it's the end of the sequence)
            segments.append({
                'start': start_index,
                'end': i - 1,
                'length': i - start_index
            })
            start_index = -1 # Reset for the next potential segment

    # Check if the sequence ends with a target segment
    if start_index != -1:
        segments.append({
            'start': start_index,
            'end': n - 1,
            'length': n - start_index
        })

    return segments

def transform(input_grid):
    """
    Transforms the input grid by changing the longest contiguous block
    of blue (1) pixels in each row to yellow (4). If there's a tie in length
    within a row, the earliest block (smallest start index) is chosen for that row.

    Args:
        input_grid (np.ndarray): A 2D NumPy array representing the input grid.

    Returns:
        np.ndarray: The transformed 2D NumPy array.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    num_rows, num_cols = input_grid.shape

    # Iterate through each row
    for r in range(num_rows):
        # Extract the current row
        row_sequence = input_grid[r, :]

        # 1. & 2. Find all blue segments in the current row
        blue_segments = find_segments(row_sequence, target_color=1)

        # If no blue segments in this row, continue to the next row
        if not blue_segments:
            continue

        # 3. & 4. Find the maximum length among blue segments in this row
        max_length = 0
        for segment in blue_segments:
            if segment['length'] > max_length:
                max_length = segment['length']

        # 5. Filter segments to find all that have the maximum length
        longest_segments = [s for s in blue_segments if s['length'] == max_length]

        # 6. & 7. Select the target segment (earliest start index in case of tie)
        # The min function with a key naturally handles finding the earliest segment
        target_segment = min(longest_segments, key=lambda s: s['start'])

        # 8. Modify the output grid row based on the target segment
        start_col = target_segment['start']
        end_col = target_segment['end']
        for c in range(start_col, end_col + 1):
            # Change blue (1) to yellow (4) in the output grid
            if output_grid[r, c] == 1: # Ensure it's still blue before changing
                 output_grid[r, c] = 4

    # Return the modified grid
    return output_grid