import numpy as np

"""
Fill the contiguous sequence of white pixels (0) located between the rightmost 
non-white pixel (source pixel) found to the left of a green pixel (3) and the 
green pixel itself, using the color of the source pixel. This operates on a 1xN grid.
"""

def find_green_pixel_column(grid):
    """
    Finds the column index of the first green pixel (3) in the first row of the grid.
    Assumes the grid has at least one row.

    Args:
        grid (np.array): The input grid (expected 1xN).

    Returns:
        int: The column index of the first green pixel (3), or -1 if none is found.
    """
    # Get the shape (rows, columns)
    if grid.ndim != 2 or grid.shape[0] == 0:
        return -1 # Not a valid grid format for this task
        
    rows, cols = grid.shape
    # Only consider the first row (index 0) as per the problem description
    first_row = grid[0, :]
    
    # Find indices where the value is 3 (Green) in the first row
    green_indices = np.where(first_row == 3)[0]
    
    # If any green pixels were found, return the index (column) of the first one
    if len(green_indices) > 0:
        return green_indices[0]
        
    # Otherwise, indicate that no green pixel was found
    return -1

def find_source_pixel_before_green(grid, green_col):
    """
    Finds the column index and color of the rightmost non-white (0) pixel
    located strictly to the left of the given green_col in the first row.
    Scans from right-to-left starting just before the green pixel.

    Args:
        grid (np.array): The input grid (expected 1xN).
        green_col (int): The column index of the green pixel in the first row.

    Returns:
        tuple[int, int]: A tuple containing (source_col, source_color).
                         Returns (-1, -1) if no non-white pixel is found
                         to the left of green_col in the first row.
    """
    source_col = -1
    source_color = -1
    
    # Check if grid is valid and green_col is valid
    if grid.ndim != 2 or grid.shape[0] == 0 or green_col <= 0:
        return source_col, source_color # Cannot search left if green is at col 0 or grid invalid

    # Scan from the column immediately left of the green pixel, moving leftwards (down to column 0)
    # Ensure the loop range is valid (doesn't go below 0)
    for i in range(green_col - 1, -1, -1):
        # Check if the pixel at the current index in the first row is not white (0)
        if grid[0, i] != 0:
            # Found the rightmost non-white pixel; record its column and color
            source_col = i
            source_color = grid[0, i]
            # Stop scanning as we found the target pixel
            break
            
    return source_col, source_color

def transform(input_grid):
    """
    Transforms the input grid row by finding a green pixel (3), locating the
    rightmost non-white pixel (source) to its left, and filling any white pixels (0)
    between the source pixel and the green pixel with the source pixel's color.

    Args:
        input_grid (np.array): A 1xN numpy array representing the input row.

    Returns:
        np.array: A 1xN numpy array representing the transformed output row.
                  Returns a copy of the input if conditions for transformation aren't met.
    """
    # Ensure input is a 2D numpy array, even if it's just 1xN
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
        # Handle unexpected input shape if necessary, or assume valid 1xN
        # For ARC, inputs are always 2D.
        # If it were 1D, we might reshape: input_grid = np.atleast_2d(input_grid)
        # But based on examples, expecting 1xN directly.
        # If input is somehow invalid (e.g., 0 rows), just return a copy
        return input_grid.copy()
        
    # Initialize output_grid as a copy of the input to avoid modifying the original
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape # Should be 1, N

    # 1. Find Green: Locate the column index of the first Green pixel (3) in the first row.
    green_col = find_green_pixel_column(output_grid)

    # If no green pixel is found, return the input row unchanged.
    if green_col == -1:
        return output_grid

    # 2. Find Source: Find the column index and color of the rightmost non-White (0) pixel
    #    to the left of the green pixel in the first row.
    source_col, source_color = find_source_pixel_before_green(output_grid, green_col)

    # If no source pixel is found before the green pixel, return the input row unchanged.
    if source_col == -1:
        return output_grid

    # 3. Check for Gap: Verify that there is at least one position (column) between
    #    the source pixel and the green pixel.
    if not (green_col > source_col + 1):
        # No gap exists (source and green are adjacent or source is not found/invalid position)
        return output_grid

    # 4. Fill Gap: Iterate through the column indices strictly between the source pixel
    #    and the green pixel.
    #    The range starts one column after the source pixel and ends one column
    #    before the green pixel (exclusive end).
    for i in range(source_col + 1, green_col):
        # 5. For each pixel in the gap (in the first row), if it's White (0), change its color
        #    in the output grid to the source color.
        if output_grid[0, i] == 0:
            output_grid[0, i] = source_color
        # Note: Based on examples, the gap is expected to be white.
        # If a non-white pixel exists in the gap, this code leaves it unchanged.

    # 6. Return the modified grid.
    return output_grid