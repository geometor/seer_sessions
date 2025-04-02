import numpy as np

"""
1. Identify the contiguous block of non-white pixels (color != 0) in the input row.
2. Note the color, starting index, and length of this block.
3. Create a new output row of the same size as the input, initially filled with white pixels (color 0).
4. Calculate the new starting index for the block by adding 3 to its original starting index.
5. Place the identified block (using its original color and length) into the output row at the new starting index.
"""

def find_object_block(grid_row):
    """
    Finds the first contiguous block of non-white pixels in a 1D array.

    Args:
        grid_row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (color, start_index, length) of the block,
               or (None, -1, 0) if no non-white block is found.
    """
    non_white_indices = np.where(grid_row != 0)[0]
    if len(non_white_indices) == 0:
        return None, -1, 0  # No non-white pixels found

    start_index = non_white_indices[0]
    color = grid_row[start_index]

    # Find the end of the contiguous block of the same color
    length = 0
    for i in range(start_index, len(grid_row)):
        if grid_row[i] == color:
            length += 1
        else:
            break # End of block

    # Sanity check: ensure all found non_white_indices belong to this single block
    # This assumes only one object per row as per observation
    if len(non_white_indices) != length or not np.all(grid_row[start_index:start_index+length] == color):
         # This case shouldn't happen based on examples, but good to consider
         # For simplicity, we'll stick to the first block found.
         # More robust code might handle multiple blocks or fragmented objects if needed.
         pass


    return color, start_index, length

def transform(input_grid):
    """
    Transforms the input grid by shifting the single non-white block 3 positions to the right.

    Args:
        input_grid (np.array): A 1D numpy array representing the input row.

    Returns:
        np.array: A 1D numpy array representing the transformed output row.
    """
    # Ensure input is treated as a 1D array (relevant if input is 1xN 2D array)
    if input_grid.ndim > 1:
      if input_grid.shape[0] == 1:
          input_row = input_grid[0]
      else:
          # Handle unexpected input dimensions if necessary
          # For this task, we assume a single row input
          raise ValueError("Input grid has more than one row")
    else:
        input_row = input_grid

    # Find the non-white object block
    color, start_index, length = find_object_block(input_row)

    # Initialize the output grid with the background color (white/0)
    output_grid = np.zeros_like(input_row)

    # If a non-white block was found, shift it
    if color is not None:
        # Calculate the new starting position
        new_start_index = start_index + 3
        new_end_index = new_start_index + length # Exclusive index for slicing

        # Place the block in the output grid at the new position
        # Ensure indices are within bounds (though numpy slicing handles the end boundary)
        if new_start_index < len(output_grid):
            # Calculate the actual end index considering grid boundaries
            actual_end_index = min(new_end_index, len(output_grid))
            # Calculate how much of the block fits
            actual_length = actual_end_index - new_start_index
            # Fill the corresponding slice in the output grid
            output_grid[new_start_index:actual_end_index] = color

    # If input was 2D (1xN), return 2D output
    if input_grid.ndim > 1:
        return output_grid.reshape(1, -1)
    else:
        return output_grid