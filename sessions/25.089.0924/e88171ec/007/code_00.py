import numpy as np

"""
Transformation rule:
1. Find the largest contiguous square block composed entirely of white (0) pixels in the input grid.
2. If multiple squares of the largest size exist, select the one whose top-left corner has the smallest row index, breaking ties with the smallest column index.
3. Let the side length of this selected white square be N and its top-left corner be (r, c).
4. Calculate the side length of the azure square to be placed: azure_N = N - 1.
5. The top-left corner of the azure square is the same as the white square's: (azure_r, azure_c) = (r, c).
6. Create the output grid by copying the input grid.
7. If azure_N is greater than 0, fill the square region of size azure_N x azure_N starting at (azure_r, azure_c) in the output grid with azure (8) pixels.
"""

def _is_square_all_color(grid, r, c, size, color):
    """
    Checks if a square region starting at (r, c) with side length 'size' 
    in the grid is entirely composed of the specified 'color'.

    Args:
        grid (np.ndarray): The input grid.
        r (int): Top row index of the square.
        c (int): Left column index of the square.
        size (int): Side length of the square.
        color (int): The color value to check for.

    Returns:
        bool: True if the square region is entirely of the specified color, False otherwise.
    """
    rows, cols = grid.shape
    # Check if the square fits within the grid boundaries
    if r < 0 or c < 0 or r + size > rows or c + size > cols:
        return False
    # Extract the square region
    square_region = grid[r:r+size, c:c+size]
    # Check if all elements in the region match the target color
    return np.all(square_region == color)

def _find_largest_square_of_color(grid, color):
    """
    Finds the top-left corner (r, c) and side length (N) of the largest 
    contiguous square block composed entirely of the specified color. 
    If multiple squares of the largest size exist, it returns the one 
    encountered first when scanning rows then columns (top-most, then left-most).

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color value of the square to find.

    Returns:
        tuple: A tuple containing (size, r, c) of the largest square found. 
               Returns (0, -1, -1) if no square of the specified color is found.
    """
    rows, cols = grid.shape
    max_size = 0
    top_left_r = -1
    top_left_c = -1

    # Iterate through possible sizes from largest possible down to 1
    for size in range(min(rows, cols), 0, -1):
        # Iterate through all possible top-left corners (r, c) for this size
        # Scan row by row, then column by column to ensure top-left-most is found first
        for r in range(rows - size + 1):
            for c in range(cols - size + 1):
                # Check if a square of the current size and color exists at (r, c)
                if _is_square_all_color(grid, r, c, size, color):
                    # Found a square of this size. Since we iterate size downwards,
                    # and scan r/c upwards, this is the largest size and the
                    # top-left-most location for this size.
                    return size, r, c 
                    
    # If the loops complete without returning, no square of the specified color was found.
    return 0, -1, -1 # Indicate no square found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid: finds the largest white square,
    and fills an (N-1)x(N-1) azure square at the same top-left position.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy of the input grid to modify, which will become the output
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # Define the colors involved in the transformation
    white_color = 0
    azure_color = 8

    # Find the largest square composed entirely of white pixels (top-left-most if tie)
    n, r, c = _find_largest_square_of_color(input_np, white_color)

    # Proceed with transformation only if a white square was found (n > 0)
    if n > 0:
        # Calculate the size of the azure square (N-1)
        azure_n = n - 1

        # The top-left position of the azure square is the same as the white square
        azure_r = r
        azure_c = c

        # Ensure the azure square has a positive size (N > 1) before attempting to fill
        if azure_n > 0:
             # Double-check bounds to prevent errors, although the logic should 
             # ensure the azure square fits within the original white square area.
             if 0 <= azure_r < rows and 0 <= azure_c < cols and \
                azure_r + azure_n <= rows and azure_c + azure_n <= cols:
                # Fill the calculated region in the output grid with the azure color
                output_grid[azure_r : azure_r + azure_n, azure_c : azure_c + azure_n] = azure_color
             # else: Calculated azure square is out of bounds or invalid. This shouldn't happen.

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()