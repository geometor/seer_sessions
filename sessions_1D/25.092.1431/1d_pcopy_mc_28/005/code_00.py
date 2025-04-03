import numpy as np

"""
Transformation Rule Natural Language Program:

1.  Verify the input grid is a list containing exactly one list (the row). Let the width of this row be `N`.
2.  Create a new output row of width `N`, initialized entirely with the background color (white, 0).
3.  Initialize a scan index `i` to 0.
4.  While the scan index `i` is less than `N`:
    a.  Get the color `C_in` of the pixel at index `i` in the input row.
    b.  If `C_in` is the background color (0), increment `i` by 1 and continue to the next iteration.
    c.  If `C_in` is not the background color:
        i.   Record the starting index `S_in = i` and the color `C = C_in`.
        ii.  Determine the length `L_in` of the contiguous segment of color `C` starting at `S_in`. Scan forward from `i` until the color changes or the end of the row is reached.
        iii. Based on `L_in`:
             - If `L_in` is 1, set the output start index `S_out = S_in - 1`.
             - If `L_in` is 3, set the output start index `S_out = S_in`.
             - (Assume no other lengths occur based on examples).
        iv.  Set the output segment length `L_out = 3`.
        v.   Draw the output segment: For each position `k` from 0 to `L_out - 1` (i.e., 0, 1, 2), calculate the target index `idx = S_out + k`. If `idx` is a valid index within the output row (i.e., `0 <= idx < N`), set the pixel at `idx` in the output row to color `C`.
        vi.  Update the scan index `i` to `S_in + L_in` to move past the segment just processed.
5.  Once the loop finishes (i >= N), wrap the completed output row in a list.
6.  Return the resulting list containing the single output row.
"""

def find_segment(row, start_index):
    """
    Finds the contiguous segment of the same color starting at start_index.

    Args:
        row (np.array): The input row.
        start_index (int): The starting index to check.

    Returns:
        tuple: (color, length) of the segment, or (0, 1) if the start pixel is background.
               Returns (None, 0) if start_index is out of bounds.
    """
    width = len(row)
    if not (0 <= start_index < width):
        return None, 0 # Out of bounds

    color = row[start_index]
    if color == 0:
        return 0, 1 # Background pixel, treat as segment of length 1 for scanning purposes

    length = 0
    for i in range(start_index, width):
        if row[i] == color:
            length += 1
        else:
            break
    return color, length

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (expected to be a single row).
    Identifies non-white horizontal segments. Segments of length 1 are expanded
    to length 3 starting one position left. Segments of length 3 remain
    length 3 at the same starting position.
    """
    # 1. Verify input and get row/width
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Raising an error as the input structure is critical and assumed by ARC tasks
        raise ValueError("Input grid must be a list containing exactly one list (the row)")

    input_row = np.array(input_grid[0], dtype=int)
    width = len(input_row)

    # 2. Create output row initialized with background color
    output_row = np.zeros(width, dtype=int)

    # 3. Initialize scan index
    i = 0

    # 4. Scan through the input row
    while i < width:
        # a & b. Check pixel color - find_segment handles background implicitly
        # c. Find the segment starting at i
        start_index_in = i
        block_color, block_length_in = find_segment(input_row, start_index_in)

        # If it's a non-background block
        if block_color != 0:
             # iii. Determine output start index based on input length
            output_start_index = -1 # Default invalid
            if block_length_in == 1:
                output_start_index = start_index_in - 1
            elif block_length_in == 3:
                output_start_index = start_index_in
            # else: other lengths ignored based on examples

            # iv. Set output length
            output_length = 3

            # v. Draw the output segment if a valid rule was found
            if output_start_index != -1:
                for k in range(output_length):
                    write_index = output_start_index + k
                    # Ensure the write index is within the grid bounds
                    if 0 <= write_index < width:
                        output_row[write_index] = block_color

        # vi. Update scan index to move past the processed segment (or single background pixel)
        i += block_length_in

    # 5. Wrap the output row in a list
    output_grid = [output_row.tolist()]

    # 6. Return the result
    return output_grid