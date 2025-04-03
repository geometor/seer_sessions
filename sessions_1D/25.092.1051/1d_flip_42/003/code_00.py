import numpy as np

"""
Moves a single 'marker' pixel from the left side of a contiguous block of a different color to the right side of that block in a 1D array (represented as a 1xN grid). The marker and block are surrounded by white pixels or grid boundaries.
"""

def find_marker_and_block_1d(grid_1d):
    """
    Scans a 1D numpy array to find the marker pixel and the end of the adjacent block.

    Args:
        grid_1d (np.array): The 1D input grid.

    Returns:
        tuple: (marker_color, marker_index, block_end_index)
               Returns (None, -1, -1) if the specific pattern is not found.
    """
    n = len(grid_1d)
    for i in range(n - 1):
        # Check for potential marker: non-white, followed by different non-white
        if grid_1d[i] != 0 and grid_1d[i+1] != 0 and grid_1d[i] != grid_1d[i+1]:
            # Check boundary condition: marker preceded by white or grid start
            if i == 0 or grid_1d[i-1] == 0:
                marker_color = grid_1d[i]
                marker_index = i
                block_color = grid_1d[i+1]
                block_start_index = i + 1
                block_end_index = block_start_index

                # Find the end of the contiguous block
                for j in range(block_start_index + 1, n):
                    if grid_1d[j] == block_color:
                        block_end_index = j
                    else:
                        break # Block ended

                # Check boundary condition: block followed by white or grid end
                if block_end_index == n - 1 or grid_1d[block_end_index + 1] == 0:
                    # Found the unique pattern
                    return marker_color, marker_index, block_end_index

    # Pattern not found
    return None, -1, -1


def transform(input_grid):
    """
    Transforms the input grid by moving the marker pixel.

    Args:
        input_grid (list): A list of lists representing the input grid (assumed 1xN).

    Returns:
        list: A list of lists representing the transformed grid (1xN).
    """
    # Convert input list of lists (1xN) to a 1D numpy array
    # Check if input_grid is empty or not a list of lists
    if not input_grid or not isinstance(input_grid, list) or not isinstance(input_grid[0], list):
         # Handle invalid input if necessary, perhaps return input or raise error
         # For ARC, inputs are generally valid lists of lists.
         # If input is guaranteed to be 1xN, this check might be simplified.
         print("Warning: Unexpected input format. Assuming 1xN grid.")
         # If input_grid is just a flat list, handle that:
         if isinstance(input_grid, list) and all(isinstance(x, int) for x in input_grid):
              input_array_1d = np.array(input_grid, dtype=int)
         elif input_grid and isinstance(input_grid[0], list):
              input_array_1d = np.array(input_grid[0], dtype=int)
         else: # Cannot confidently process, return original
             return input_grid # Or raise an error
    else:
         input_array_1d = np.array(input_grid[0], dtype=int)


    # Find the marker and block details using the helper function
    marker_color, marker_index, block_end_index = find_marker_and_block_1d(input_array_1d)

    # If the pattern wasn't found, return the original grid unchanged
    if marker_index == -1:
        return input_grid

    # Create a copy of the input array to modify for the output
    output_array_1d = np.copy(input_array_1d)

    # Step 3a: Set the original marker position to white (0)
    output_array_1d[marker_index] = 0

    # Step 3b: Calculate the new position for the marker
    new_marker_index = block_end_index + 1

    # Step 3c: Set the position immediately after the block to the marker color
    # Check array bounds just in case, though examples suggest it fits.
    if new_marker_index < len(output_array_1d):
         output_array_1d[new_marker_index] = marker_color
    # else: # Handle edge case if necessary (e.g., print warning or error)
         # Based on examples, this is unlikely to be needed.

    # Convert the output 1D numpy array back to a list of lists (1xN) format
    output_grid = [output_array_1d.tolist()]

    return output_grid