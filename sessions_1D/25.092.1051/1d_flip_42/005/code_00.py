import numpy as np

"""
Moves a single 'marker' pixel from the left side of a contiguous block of a different color to the right side of that block within a 1xN grid. The marker and block pattern is identified by specific boundary conditions: the marker must be preceded by white (0) or the grid start, and the block must be followed by white (0) or the grid end.
"""

def find_marker_and_block_1d(grid_1d):
    """
    Scans a 1D numpy array to find the unique marker pixel and the end of the adjacent block,
    checking boundary conditions.

    Args:
        grid_1d (np.array): The 1D input grid row.

    Returns:
        tuple: (marker_color, marker_index, block_end_index)
               Returns (None, -1, -1) if the specific pattern is not found.
    """
    n = len(grid_1d)
    # Iterate through potential marker positions
    for i in range(n - 1):
        # Condition 1: Potential marker pixel is non-white
        # Condition 2: Next pixel is non-white and *different* color
        if grid_1d[i] != 0 and grid_1d[i+1] != 0 and grid_1d[i] != grid_1d[i+1]:
            
            # Condition 3: Marker is at the start OR preceded by white
            is_left_boundary_ok = (i == 0) or (grid_1d[i-1] == 0)
            
            if is_left_boundary_ok:
                # Found a potential marker and the start of a block
                marker_color = grid_1d[i]
                marker_index = i
                block_color = grid_1d[i+1]
                block_start_index = i + 1
                block_end_index = block_start_index # Initialize end index

                # Find the actual end of the contiguous block
                for j in range(block_start_index + 1, n):
                    if grid_1d[j] == block_color:
                        block_end_index = j
                    else:
                        break # End of the block sequence

                # Condition 4: Block is at the end OR followed by white
                is_right_boundary_ok = (block_end_index == n - 1) or (grid_1d[block_end_index + 1] == 0)

                if is_right_boundary_ok:
                    # All conditions met, found the unique pattern
                    return marker_color, marker_index, block_end_index

    # If loop finishes without returning, the pattern was not found
    return None, -1, -1


def transform(input_grid):
    """
    Transforms the input grid by moving the marker pixel.

    Args:
        input_grid (list or np.ndarray): A list of lists or numpy array representing the 1xN input grid.

    Returns:
        list or np.ndarray: The transformed grid in the same format as the input.
    """
    # Convert input to NumPy array if it's not already
    if isinstance(input_grid, list):
        input_array = np.array(input_grid, dtype=int)
    elif isinstance(input_grid, np.ndarray):
        input_array = input_grid.astype(int) # Ensure integer type
    else:
        raise TypeError("Input grid must be a list of lists or a NumPy array.")

    # Ensure the input is 2D, even if 1xN
    if input_array.ndim == 1:
         # This case might occur if input is just [0, 0, 3, 1, 1, 0]
         # Reshape to 2D (1xN)
         input_array = input_array.reshape(1, -1)
         
    # Verify shape is 1xN
    if input_array.shape[0] != 1:
         print(f"Warning: Expected input shape 1xN, but got {input_array.shape}. Processing first row only.")
         # Or return input_grid unchanged if strict 1xN is required
         # return input_grid

    # Extract the first (and only) row for processing
    grid_1d = input_array[0]

    # Find the marker and block details using the helper function
    marker_color, marker_index, block_end_index = find_marker_and_block_1d(grid_1d)

    # If the specific marker/block pattern wasn't found, return the original grid
    if marker_index == -1:
        # Return in the original format
        if isinstance(input_grid, list):
            return input_grid
        else:
            return input_array # Return the potentially reshaped array

    # Create a copy of the input array to modify for the output
    output_array = np.copy(input_array)

    # Calculate the new position for the marker (immediately after the block)
    new_marker_index = block_end_index + 1

    # Check if the new marker position is within the grid bounds
    if new_marker_index < output_array.shape[1]:
        # Perform the move:
        # 1. Set the original marker position to white (0)
        output_array[0, marker_index] = 0
        # 2. Set the new position (after the block) to the marker's color
        output_array[0, new_marker_index] = marker_color
    else:
        # This case shouldn't happen based on examples and boundary checks,
        # but handle defensively. Return unmodified if move is out of bounds.
        print(f"Warning: Calculated new marker position {new_marker_index} is out of bounds. Returning original grid.")
        if isinstance(input_grid, list):
            return input_grid
        else:
            return input_array


    # Return the result in the same format as the input
    if isinstance(input_grid, list):
        return output_array.tolist()
    else:
        return output_array