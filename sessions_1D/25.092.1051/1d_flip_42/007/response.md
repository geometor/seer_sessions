```python
import numpy as np

"""
Transforms a 1xN grid by finding a specific pattern: a single non-white 'marker' pixel adjacent to a contiguous block of a different non-white color. This pattern must be bounded by white (0) pixels or grid edges. The transformation swaps the marker and the block: the block shifts one position left to occupy the marker's original position, and the marker moves to the position immediately following the block's original end position.
"""

def find_marker_and_block_1d(grid_1d):
    """
    Scans a 1D numpy array to find the unique marker pixel and the adjacent block,
    checking boundary conditions.

    Args:
        grid_1d (np.array): The 1D input grid row.

    Returns:
        tuple: (marker_color, marker_index, block_color, block_end_index)
               Returns (None, -1, None, -1) if the specific pattern is not found.
    """
    n = len(grid_1d)
    # Iterate through potential marker positions (up to second to last element)
    for i in range(n - 1):
        # Condition 1 & 2: Current pixel is non-white (marker), next is non-white and DIFFERENT color (start of block)
        if grid_1d[i] != 0 and grid_1d[i+1] != 0 and grid_1d[i] != grid_1d[i+1]:
            
            # Condition 3: Marker is at the start OR preceded by white
            is_left_boundary_ok = (i == 0) or (grid_1d[i-1] == 0)
            
            if is_left_boundary_ok:
                # Potential pattern found, identify components
                marker_color = grid_1d[i]
                marker_index = i
                block_color = grid_1d[i+1]
                block_start_index = i + 1
                block_end_index = block_start_index # Initialize block end index

                # Find the actual end of the contiguous block of 'block_color'
                for j in range(block_start_index + 1, n):
                    if grid_1d[j] == block_color:
                        block_end_index = j
                    else:
                        break # Block sequence ended

                # Condition 4: Block is at the end OR followed by white
                # Ensure check doesn't go out of bounds if block ends at the last pixel
                is_right_boundary_ok = (block_end_index == n - 1) or \
                                       (block_end_index + 1 < n and grid_1d[block_end_index + 1] == 0)

                if is_right_boundary_ok:
                    # All conditions met, found the unique pattern
                    return marker_color, marker_index, block_color, block_end_index

    # If loop finishes without returning, the specific pattern was not found
    return None, -1, None, -1


def transform(input_grid):
    """
    Transforms the input grid by swapping the marker pixel and the adjacent block.

    Args:
        input_grid (list or np.ndarray): A list of lists or numpy array representing the 1xN input grid.

    Returns:
        list or np.ndarray: The transformed grid in the same format as the input.
    """
    # Convert input to NumPy array for processing, ensure integer type
    if isinstance(input_grid, list):
        input_array = np.array(input_grid, dtype=int)
    elif isinstance(input_grid, np.ndarray):
        input_array = input_grid.astype(int) 
    else:
        raise TypeError("Input grid must be a list of lists or a NumPy array.")

    # Ensure the input is treated as 2D (e.g., 1xN)
    if input_array.ndim == 1:
         # Reshape 1D array like [0, 3, 1, 1, 0] to 2D [[0, 3, 1, 1, 0]]
         input_array = input_array.reshape(1, -1)
         
    # Verify shape is 1xN (or handle MxN if needed, though examples are 1xN)
    if input_array.shape[0] != 1:
         # For this specific task based on examples, we expect 1xN.
         # If other shapes were possible, logic would need adjustment.
         print(f"Warning: Expected input shape 1xN, but got {input_array.shape}. Processing first row only.")
         # Decide how to handle: proceed with row 0, return original, or raise error.
         # Proceeding with row 0 based on task structure.

    # Extract the first (and only relevant) row for processing
    grid_1d = input_array[0]

    # Find the marker and block details using the helper function
    marker_color, marker_index, block_color, block_end_index = find_marker_and_block_1d(grid_1d)

    # If the specific marker/block pattern wasn't found, return the original grid
    if marker_index == -1:
        # Return in the original format
        if isinstance(input_grid, list):
            return input_grid
        else:
            # Return original numpy array (potentially reshaped if input was 1D)
            return input_array 

    # Create a copy of the input array to modify for the output
    output_array = np.copy(input_array)

    # Calculate block properties
    block_start_index = marker_index + 1
    block_length = block_end_index - block_start_index + 1
    
    # Calculate the new index for the marker (position after original block end)
    new_marker_index = block_end_index + 1

    # Perform the swap transformation on the output array:
    # 1. Copy the block pixels to the marker's original starting position
    output_array[0, marker_index : marker_index + block_length] = block_color
    
    # 2. Place the marker pixel at the position after the block's original end position
    # Check bounds before placing the marker, although find_marker_and_block should ensure validity
    if new_marker_index < output_array.shape[1]:
        output_array[0, new_marker_index] = marker_color
    else:
        # This path indicates an issue, either in pattern finding or unexpected input structure.
        print(f"Warning: Calculated new marker position {new_marker_index} is out of bounds for grid width {output_array.shape[1]}. Returning original grid.")
        if isinstance(input_grid, list):
            return input_grid
        else:
            return input_array

    # Return the result in the same format as the input
    if isinstance(input_grid, list):
        # If original input was list of lists or 1D list reshaped internally
        return output_array.tolist()
    else:
        # If original input was numpy array
        return output_array
```