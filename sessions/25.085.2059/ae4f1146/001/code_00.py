"""
Finds the 3x3 subgrid within the input grid that contains only azure (8) and blue (1) pixels
and has the maximum number of blue (1) pixels. If there's a tie in the blue pixel count,
the subgrid located topmost (minimum row index) is chosen. If there's still a tie,
the subgrid located leftmost (minimum column index) is chosen. The selected 3x3 subgrid
is returned as the output.
"""

import numpy as np

def is_valid_subgrid(subgrid):
    """
    Checks if a 3x3 subgrid contains only azure (8) and blue (1) pixels.

    Args:
        subgrid (np.array): A 3x3 numpy array representing the subgrid.

    Returns:
        bool: True if the subgrid contains only pixels with values 1 or 8, False otherwise.
    """
    # Check if all elements in the subgrid are present in the allowed set [1, 8]
    return np.all(np.isin(subgrid, [1, 8]))

def transform(input_grid):
    """
    Identifies and extracts a specific 3x3 subgrid from the input grid based on content rules.

    The function scans the input grid for all 3x3 subgrids containing only azure (8) and blue (1)
    pixels. Among these valid candidates, it selects the one with the highest count of blue (1)
    pixels. Ties are broken by choosing the subgrid with the smallest row index for its top-left
    corner, and then by the smallest column index if rows are also tied.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        np.array: A 3x3 numpy array representing the selected subgrid.
                  Returns None if no valid 3x3 subgrid is found (though this is
                  not expected based on the provided examples).
    """
    # Convert input list of lists to a numpy array for efficient slicing and operations
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Ensure the grid is large enough to contain a 3x3 subgrid
    if height < 3 or width < 3:
        # Or raise an error, or return an empty grid, depending on requirements
        return None

    # Initialize variables to keep track of the best candidate subgrid found so far:
    # max_blue_count: Stores the highest number of blue pixels found in a valid subgrid. Initialized to -1
    #                 to ensure the first valid subgrid found is always considered better.
    # best_subgrid_pos: Stores the top-left (row, col) tuple of the best subgrid found so far.
    # best_subgrid: Stores the actual 3x3 numpy array of the best subgrid found so far.
    max_blue_count = -1
    best_subgrid_pos = None
    best_subgrid = None # This will hold the final output grid

    # Iterate through all possible top-left starting positions (r, c) for a 3x3 subgrid.
    # The row index `r` can go from 0 up to `height - 3`.
    # The column index `c` can go from 0 up to `width - 3`.
    for r in range(height - 2):
        for c in range(width - 2):
            # Extract the 3x3 subgrid starting at the current position (r, c)
            subgrid = input_np[r:r+3, c:c+3]

            # Check if this 3x3 subgrid is a valid candidate
            # (contains *only* azure (8) and blue (1) pixels).
            if is_valid_subgrid(subgrid):
                # If it's a valid candidate, count the number of blue (1) pixels within it.
                current_blue_count = np.count_nonzero(subgrid == 1)

                # Determine if the current subgrid is better than the best one found so far.
                is_better = False
                if current_blue_count > max_blue_count:
                    # Found a subgrid with strictly more blue pixels.
                    is_better = True
                elif current_blue_count == max_blue_count:
                    # Tie in blue pixel count. Apply tie-breaking rules.
                    # Check if the current position (r, c) is "smaller" (topmost, then leftmost)
                    # than the position of the best subgrid found so far (best_subgrid_pos).
                    # The condition `best_subgrid_pos is None` handles the very first valid subgrid found.
                    if best_subgrid_pos is None or r < best_subgrid_pos[0] or \
                       (r == best_subgrid_pos[0] and c < best_subgrid_pos[1]):
                        is_better = True

                # If the current subgrid is determined to be the new best candidate...
                if is_better:
                    # Update the tracking variables to reflect this new best candidate.
                    max_blue_count = current_blue_count
                    best_subgrid_pos = (r, c)
                    best_subgrid = subgrid # Store the content of the best subgrid

    # After iterating through all possible positions, best_subgrid contains the selected 3x3 grid.
    # Based on the task examples, it's assumed that at least one valid subgrid will always be found.
    # If there's a possibility of no valid subgrid existing, error handling or returning a default
    # value (like None or an empty array) might be necessary here.

    # Return the content of the best 3x3 subgrid found.
    return best_subgrid