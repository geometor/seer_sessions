import numpy as np

def find_colored_block(grid):
    """
    Finds the contiguous block of color that is not white (0) or yellow (4).

    Args:
        grid (np.ndarray): The input grid (1D array).

    Returns:
        tuple: (color, start_index, end_index, length) or None if not found.
    """
    block_color = -1
    start_index = -1
    end_index = -1
    length = 0

    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 4:
            if start_index == -1:  # Start of a potential block
                block_color = pixel
                start_index = i
                length = 1
            elif pixel == block_color: # Continue the block
                length += 1
            else: # Different color, stop (shouldn't happen based on examples)
                end_index = i - 1
                return block_color, start_index, end_index, length
        elif start_index != -1: # End of the block
            end_index = i - 1
            return block_color, start_index, end_index, length

    # Handle case where block goes to the end of the grid
    if start_index != -1:
        end_index = len(grid) - 1
        return block_color, start_index, end_index, length

    return None # Should not happen in this task's examples


def find_marker(grid, marker_color=4):
    """
    Finds the index of the marker pixel.

    Args:
        grid (np.ndarray): The input grid (1D array).
        marker_color (int): The color of the marker to find (default is 4, yellow).

    Returns:
        int: The index of the marker, or -1 if not found.
    """
    for i, pixel in enumerate(grid):
        if pixel == marker_color:
            return i
    return -1


def transform(input_grid):
    """
    Shifts a colored block horizontally so its right edge is immediately
    to the left of a yellow marker pixel, maintaining the marker's position.
    The rest of the grid is filled with the background color (white, 0).
    Assumes input is a 1D numpy array (single row).
    """
    # Ensure input is a numpy array
    grid = np.array(input_grid)
    if grid.ndim == 2 and grid.shape[0] == 1: # Handle potential [[...]] format
        grid = grid[0]
    elif grid.ndim != 1:
        raise ValueError("Input grid must be 1-dimensional or 1xN")

    # Get grid dimensions
    grid_length = len(grid)

    # Initialize output_grid with background color (white, 0)
    output_grid = np.zeros(grid_length, dtype=int)

    # Find the colored block
    block_info = find_colored_block(grid)
    if block_info is None:
        # Handle cases where no block is found (though not expected in this task)
        # Maybe return input or an empty grid? For now, return the empty grid.
        print("Warning: Colored block not found.")
        # Copy marker if present
        marker_index = find_marker(grid)
        if marker_index != -1:
             output_grid[marker_index] = 4
        return output_grid.tolist() # Convert back to list for consistency if needed

    block_color, _, _, block_length = block_info

    # Find the yellow marker
    marker_index = find_marker(grid, 4)
    if marker_index == -1:
        # Handle cases where no marker is found (not expected)
        print("Warning: Yellow marker (4) not found.")
         # Place block at original position maybe? For now, return grid with just block.
        output_grid[block_info[1]:block_info[2]+1] = block_color
        return output_grid.tolist()

    # Calculate the target position for the block
    # The right edge of the block should be at marker_index - 1
    # The block has length `block_length`
    target_end_index = marker_index - 1
    target_start_index = target_end_index - block_length + 1

    # Check for boundary conditions (if the block would go out of bounds)
    if target_start_index < 0:
        print(f"Warning: Calculated block start index {target_start_index} is out of bounds.")
        # Decide on behavior - truncate? error? Place as much as possible?
        # For now, let's place what fits, starting from index 0
        actual_start = 0
        actual_length = target_end_index + 1
        output_grid[actual_start : actual_start + actual_length] = block_color

    elif target_end_index >= grid_length:
         print(f"Warning: Calculated block end index {target_end_index} is out of bounds.")
         # This case seems less likely given the logic, but handle defensively
         # Place block up to the edge?
         actual_end = grid_length - 1
         actual_length = block_length
         actual_start = actual_end - actual_length + 1
         if actual_start < 0: actual_start = 0 # prevent negative start
         output_grid[actual_start : actual_end + 1] = block_color

    else:
        # Place the colored block in the output grid at the target position
        output_grid[target_start_index : target_end_index + 1] = block_color

    # Place the yellow marker in the output grid at its original position
    output_grid[marker_index] = 4

    # Return the modified grid as a list
    return output_grid.tolist()
