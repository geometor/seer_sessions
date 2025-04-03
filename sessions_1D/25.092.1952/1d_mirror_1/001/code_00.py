import numpy as np
import collections

# COLOR_MAP = {
#     0: (238, 238, 238),  # white
#     1: (30, 147, 255),  # blue
#     2: (220, 50, 40),  # red
#     3: (79, 204, 48),  # green
#     4: (230, 200, 0),  # yellow
#     5: (85, 85, 85),  # gray
#     6: (229, 58, 163),  # magenta
#     7: (230, 120, 20),  # orange
#     8: (135, 216, 241),  # azure
#     9: (146, 18, 49),  # maroon
# }

def find_movable_block(grid_list):
    """
    Finds the first contiguous block of a single color that is not white (0)
    or maroon (9).

    Args:
        grid_list: A list of integers representing the grid row.

    Returns:
        A tuple (block_color, block_start_index, block_length) if found,
        otherwise raises ValueError.
    """
    block_color = -1
    block_start = -1
    block_length = 0
    n = len(grid_list)
    i = 0
    while i < n:
        pixel_color = grid_list[i]
        if pixel_color != 0 and pixel_color != 9:
            # Found the start of a potential block
            block_color = pixel_color
            block_start = i
            j = i
            # Find the end of the block
            while j < n and grid_list[j] == block_color:
                j += 1
            block_length = j - i
            # Return the first block found
            return block_color, block_start, block_length
        i += 1
    # If loop completes without finding a block
    raise ValueError("Movable block not found in input.")


def transform(input_grid):
    """
    Moves a contiguous block of a single color (not white 0 or maroon 9)
    from one side of the stationary maroon (9) pivot pixel to the other side,
    ensuring exactly one white (0) pixel separates the block and the pivot
    in the output. Assumes the input is a 1D list or represents a 1xN grid.
    """

    # Ensure input is treated as a 1D list
    if isinstance(input_grid, np.ndarray):
        # Handle numpy array input, expecting 1D or 1xN / Nx1
        if input_grid.ndim == 1:
            input_list = input_grid.tolist()
        elif input_grid.ndim == 2 and (input_grid.shape[0] == 1 or input_grid.shape[1] == 1):
             input_list = input_grid.flatten().tolist()
        else:
            raise ValueError("Input grid must be 1D or effectively 1D (1xN or Nx1)")
    elif isinstance(input_grid, list):
        # Basic check if it's a list of lists (potentially 2D)
        if input_grid and isinstance(input_grid[0], list):
             if len(input_grid) == 1: # Treat as 1xN
                 input_list = input_grid[0]
             elif all(len(row) == 1 for row in input_grid): # Treat as Nx1
                 input_list = [row[0] for row in input_grid]
             else:
                 raise ValueError("Input grid must be 1D or effectively 1D (1xN or Nx1)")
        else: # Assume it's already a 1D list
            input_list = input_grid
    else:
        raise TypeError("Input must be a list or a numpy array.")


    n = len(input_list)
    if n == 0:
        return [] # Handle empty input

    # Initialize output grid (list) with background color (white 0)
    output_list = [0] * n

    # --- Workflow ---

    # 1. Locate the pivot pixel (maroon 9)
    try:
        pivot_index = input_list.index(9)
    except ValueError:
        raise ValueError("Pivot pixel (9) not found in input.")

    # 2. Place the pivot pixel in the output list
    output_list[pivot_index] = 9

    # 3. Identify the movable block (color, start index, length) using helper
    block_color, block_start_index, block_length = find_movable_block(input_list)

    # 4. Determine if the block is currently left or right of the pivot
    is_left_of_pivot = block_start_index < pivot_index

    # 5. Calculate the new starting index for the block in the output list
    if is_left_of_pivot:
        # Block was left, move it to the right of the pivot
        # The new layout should be: ... Pivot | White(0) | Block_Start ...
        new_start_index = pivot_index + 2
    else:
        # Block was right, move it to the left of the pivot
        # The new layout should be: ... Block_End | White(0) | Pivot ...
        # The start index needs to be calculated from the pivot position backwards
        # Indices occupied by block: new_start_index to new_start_index + block_length - 1
        # Index before pivot: pivot_index - 1 (should be white)
        # Index of last block element: pivot_index - 2
        # Index of first block element: (pivot_index - 2) - (block_length - 1) = pivot_index - block_length - 1
        new_start_index = pivot_index - block_length - 1

    # 6. Check if the calculated new position is valid (within bounds)
    if new_start_index < 0 or (new_start_index + block_length) > n:
         # This might indicate an input where the move isn't possible with the required spacing
         raise ValueError(f"Calculated new block position ({new_start_index} to {new_start_index + block_length -1}) is out of bounds for length {n}.")

    # 7. Place the block in the output list at the new calculated position
    for k in range(block_length):
        current_output_index = new_start_index + k
        # Sanity check: Ensure we are not overwriting the pivot pixel.
        # This should only happen if block_length is too large or spacing is wrong.
        if current_output_index == pivot_index:
             raise ValueError("Block placement calculation conflicts with pivot position.")
        # Ensure we are only writing over background (0) pixels
        if output_list[current_output_index] != 0:
             raise ValueError(f"Attempting to overwrite non-background pixel at index {current_output_index} during block placement.")

        output_list[current_output_index] = block_color

    # Return the transformed list
    return output_list