import numpy as np

"""
1.  Input: Assume the input is a single row of pixels (represented as a list of integers within a list). Let `W` be the width of the row.
2.  Initialize: Create a new output row of width `W`, filled entirely with the background color (white, 0).
3.  Scan: Iterate through the input row using an index `i`, starting at 0 and going up to `W-1`.
4.  Segment Detection:
    *   If the pixel at index `i` in the input row is the background color (0), increment `i` and continue scanning.
    *   If the pixel at index `i` is *not* the background color:
        a.  This marks the start of a segment. Record its color (`C`) and its starting index (`S_in = i`).
        b.  Determine the length (`L_in`) of this contiguous segment of color `C` by checking subsequent pixels.
        c.  Apply Transformation Rule:
            *   If `L_in` is 1, calculate the output start index `S_out = S_in - 1`.
            *   If `L_in` is 3, calculate the output start index `S_out = S_in`.
            *   (Assume only lengths 1 and 3 occur based on examples).
        d.  Draw Output: Write a segment of color `C` and length 3 into the *output* row, starting at index `S_out`. Ensure that writing only occurs for indices `idx` where `0 <= idx < W`. For `k` from 0 to 2, calculate `idx = S_out + k`; if `idx` is valid, set `output_row[idx] = C`.
        e.  Advance Scanner: Set `i = S_in + L_in` to continue scanning after this input segment.
5.  Output: Once the scan is complete (`i >= W`), return the output row wrapped in a list structure (e.g., `[output_row]`).
"""


def find_segment(row, start_index):
    """
    Finds the contiguous segment of the same color starting at start_index.

    Args:
        row (np.array): The input row.
        start_index (int): The starting index to check.

    Returns:
        tuple: (color, length) of the segment.
               If the pixel at start_index is background (0), returns (0, 1).
               Returns (None, 0) if start_index is out of bounds.
    """
    width = len(row)
    if not (0 <= start_index < width):
        # Handle out-of-bounds index
        return None, 0 

    color = row[start_index]
    # If the starting pixel is background, treat it as a segment of length 1 for scanning purposes
    if color == 0:
        return 0, 1 

    # If starting pixel is non-background, find the length of the contiguous segment
    length = 0
    for i in range(start_index, width):
        if row[i] == color:
            length += 1
        else:
            # Stop when color changes
            break
    return color, length

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (expected to be a single row).
    Identifies non-white horizontal segments. Segments of length 1 are expanded
    to length 3 starting one position left. Segments of length 3 remain
    length 3 at the same starting position.
    """
    # 1. Verify input format and extract the row/width
    # ARC format expects a list of lists, even for a single row.
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Raise error for unexpected input format
        raise ValueError("Input grid must be a list containing exactly one list (the row)")

    input_row = np.array(input_grid[0], dtype=int)
    width = len(input_row)

    # 2. Initialize output row with background color
    output_row = np.zeros(width, dtype=int)

    # 3. Initialize scan index
    i = 0

    # 4. Scan through the input row
    while i < width:
        # c. Find the segment starting at the current scan index `i`
        start_index_in = i
        block_color, block_length_in = find_segment(input_row, start_index_in)

        # Check if the found segment is a non-background block
        if block_color != 0:
             # c.iii. Determine output start index based on input length
            output_start_index = -1 # Initialize with an invalid index

            if block_length_in == 1:
                # Rule: Length 1 shifts left by 1
                output_start_index = start_index_in - 1
            elif block_length_in == 3:
                # Rule: Length 3 stays in place
                output_start_index = start_index_in
            # Note: Other lengths are ignored based on observed examples

            # c.iv. Set output length (always 3)
            output_length = 3

            # c.v. Draw the output segment onto the output_row, checking bounds
            if output_start_index != -1: # Proceed only if a valid rule was applied
                for k in range(output_length):
                    write_index = output_start_index + k
                    # Check if the calculated write index is within the grid bounds [0, width-1]
                    if 0 <= write_index < width:
                        output_row[write_index] = block_color

        # 4.e. Update scan index to move past the processed segment
        # block_length_in will be 1 for background pixels or the length of the non-background segment
        i += block_length_in

    # 5. Wrap the completed output row in a list to match ARC format
    output_grid = [output_row.tolist()]

    # 6. Return the result
    return output_grid