import numpy as np

"""
Recolors contiguous horizontal blocks of green (3) pixels based on their length.
Odd length green blocks become azure (8).
Even length green blocks become magenta (6).
White (0) pixels remain unchanged.
"""

def find_segments(row, target_color):
    """
    Finds contiguous segments of a target color in a 1D array (row).

    Args:
        row (np.array): A 1D numpy array representing a grid row.
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of tuples, where each tuple contains (start_index, length)
              of a found segment.
    """
    segments = []
    n_cols = len(row)
    col = 0
    while col < n_cols:
        # Skip pixels that are not the target color
        if row[col] != target_color:
            col += 1
            continue

        # Found the start of a target color segment
        start_col = col
        segment_length = 0
        while col < n_cols and row[col] == target_color:
            segment_length += 1
            col += 1
        # End of the segment found (or end of row)
        segments.append((start_col, segment_length))
        # col is already advanced past the segment
    return segments

def transform(input_grid):
    """
    Transforms the input grid by recoloring green segments based on length parity.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    # This preserves background (0) and any other non-target pixels
    output_np = input_np.copy()

    green_color = 3
    azure_color = 8
    magenta_color = 6

    # Iterate through each row of the grid
    for r_idx in range(input_np.shape[0]):
        row = input_np[r_idx]
        output_row = output_np[r_idx]

        # Find all green segments in the current row
        green_segments = find_segments(row, green_color)

        # Process each found green segment
        for start_col, length in green_segments:
            # Determine the replacement color based on length parity
            # Odd length -> azure (8)
            # Even length -> magenta (6)
            replacement_color = azure_color if length % 2 != 0 else magenta_color

            # Calculate the end column index (exclusive)
            end_col = start_col + length

            # Update the corresponding segment in the output row
            output_row[start_col:end_col] = replacement_color

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()