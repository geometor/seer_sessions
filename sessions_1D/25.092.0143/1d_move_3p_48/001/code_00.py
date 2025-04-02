import numpy as np

def transform(input_grid):
    """
    Identifies a single contiguous block of non-white pixels in a 1D input grid
    (represented as a list or numpy array, potentially shaped as 1xN or Nx1)
    and shifts this block 3 positions to the right in the output grid.
    The space previously occupied by the block becomes white (0).
    The output grid has the same dimensions as the input grid.
    """

    # Ensure input is a numpy array
    input_np = np.array(input_grid, dtype=int)

    # Store original shape if > 1D but effectively 1D (like 1xN or Nx1)
    original_shape = None
    if input_np.ndim > 1:
        # Check if it's a single row or single column
        if input_np.shape[0] == 1 or input_np.shape[1] == 1:
            original_shape = input_np.shape
            # Flatten to 1D for processing
            input_1d = input_np.flatten()
        else:
            # Raise error if input is genuinely 2D with multiple rows/columns
            raise ValueError("Input grid must be 1-dimensional or effectively 1-dimensional (e.g., shape 1xN or Nx1).")
    else:
        # Input is already 1D
        input_1d = input_np

    grid_size = input_1d.shape[0]

    # --- Find the non-white block ---
    start_index = -1
    end_index = -1
    # Iterate to find the first non-white pixel (start of the block)
    for i, pixel in enumerate(input_1d):
        if pixel != 0:
            start_index = i
            break

    # --- Initialize output grid ---
    # Create a new grid filled with the background color (white=0)
    output_grid_1d = np.zeros(grid_size, dtype=int)

    # --- Shift and place the block if found ---
    if start_index != -1:
        # Find the end index of the block (last contiguous non-white pixel)
        end_index = start_index
        for i in range(start_index + 1, grid_size):
            # Check if the pixel belongs to the same block (non-white)
            # Assuming the block is contiguous and of a single color is not strictly necessary here,
            # only that it's a contiguous sequence of non-white pixels.
            if input_1d[i] != 0:
                end_index = i
            else:
                # Found the first white pixel after the block started
                break # End of block

        # Extract the block slice from the input
        block = input_1d[start_index : end_index + 1]
        block_length = len(block)

        # Calculate the new starting position for the block (shift right by 3)
        new_start_index = start_index + 3

        # --- Place the block in the output grid ---
        # Determine the actual end position in the output grid
        new_end_index = new_start_index + block_length

        # Check if the shifted block fits entirely within the grid boundaries
        if new_end_index <= grid_size:
            # Place the entire block
            output_grid_1d[new_start_index : new_end_index] = block
        else:
            # Handle cases where the block goes partially out of bounds
            # Calculate how many pixels of the block can fit
            placeable_length = grid_size - new_start_index
            if placeable_length > 0:
                # Place the part of the block that fits
                output_grid_1d[new_start_index : grid_size] = block[:placeable_length]
            # Pixels shifted beyond the grid boundary are lost


    # --- Format Output ---
    # Reshape the output to match the original input shape if it was 1xN or Nx1
    if original_shape:
        output_grid = output_grid_1d.reshape(original_shape)
    else:
        # Output remains 1D
        output_grid = output_grid_1d

    return output_grid