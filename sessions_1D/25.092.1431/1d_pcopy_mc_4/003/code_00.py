import numpy as np

"""
Transforms a 1xN grid by expanding isolated single colored pixels into blocks of three.

This function takes a 1xN NumPy array as input. It identifies any non-white pixel 
(color C > 0) at index `i` that is surrounded by white pixels (0) at indices `i-1` 
and `i+1`. For each such identified pixel, it changes the color of the adjacent 
white pixels at indices `i-1` and `i+1` in the output grid to the color C, 
effectively transforming the pattern '0 C 0' into 'C C C'. Pixels that are already 
part of a block of three or more identical colors, or are white pixels not 
adjacent to an isolated single colored pixel, remain unchanged.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the expansion transformation to the input grid.

    Args:
        input_grid (np.ndarray): A NumPy array of shape (1, N) representing the input grid.

    Returns:
        np.ndarray: The transformed grid, also a NumPy array of shape (1, N).
    """
    # Ensure input is a 2D numpy array with at least one row and one column
    if input_grid.ndim != 2 or input_grid.shape[0] == 0 or input_grid.shape[1] == 0:
        # Return an empty array or handle error as appropriate for the framework
        # Returning a copy might be safer if modification in place is undesirable
        return np.copy(input_grid) 

    # Initialize output_grid as a copy of the input grid
    # This ensures that pixels not involved in the transformation are preserved
    output_grid = np.copy(input_grid)
    
    # Get the dimensions (height should be 1, width is N)
    height, width = input_grid.shape
    
    # Iterate through the columns of the single row, checking for the '0 C 0' pattern
    # We only need to check indices from 1 to width-2, as the pattern requires neighbors
    for i in range(1, width - 1):
        # Get the color of the current pixel and its immediate horizontal neighbors from the *input* grid
        center_pixel_color = input_grid[0, i]
        left_pixel_color = input_grid[0, i-1]
        right_pixel_color = input_grid[0, i+1]
        
        # Check if the pattern matches: center is non-white ( > 0) and neighbors are white ( == 0)
        if center_pixel_color > 0 and left_pixel_color == 0 and right_pixel_color == 0:
            # If the pattern is found, modify the *output* grid
            # Change the left neighbor to the center pixel's color
            output_grid[0, i-1] = center_pixel_color
            # Change the right neighbor to the center pixel's color
            output_grid[0, i+1] = center_pixel_color
            # The center pixel output_grid[0, i] is already correct due to the initial copy

    # Return the modified grid
    return output_grid