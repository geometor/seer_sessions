import numpy as np

"""
Transformation rule:
1. Find the largest contiguous square block composed entirely of white (0) pixels in the input grid.
2. Let the side length of this largest white square be N and its top-left corner be (r, c).
3. Determine the side length of the azure square to be placed: azure_N = N - 1.
4. Determine the top-left corner (azure_r, azure_c) for the azure square:
   - If N is odd, azure_r = r + 1 and azure_c = c.
   - If N is even, azure_r = r and azure_c = c.
5. Create the output grid by copying the input grid.
6. If azure_N is greater than 0, fill the square region of size azure_N x azure_N starting at (azure_r, azure_c) in the output grid with azure (8) pixels.
"""

def _is_square_all_color(grid, r, c, size, color):
    """Checks if a square region in the grid is entirely of a specific color."""
    rows, cols = grid.shape
    if r + size > rows or c + size > cols:
        return False  # Square goes out of bounds
    square_region = grid[r:r+size, c:c+size]
    return np.all(square_region == color)

def _find_largest_square_of_color(grid, color):
    """Finds the largest square block of a specified color."""
    rows, cols = grid.shape
    max_size = 0
    top_left = None

    # Iterate through possible sizes from largest possible down to 1
    for size in range(min(rows, cols), 0, -1):
        # Iterate through all possible top-left corners for this size
        for r in range(rows - size + 1):
            for c in range(cols - size + 1):
                if _is_square_all_color(grid, r, c, size, color):
                    # Found a square of this size, since we iterate largest first, this is the largest
                    return size, r, c
        # If we found a square of size > 0 in the inner loops, we would have returned.
        # If we reach here, no square of 'size' was found, continue to smaller sizes.
    
    # If no square of any size > 0 is found
    return 0, -1, -1 # Indicate no square found

def transform(input_grid):
    """
    Finds the largest white square in the input grid and fills a slightly
    smaller azure square within it, adjusting position based on the white
    square's size parity.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # Find the largest square of white (0) pixels
    white_color = 0
    azure_color = 8
    
    n, r, c = _find_largest_square_of_color(input_np, white_color)

    # If a white square was found (n > 0)
    if n > 0:
        # Calculate properties for the azure square
        azure_n = n - 1
        
        # Determine placement based on parity of n
        if n % 2 != 0:  # N is odd
            azure_r = r + 1
            azure_c = c
        else:  # N is even
            azure_r = r
            azure_c = c

        # Ensure the azure square has a positive size and fits within the grid
        if azure_n > 0:
             # Check bounds just in case (though placement logic should keep it within original white square)
             if azure_r + azure_n <= rows and azure_c + azure_n <= cols:
                # Fill the azure square in the output grid
                output_grid[azure_r : azure_r + azure_n, azure_c : azure_c + azure_n] = azure_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()