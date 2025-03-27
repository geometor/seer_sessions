import numpy as np

"""
Transformation Rule:

1.  Check the entire input grid for any instance of two red pixels (value 2) being horizontally adjacent in the same row.
2.  If any such horizontally adjacent red pixels exist anywhere in the grid, the transformation does nothing, and the output grid is identical to the input grid.
3.  If no horizontally adjacent red pixels are found, proceed to process each row independently.
4.  For each row:
    a.  Find all red pixels in the row.
    b.  If a row contains exactly two red pixels:
        i.  Identify the segment of pixels strictly *between* these two red pixels.
        ii. Check if all pixels within this segment are white (value 0).
        iii.If all pixels in the segment are white, change the color of these pixels in the segment to red (value 2) in the output grid.
    c.  If a row does not contain exactly two red pixels, or if the segment between the two red pixels contains non-white pixels, the row remains unchanged.
5.  The final modified grid is the output.
"""

def has_adjacent_reds(grid):
    """Checks if any row in the grid contains adjacent red pixels."""
    height, width = grid.shape
    for r in range(height):
        for c in range(width - 1):
            if grid[r, c] == 2 and grid[r, c + 1] == 2:
                return True
    return False

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    Fills horizontal segments between pairs of red pixels in a row with red,
    only if all pixels in the segment are white and there are no horizontally
    adjacent red pixels anywhere in the input grid.
    """
    # Check for the global inhibiting condition: adjacent red pixels
    if has_adjacent_reds(input_grid):
        # If inhibitor found, return the input grid unchanged
        return input_grid.copy()

    # Initialize output_grid as a copy of the input
    output_grid = input_grid.copy()
    height, width = output_grid.shape

    # Process each row if no inhibitor was found
    for r in range(height):
        row = output_grid[r, :]
        # Find indices of red pixels in the current row
        red_indices = np.where(row == 2)[0]

        # Check if the row contains exactly two red pixels
        if len(red_indices) == 2:
            c1, c2 = red_indices[0], red_indices[1]
            # Ensure c1 < c2 (should be guaranteed by np.where)

            # Check if the segment between c1 and c2 is non-empty
            if c1 + 1 < c2:
                 # Extract the segment between the two red pixels
                segment = row[c1 + 1 : c2]

                # Check if all pixels in the segment are white (0)
                if np.all(segment == 0):
                    # If all white, fill the segment in the output grid with red (2)
                    output_grid[r, c1 + 1 : c2] = 2

    return output_grid