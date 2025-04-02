import numpy as np

"""
Identifies pairs of adjacent pixels (horizontal or vertical) of the same non-background color in the input grid. 
Filters these pairs, keeping only those whose top-left coordinate (r, c) has both r and c as even numbers.
For each uniquely identified filtered pair location (r, c) and its associated color, draws a 2x2 square of that color onto the output grid, starting at (r, c).
The output grid is initialized with the background color (white, 0).
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on finding specific adjacent pairs 
    at even coordinates and replacing them with 2x2 squares.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_grid)

    # Set to store unique tuples (color, top_left_row, top_left_col) 
    # for the 2x2 squares to be drawn.
    squares_to_draw = set()

    # Iterate through each cell (r, c) of the input grid
    for r in range(height):
        for c in range(width):
            current_color = input_grid[r, c]

            # Skip background color
            if current_color == 0:
                continue

            # Check for horizontal pair (pixel to the right)
            if c + 1 < width and input_grid[r, c + 1] == current_color:
                # The top-left coordinate of this pair is (r, c)
                # Check if both row and column indices are even
                if r % 2 == 0 and c % 2 == 0:
                    squares_to_draw.add((current_color, r, c))

            # Check for vertical pair (pixel below)
            if r + 1 < height and input_grid[r + 1, c] == current_color:
                # The top-left coordinate of this pair is (r, c)
                # Check if both row and column indices are even
                if r % 2 == 0 and c % 2 == 0:
                    squares_to_draw.add((current_color, r, c))

    # Draw the identified 2x2 squares onto the output grid
    for color, r, c in squares_to_draw:
        # Double-check boundary conditions for the 2x2 square
        # (Although the loops above implicitly handle the start r, c, 
        # we ensure the square doesn't go out of bounds)
        if r + 1 < height and c + 1 < width:
            # Color the 2x2 block in the output grid
            output_grid[r:r+2, c:c+2] = color

    return output_grid
