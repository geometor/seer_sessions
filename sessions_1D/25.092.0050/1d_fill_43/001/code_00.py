import numpy as np

def find_non_white_pixels(grid_1d):
    """Finds the color and indices of non-white pixels in a 1D grid."""
    non_white_color = -1
    indices = []
    for i, pixel in enumerate(grid_1d):
        if pixel != 0:
            if non_white_color == -1:
                non_white_color = pixel
            elif pixel != non_white_color:
                 # Optional: Handle case where there are multiple non-white colors if needed
                 # For this task, we assume only one non-white color exists based on examples
                 pass 
            indices.append(i)
    if not indices:
        return -1, None, None # No non-white pixels found
    
    first_index = min(indices)
    last_index = max(indices)
    
    return non_white_color, first_index, last_index

def transform(input_grid):
    """
    Identifies the first and last occurrences of a non-white color in a single-row input grid 
    and fills the segment between them (exclusive of the first, inclusive up to the last) 
    with that same non-white color.
    """
    # Convert input grid (potentially list of lists) to a 1D numpy array
    # Assuming input is always a single row like [[0, 0, 2, ...]]
    if isinstance(input_grid, list) and len(input_grid) == 1:
         grid_1d = np.array(input_grid[0], dtype=int)
    elif isinstance(input_grid, np.ndarray) and input_grid.shape[0] == 1:
         grid_1d = input_grid.flatten()
    else:
        # Handle other potential input formats or raise an error if unexpected
        # For simplicity, assuming it's always a single row based on examples.
        raise ValueError("Input grid format not supported or not 1D as expected.")

    # Initialize output_grid as a copy of the input
    output_grid_1d = grid_1d.copy()

    # 1. & 2. & 3. Identify the non-white color and find the first/last indices
    fill_color, first_idx, last_idx = find_non_white_pixels(grid_1d)

    # Check if exactly two markers were found (as per perception)
    # Although the logic works for more, the description implies two.
    if fill_color != -1 and first_idx is not None and last_idx is not None and first_idx != last_idx:
        # 4. & 5. Iterate between the first and last indices and fill
        # The range is from the cell *after* the first marker up to *before* the last marker.
        for i in range(first_idx + 1, last_idx):
            output_grid_1d[i] = fill_color

    # 6. Other cells remain unchanged (handled by copying initially)
    
    # 7. Return the result, ensuring it's in the original list-of-lists format
    # Reshape the 1D array back into a 2D array (1 row, N columns)
    output_grid = output_grid_1d.reshape(1, -1).tolist()

    return output_grid