import numpy as np

def find_contiguous_blocks(grid_row, target_color):
    """
    Identifies contiguous blocks of a specific color in a 1D grid row.

    Args:
        grid_row (list or np.array): The 1D input grid row.
        target_color (int): The color value to find blocks of.

    Returns:
        list: A list of tuples, where each tuple contains (start_index, length).
    """
    blocks = []
    n = len(grid_row)
    i = 0
    while i < n:
        if grid_row[i] == target_color:
            start_index = i
            length = 0
            # Find the end of the block
            while i < n and grid_row[i] == target_color:
                length += 1
                i += 1
            blocks.append((start_index, length))
        else:
            i += 1
    return blocks

def transform(input_grid):
    """
    Transforms a 1D grid by recoloring contiguous blocks of yellow (4) pixels
    based on their length:
    - Length 1 becomes maroon (9).
    - Length 2 becomes gray (5).
    - Length 3 becomes orange (7).
    White (0) pixels remain unchanged.

    Args:
        input_grid (list or np.array): A 1D list or numpy array representing the input grid row.

    Returns:
        list: A 1D list representing the transformed output grid row.
    """
    # Ensure input is a list for easier manipulation if it's numpy
    if isinstance(input_grid, np.ndarray):
        # Assuming it's a 1xN or Nx1 array, flatten it
        input_list = input_grid.flatten().tolist()
    else:
        input_list = list(input_grid) # Make a mutable copy

    # Initialize output_grid as a copy of the input
    output_list = list(input_list)

    # Define the color mapping based on block length
    length_to_color_map = {
        1: 9,  # maroon
        2: 5,  # gray
        3: 7   # orange
    }

    # Find all yellow blocks
    yellow_blocks = find_contiguous_blocks(input_list, 4) # 4 is yellow

    # Recolor the blocks in the output grid based on their length
    for start_index, length in yellow_blocks:
        # Determine the new color based on length
        new_color = length_to_color_map.get(length)

        # If the length is found in the map, recolor the block
        if new_color is not None:
            for i in range(start_index, start_index + length):
                output_list[i] = new_color
        # else: (optional) handle lengths not specified (e.g., leave as yellow or map to white)
        # In this case, the problem description only covers lengths 1, 2, 3.
        # If a block of yellow with another length exists, it will remain yellow
        # according to this implementation, as it was copied initially.
        # However, based on examples, only lengths 1, 2, 3 appear.

    return output_list