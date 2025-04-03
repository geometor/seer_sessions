import numpy as np

"""
Recolor the longest contiguous horizontal block of blue (1) pixels to green (3).

1. Scan the input grid (treated as a 1D array) from left to right.
2. Identify all contiguous horizontal sequences (blocks) composed entirely of blue (1) pixels.
3. For each identified blue block, record its length and starting position.
4. Determine the maximum length found among all recorded blue blocks.
5. Find the first blue block (the one with the smallest starting position) that has this maximum length.
6. Create the output grid as a copy of the input grid.
7. In the output grid, change the color of all pixels belonging to the identified longest blue block from blue (1) to green (3).
8. Keep all other pixels unchanged.
"""

def find_contiguous_blocks(grid_1d, target_color):
    """
    Finds all contiguous blocks of a specific color in a 1D grid.

    Args:
        grid_1d: A 1D list or numpy array representing the grid row.
        target_color: The color value to search for blocks of.

    Returns:
        A list of tuples, where each tuple represents a block
        in the format (start_index, length). Returns an empty list
        if no blocks are found.
    """
    blocks = []
    current_block_start = -1
    current_block_length = 0

    for i, pixel in enumerate(grid_1d):
        if pixel == target_color:
            if current_block_length == 0:
                current_block_start = i
            current_block_length += 1
        else:
            if current_block_length > 0:
                blocks.append((current_block_start, current_block_length))
            current_block_start = -1
            current_block_length = 0

    # Check for a block ending at the last pixel
    if current_block_length > 0:
        blocks.append((current_block_start, current_block_length))

    return blocks

def transform(input_grid):
    """
    Transforms the input grid by recoloring the longest contiguous block
    of blue (1) pixels to green (3).
    Assumes the input_grid is effectively 1D (either 1xN or Nx1).
    """
    # Convert input to a numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)

    # Handle potentially 2D input by flattening if it's 1xN or Nx1
    if input_array.shape[0] == 1 or input_array.shape[1] == 1:
      grid_1d = input_array.flatten()
    else:
      # This function is designed for 1D grids based on examples.
      # If it's truly 2D with >1 row and >1 col, the logic might need adjustment.
      # For now, proceed assuming it behaves like 1D or raise an error.
      # Let's assume the examples dictate 1D behavior.
      # If shape[0] > 1 and shape[1] > 1, we should perhaps reconsider the problem description.
      # Given the examples are flat lists, flatten seems appropriate.
      grid_1d = input_array.flatten()


    # Initialize output_grid as a copy of the input
    # We'll work with the flattened version and reshape at the end
    output_grid_1d = grid_1d.copy()

    # Find all contiguous blocks of blue (1)
    blue_color = 1
    green_color = 3
    blue_blocks = find_contiguous_blocks(grid_1d, blue_color)

    # If no blue blocks are found, return the original grid
    if not blue_blocks:
        return input_grid # Return original format

    # Find the maximum length among the blocks
    max_length = 0
    for _, length in blue_blocks:
        if length > max_length:
            max_length = length

    # Find the first block with the maximum length
    target_block_start = -1
    target_block_length = -1
    for start, length in blue_blocks:
        if length == max_length:
            target_block_start = start
            target_block_length = length
            break # Found the first one (leftmost)

    # Recolor the target block in the output grid if one was found
    if target_block_start != -1:
        for i in range(target_block_start, target_block_start + target_block_length):
            # Ensure we only change pixels that were originally blue
            if output_grid_1d[i] == blue_color:
                output_grid_1d[i] = green_color

    # Reshape the 1D output array back to the original input shape
    output_grid = output_grid_1d.reshape(input_array.shape)

    # Convert back to list of lists if that's the required final format
    # Assuming input is list of lists, output should match
    if isinstance(input_grid, list):
        # Check if the inner elements are lists (2D) or just numbers (1D list)
        if input_array.ndim > 1 and input_array.shape[0] > 0 and isinstance(input_grid[0], list):
             output_grid = output_grid.tolist()
        elif input_array.ndim == 1 or input_array.shape[0] == 1 or input_array.shape[1] == 1:
             # Handle cases originally represented as [[...]] or just [...]
             if input_array.shape[0] == 1:
                 output_grid = [output_grid.flatten().tolist()] # Keep [[...]] format
             else: # Treat as simple list [...] format potentially? Let's stick to numpy shape
                 output_grid = output_grid.tolist() # Will produce list of lists for Nx1, flatten list for 1xN handled above


    # Let's ensure output matches input structure precisely if possible
    # If input was [[a, b, c]], output should be [[d, e, f]]
    # If input was [[a], [b], [c]], output should be [[d], [e], [f]]
    # The reshape handles this. Conversion to list needs care.

    # Final check based on input type
    if isinstance(input_grid, list):
        # If input was List[List[int]]
        if input_array.ndim == 2:
            return output_grid.tolist()
        # If input was List[int] (implicitly 1xN or Nx1?)
        # The examples look like List[int] representing 1xN
        else: # ndim == 1
            # If original input was list[list[int]] like [[1, 2, 3]], return that shape
            if input_array.shape[0] == 1 and len(input_grid) == 1 and isinstance(input_grid[0], list):
                 return [output_grid.flatten().tolist()]
            else: # Assume original was just list[int]
                 return output_grid.flatten().tolist()

    # If input was numpy array, return numpy array
    return output_grid
