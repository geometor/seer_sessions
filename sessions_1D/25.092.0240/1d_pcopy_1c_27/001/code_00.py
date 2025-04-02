import numpy as np

"""
Identifies isolated non-white pixels in a 1D horizontal grid and expands them into a 3-pixel segment of the same color, centered at the original pixel's position. Segments that are already larger than one pixel remain unchanged. The background color is white (0).

1. Initialize the output grid as a copy of the input grid.
2. Iterate through each pixel of the input grid (assumed to be 1xN).
3. For each non-white pixel at index `j` with color `C`:
    a. Check its left neighbor (at `j-1`, if `j>0`) and right neighbor (at `j+1`, if `j < width-1`).
    b. If both existing neighbors are white (0), then the pixel at `j` is isolated.
    c. If the pixel is isolated:
        i. Determine the start index for the new 3-pixel segment: `start = max(0, j - 1)`.
        ii. Determine the end index (exclusive) for the new segment: `end = min(width, j + 2)`.
        iii. Set the pixels in the output grid from `start` to `end` (exclusive) to the color `C`.
4. Pixels that are part of segments larger than 1 or background pixels are effectively copied from the input to the output during initialization and are not modified further.
5. Return the modified output grid.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by expanding isolated pixels.

    Args:
        input_grid: A numpy array representing the input grid (assumed 1xN).

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Ensure input is treated as a 2D array (1 row)
    if input_grid.ndim == 1:
        input_grid = input_grid.reshape(1, -1)
        
    height, width = input_grid.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Iterate through each pixel in the single row
    for j in range(width):
        pixel_color = input_grid[0, j]

        # Check if the pixel is non-white
        if pixel_color != 0:
            # Check left neighbor (handle boundary)
            is_left_neighbor_white = (j == 0) or (input_grid[0, j - 1] == 0)
            
            # Check right neighbor (handle boundary)
            is_right_neighbor_white = (j == width - 1) or (input_grid[0, j + 1] == 0)

            # If both neighbors are white, it's an isolated pixel
            if is_left_neighbor_white and is_right_neighbor_white:
                # Calculate the start and end indices for the 3-pixel segment
                # Center the segment at j, expanding one pixel left and one right
                start_col = max(0, j - 1)
                end_col = min(width, j + 2) # slice uses exclusive end

                # Update the output grid with the 3-pixel segment
                output_grid[0, start_col:end_col] = pixel_color
                
    # If the original input was 1D, return a 1D array
    if input_grid.shape[0] == 1 and output_grid.shape[0] == 1 and input_grid.ndim == 1:
         return output_grid.flatten()
    # otherwise return the 2D shape. In this task context, inputs seem 1D in spirit
    # but might be represented as (1, N) or (N,). We'll return (1, N) for consistency with potential numpy loading.
    # Reconsidering: ARC examples usually maintain dimensionality. Let's return the same shape as input came in.
    # The check `if input_grid.ndim == 1:` at the start normalized to 2D. Let's just return the 2D version.
    # Final Decision: The examples are shown flat. Let's return flat if input was flat.
    # We need the original ndim. Let's store it.
    original_ndim = np.array(input_grid).ndim # get ndim before potential reshape
    if original_ndim == 1:
         # check if input_grid was reshaped
         if input_grid.shape[0] == 1 and output_grid.shape[0] == 1:
             return output_grid.flatten()
             
    return output_grid # Return as potentially reshaped 2D
