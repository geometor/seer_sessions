import numpy as np

"""
Transforms an input grid by processing each row independently. 
For each row:
1. Identifies the unique non-white color C (if any).
2. Finds all column indices where color C appears.
3. Groups these indices into consecutive pairs (1st & 2nd, 3rd & 4th, etc.). If there's an odd number of indices, the last one is ignored.
4. For each pair (start_idx, end_idx), it fills the segment of the output grid's corresponding row from start_idx to end_idx (inclusive) with color C.
Rows containing only the background color (white=0) or fewer than two non-white pixels of the target color remain unchanged.
"""

def find_color_indices_in_row(row):
    """
    Finds the unique non-white color and all its indices in a single row.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (non_white_color, indices)
               - non_white_color: The integer value of the unique non-white color, or None if none found.
               - indices: A numpy array of column indices where the non_white_color appears. Empty if no non-white color found.
    """
    non_white_color = None
    indices = np.array([], dtype=int)

    # Find indices of all non-zero elements
    non_zero_indices = np.where(row != 0)[0]

    if len(non_zero_indices) > 0:
        # Determine the non-white color (assuming only one per row based on examples)
        non_white_color = row[non_zero_indices[0]]
        # Find all indices specifically for this color
        indices = np.where(row == non_white_color)[0]

    return non_white_color, indices


def transform(input_grid):
    """
    Applies the row-wise segment filling transformation based on paired indices.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: The transformed 2D numpy array.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(rows):
        current_row = input_grid[r, :]

        # Find the non-white color and its indices in the current row
        non_white_color, color_indices = find_color_indices_in_row(current_row)

        # Proceed only if a non-white color exists and there are at least two indices
        if non_white_color is not None and len(color_indices) >= 2:
            
            # Iterate through the indices in pairs (0, 1), (2, 3), ...
            # The range ensures we only process pairs and safely access k and k+1.
            # It effectively ignores the last index if the count is odd.
            for k in range(0, len(color_indices) // 2 * 2, 2):
                start_col = color_indices[k]
                end_col = color_indices[k+1]

                # Fill the corresponding segment in the output grid's row
                # Slicing includes start_col but excludes end_col + 1, hence the +1
                output_grid[r, start_col : end_col + 1] = non_white_color

    # Return the modified output grid
    return output_grid