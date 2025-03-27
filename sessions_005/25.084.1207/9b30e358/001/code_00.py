"""
Identifies a repeating pattern segment at the bottom of the input grid and uses it to construct the output grid by repeating the segment vertically.

1. Determine the height (H_in) and width (W) of the input grid.
2. Identify the background color, typically the color of the pixel at the top-left corner (0, 0).
3. Scan the input grid row by row, starting from the top (row 0), to find the index of the first row (R) that contains at least one pixel with a color different from the background color.
4. If no such row exists (i.e., the grid is entirely the background color), the output grid is identical to the input grid.
5. Otherwise, extract the "pattern block" which consists of the subgrid from row R down to the last row (H_in - 1).
6. Calculate the height of this pattern block: H_pattern = H_in - R.
7. Calculate the number of full pattern repetitions that fit into the output height: N_full = H_in // H_pattern.
8. Calculate the number of rows required for a partial repetition at the beginning: N_partial = H_in % H_pattern.
9. Initialize an empty output grid with dimensions H_in x W.
10. If N_partial is greater than 0, extract the last N_partial rows from the pattern_block and place them at the top of the output grid (from row 0 to N_partial - 1).
11. Starting from the row index where the partial pattern ended (or row 0 if N_partial was 0), append N_full complete copies of the pattern_block vertically until the output grid is filled.
12. Return the constructed output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by identifying a pattern at the bottom and repeating it vertically.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    H_in, W = input_array.shape

    # Identify the background color (assuming top-left pixel is representative)
    background_color = input_array[0, 0]

    # Find the starting row (R) of the pattern block
    pattern_start_row = -1
    for r in range(H_in):
        if not np.all(input_array[r, :] == background_color):
            pattern_start_row = r
            break

    # Handle case where the entire grid is the background color
    if pattern_start_row == -1:
        return input_grid # Output is identical to input

    # Extract the pattern block
    pattern_block = input_array[pattern_start_row:, :]
    H_pattern = pattern_block.shape[0]

    # Calculate repetition parameters
    if H_pattern == 0: # Should not happen if pattern_start_row != -1, but safety check
         return input_grid # Or handle as an error/empty grid? Return input for now.

    N_full = H_in // H_pattern
    N_partial = H_in % H_pattern

    # Initialize the output grid (NumPy array for easier assembly)
    # Using -1 as a placeholder to ensure all cells get filled
    output_array = np.full((H_in, W), -1, dtype=int)

    current_row = 0

    # Place the partial pattern at the top if needed
    if N_partial > 0:
        partial_pattern = pattern_block[-N_partial:, :]
        output_array[0:N_partial, :] = partial_pattern
        current_row = N_partial

    # Place the full pattern repetitions
    for _ in range(N_full):
        output_array[current_row : current_row + H_pattern, :] = pattern_block
        current_row += H_pattern

    # Ensure the output grid is fully filled (debugging check)
    if np.any(output_array == -1):
        # This indicates an error in the logic or calculation
        print("Warning: Output grid not fully filled. There might be an issue.")
        # Fill remaining with background as a fallback, though ideally this shouldn't be needed
        output_array[output_array == -1] = background_color

    # Convert the final NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid