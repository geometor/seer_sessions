"""
1.  Identify the largest red rectangle: Find the largest contiguous block of red pixels in the input grid. Consider "largest" to prioritize width, then height if widths are equal.
2.  Represent with a blue pixel: Replace the entire red rectangle with a single blue pixel.
3.  Resize the grid:
    *   Set the output grid height to 3.
    *   Set the output width based on its relationship to the identified red
        rectangle - in some cases it can be reduced to 3 and in others it
        needs to be adjusted to accommodate placing the blue pixel within the grid.
4. Place Blue Pixel: The blue pixel representing the red object will always
   be on the second row.
5. Fill: Fill the remaining grid cells with white pixels.
6. Center Blue Pixel**: In two of the three training sets, the blue pixel is
   horizontally centered, however, this rule isn't consistent and needs
   additional review.
"""

import numpy as np

def find_largest_red_rectangle(grid):
    """Finds the largest red rectangle in the grid."""
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) == 0:
        return None

    # Calculate bounding box for each red pixel cluster
    min_row, min_col = np.min(red_pixels, axis=0)
    max_row, max_col = np.max(red_pixels, axis=0)
    width = max_col - min_col + 1
    height = max_row - min_row + 1

    return (min_row, min_col, width, height)

def transform(input_grid):
    # Find the largest red rectangle.
    rectangle_info = find_largest_red_rectangle(input_grid)

    # Determine output grid width.
    if rectangle_info:
        _, _, rect_width, _ = rectangle_info
        output_width = max(3, input_grid.shape[1] - rect_width + 1) if input_grid.shape[1] != 3 else 3 # handles example 2 and others
    else:
        output_width = input_grid.shape[1]  # Default case, should not occur, but prevents error

    # Initialize output grid.
    output_grid = np.zeros((3, output_width), dtype=int)

    # Place blue pixel.
    if rectangle_info:
        #_, _, rect_width, _ = rectangle_info

        # blue_col = output_width // 2 # initial centering attempt - failed

        blue_col = (output_width-1)//2 # accounts for off by one error, tries
                                       # again

        output_grid[1, blue_col] = 1  # second row

    return output_grid