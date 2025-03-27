import numpy as np
from collections import Counter

"""
1. Determine the dimensions (height `H_in`, width `W_in`) of the input grid.
2. Identify the `background_color` by finding the most frequent color value.
3. Find the first (`min_row`) and last (`max_row`) rows containing non-background colors.
4. If no non-background pixels exist, return the input grid.
5. Extract the "pattern block" (rows `min_row` to `max_row`). Let its height be `H_p`.
6. If `H_p` is odd:
   - The `source_sequence` is the pattern block itself.
7. If `H_p` is even:
   - Split the pattern block into top and bottom halves.
   - The `source_sequence` is the bottom half followed by the top half.
8. Create an output grid of the same dimensions as the input.
9. Fill the output grid by repeating the `source_sequence` vertically, using modulo arithmetic on the row index.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    colors, counts = np.unique(grid, return_counts=True)
    return colors[np.argmax(counts)]

def find_pattern_rows(grid, background_color):
    """Finds the min and max row indices containing non-background colors."""
    non_background_rows = np.where(np.any(grid != background_color, axis=1))[0]
    if len(non_background_rows) == 0:
        return None, None # No pattern found
    min_row = non_background_rows[0]
    max_row = non_background_rows[-1]
    return min_row, max_row

def transform(input_grid):
    """
    Transforms the input grid by identifying a pattern block, potentially reordering
    its halves based on height parity, and tiling this sequence vertically.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H_in, W_in = input_np.shape

    # Step 2: Identify the background color
    background_color = find_background_color(input_np)

    # Step 3: Find the row boundaries of the non-background pattern
    min_row, max_row = find_pattern_rows(input_np, background_color)

    # Step 4: Handle case where no pattern is found (grid is uniform)
    if min_row is None:
        return input_grid # Return original grid

    # Step 5: Extract the pattern block and determine its height
    pattern_block = input_np[min_row:max_row+1, :]
    H_p = pattern_block.shape[0]

    # Steps 6 & 7: Determine the source sequence based on pattern height parity
    if H_p % 2 != 0:
        # Odd height: Source sequence is the pattern block itself
        source_sequence = pattern_block
    else:
        # Even height: Split into halves and swap
        half_height = H_p // 2
        top_half = pattern_block[:half_height, :]
        bottom_half = pattern_block[half_height:, :]
        # Concatenate bottom half followed by top half
        source_sequence = np.vstack((bottom_half, top_half))

    # Step 9: Get the length (number of rows) of the source sequence
    L_s = source_sequence.shape[0]

    # Step 10: Initialize the output grid
    output_np = np.zeros((H_in, W_in), dtype=int)

    # Step 11: Fill the output grid by tiling the source sequence
    for i in range(H_in):
        # Use modulo operator to cycle through the source sequence rows
        source_row_index = i % L_s
        output_np[i, :] = source_sequence[source_row_index, :]

    # Step 12: Return the output grid (convert back to list of lists if necessary)
    return output_np.tolist()