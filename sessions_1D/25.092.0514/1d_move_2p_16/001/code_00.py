import numpy as np

"""
Identifies a single contiguous block of non-white pixels in a 1D input grid and shifts this block two positions to the right. The original positions of the block become white, and the grid size remains unchanged.
"""

def find_contiguous_block(grid_1d):
    """
    Finds the start index, end index, and color of the first contiguous block
    of non-background pixels in a 1D grid. Assumes background is 0.

    Args:
        grid_1d (np.array): A 1D numpy array representing the grid row.

    Returns:
        tuple: (start_index, end_index, color) or (None, None, None) if no block found.
    """
    non_background_indices = np.where(grid_1d != 0)[0]
    if len(non_background_indices) == 0:
        return None, None, None

    start_index = non_background_indices[0]
    end_index = non_background_indices[-1]
    color = grid_1d[start_index] # Assumes block is one color

    # Verify contiguity (optional but good practice for more complex cases)
    if not np.all(grid_1d[start_index : end_index + 1] == color):
         # This basic check assumes the block is truly contiguous and one color.
         # More robust checks might be needed for complex patterns.
         # For this specific task, the examples suggest this simple check is sufficient.
         pass # Or raise an error if non-contiguous blocks are possible

    return start_index, end_index, color


def transform(input_grid):
    """
    Shifts a contiguous block of non-white pixels two positions to the right in a 1D grid.

    Args:
        input_grid (list): A list representing the 1D input grid.

    Returns:
        list: A list representing the 1D output grid with the block shifted.
    """
    # Convert input list to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    grid_size = len(input_array)

    # Find the contiguous block of non-background color
    start_idx, end_idx, block_color = find_contiguous_block(input_array)

    # Handle cases where no block is found (though not present in examples)
    if start_idx is None:
        return input_grid # Return original grid if no block found

    # Initialize the output grid with the background color (white=0)
    output_array = np.zeros_like(input_array)

    # Calculate the new starting position for the block
    new_start_idx = start_idx + 2
    block_length = end_idx - start_idx + 1
    new_end_idx = new_start_idx + block_length - 1

    # Check if the shifted block goes out of bounds (handle if necessary,
    # though not seen in examples - assuming it stays within grid)
    if new_end_idx >= grid_size:
        # Decide how to handle out-of-bounds: clip, wrap, error?
        # Based on examples, it seems the grid is large enough.
        # We'll proceed assuming it fits.
        pass

    # Extract the block from the input
    block = input_array[start_idx : end_idx + 1]

    # Place the block into the output grid at the new position
    # Ensure indices are within bounds before assignment
    if new_start_idx < grid_size:
        # Determine the actual length to copy if part of the block goes off the end
        copy_len = min(block_length, grid_size - new_start_idx)
        output_array[new_start_idx : new_start_idx + copy_len] = block[:copy_len]

    # Convert the numpy array back to a list for the return value
    return output_array.tolist()