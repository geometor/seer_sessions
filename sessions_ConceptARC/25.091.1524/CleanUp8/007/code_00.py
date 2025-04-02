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

    # Step 1: Initialize an empty output grid of the same dimensions as the input grid, filled with the background color (white, 0).
    output_grid = np.zeros_like(input_grid)

    # Set to store unique tuples (color, top_left_row, top_left_col) 
    # for the 2x2 squares to be drawn. This handles steps 2 & 3 implicitly.
    squares_to_draw = set()

    # Step 2 & 3: Iterate through each cell (r, c) of the input grid to find pairs and filter based on coordinates.
    for r in range(height):
        for c in range(width):
            current_color = input_grid[r, c]

            # Skip background color
            if current_color == 0:
                continue

            # Check for horizontal pair (pixel to the right)
            # If found, check if the top-left coord (r, c) is even-even
            if c + 1 < width and input_grid[r, c + 1] == current_color:
                if r % 2 == 0 and c % 2 == 0:
                    # Store the color and top-left coordinates
                    squares_to_draw.add((current_color, r, c))

            # Check for vertical pair (pixel below)
            # If found, check if the top-left coord (r, c) is even-even
            if r + 1 < height and input_grid[r + 1, c] == current_color:
                if r % 2 == 0 and c % 2 == 0:
                    # Store the color and top-left coordinates
                    # The set automatically handles duplicates if both H and V pairs exist for the same (r, c)
                    squares_to_draw.add((current_color, r, c))

    # Step 4: Draw the identified 2x2 squares onto the output grid.
    for color, r, c in squares_to_draw:
        # Check boundary conditions to ensure the 2x2 square fits
        if r + 1 < height and c + 1 < width:
            # Color the 2x2 block in the output grid
            output_grid[r:r+2, c:c+2] = color

    # Step 5: Return the final output grid.
    return output_grid