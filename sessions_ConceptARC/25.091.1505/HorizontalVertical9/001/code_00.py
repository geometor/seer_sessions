import numpy as np

"""
Recolor non-background pixels based on the orientation of the line segment they belong to.
Vertical line segments are colored yellow (4).
Horizontal line segments are colored orange (7).
The background (white, 0) remains unchanged.
A pixel is considered part of a vertical segment if it has a neighbor of the same color immediately above or below it.
A pixel is considered part of a horizontal segment if it has a neighbor of the same color immediately to its left or right.
If a pixel could be considered part of both (e.g., at a corner), the vertical rule takes precedence.
"""

def transform(input_grid):
    """
    Transforms the input grid based on line orientation rules.

    Args:
        input_grid (list[list[int]]): The input 2D grid.

    Returns:
        list[list[int]]: The transformed 2D grid.
    """
    # Convert input to numpy array for easier handling
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Initialize output grid as a copy of the input
    # We will modify the colors of non-background pixels based on rules
    output_grid = grid.copy()

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            pixel_color = grid[r, c]

            # Skip background pixels
            if pixel_color == 0:
                continue

            # Check for vertical neighbors of the same color
            is_vertical = False
            # Check above (if not on the top row)
            if r > 0 and grid[r - 1, c] == pixel_color:
                is_vertical = True
            # Check below (if not on the bottom row)
            if r < height - 1 and grid[r + 1, c] == pixel_color:
                is_vertical = True

            if is_vertical:
                # If part of a vertical line, color it yellow (4)
                output_grid[r, c] = 4
            else:
                # If not part of a vertical line, check for horizontal neighbors
                is_horizontal = False
                # Check left (if not on the leftmost column)
                if c > 0 and grid[r, c - 1] == pixel_color:
                    is_horizontal = True
                # Check right (if not on the rightmost column)
                if c < width - 1 and grid[r, c + 1] == pixel_color:
                    is_horizontal = True
                
                if is_horizontal:
                    # If part of a horizontal line (and not vertical), color it orange (7)
                    output_grid[r, c] = 7
                # else:
                    # If it's an isolated pixel (no same-colored neighbors) 
                    # or part of a structure not covered (e.g., diagonal - though not in examples),
                    # it retains its original color from the copy.
                    # Based on examples, all non-zero pixels are part of vertical or horizontal lines.

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()