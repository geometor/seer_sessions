"""
Transforms an input grid based on a single unique pixel identified within it.
The transformation rule involves calculating the Manhattan distance from each
cell to the unique pixel, using this distance along with the unique pixel's
value to determine an index into a fixed base sequence, and assigning the
value from the sequence to the output cell.

1.  Identify Unique Pixel: Scan the input grid to find the single pixel
    differing from the background color. Record its row `r0`, column `c0`,
    and color `v0`.
2.  Define Base Sequence: Establish the constant base sequence of 9 values:
    `BaseSeq = [3, 4, 0, 5, 2, 8, 9, 6, 1]`.
3.  Calculate Shift: Compute a shift value `Shift = (6 * v0) % 9`.
4.  Initialize Output Grid: Create a new grid with the same dimensions as
    the input grid.
5.  Calculate Output Pixel Values: Iterate through each cell `(r, c)` of the
    output grid.
6.  Determine Pixel Color: For the current cell `(r, c)`:
    a.  Calculate the Manhattan distance `d` from `(r, c)` to `(r0, c0)`.
    b.  Calculate the index into the base sequence: `Index = (d + Shift) % 9`.
    c.  Retrieve the color from the base sequence: `Color = BaseSeq[Index]`.
7.  Populate Output Grid: Assign the calculated `Color` to the cell `(r, c)`.
8.  Return Output Grid: Return the completed output grid.
"""

import collections
import math
from typing import List, Tuple

# Define the constant base sequence used for color lookup
BASE_SEQ = [3, 4, 0, 5, 2, 8, 9, 6, 1]

def find_unique_pixel(grid: List[List[int]]) -> Tuple[int, int, int]:
    """
    Finds the row, column, and value of the single unique pixel in the grid.

    Assumes the background color is the most frequent color and there is
    exactly one pixel with a different color.

    Args:
        grid: The input grid (list of lists of integers).

    Returns:
        A tuple containing (row, column, value) of the unique pixel.

    Raises:
        ValueError: If the grid is empty, no unique pixel is found, or more
                    than one unique pixel is found, or if color counting fails.
    """
    if not grid or not grid[0]:
        raise ValueError("Input grid cannot be empty")

    height = len(grid)
    width = len(grid[0])

    # Count color occurrences to find the background color
    counts = collections.Counter()
    for r in range(height):
        for c in range(width):
            counts[grid[r][c]] += 1

    if not counts:
         raise ValueError("Could not count colors in the grid.")

    # Determine background color (most frequent).
    background_color = counts.most_common(1)[0][0]
    if counts.most_common(1)[0][1] == height * width:
         # Handle uniform grid case - implies no unique pixel
         raise ValueError("Grid is uniform, no unique pixel found.")

    # Find the unique pixel (the one not matching the background)
    unique_pixel_info = None
    unique_count = 0
    for r in range(height):
        for c in range(width):
            pixel_value = grid[r][c]
            if pixel_value != background_color:
                if unique_count > 0:
                     # Found more than one pixel different from background
                     raise ValueError("More than one unique pixel found.")
                unique_pixel_info = (r, c, pixel_value)
                unique_count += 1

    # Check if exactly one unique pixel was found
    if unique_pixel_info is None:
         raise ValueError("No unique pixel found (different from background).")

    return unique_pixel_info


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # 1. Identify Unique Pixel
    try:
        r0, c0, v0 = find_unique_pixel(input_grid)
    except ValueError as e:
        # Handle cases where the input doesn't match assumptions
        print(f"Error processing input grid: {e}. Returning original grid.")
        # Depending on ARC contest rules, might need to return something else
        return input_grid

    height = len(input_grid)
    width = len(input_grid[0])

    # 2. Base Sequence is defined globally as BASE_SEQ

    # 3. Calculate Shift
    shift = (6 * v0) % 9

    # 4. Initialize Output Grid
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # 5. & 7. Calculate Output Pixel Values and Populate Output Grid
    for r in range(height):
        for c in range(width):
            # 6. Determine Pixel Color
            # 6a. Calculate Manhattan distance
            manhattan_distance = abs(r - r0) + abs(c - c0)

            # 6b. Calculate the index into the base sequence
            index = (manhattan_distance + shift) % 9

            # 6c. Retrieve the color from the base sequence
            output_value = BASE_SEQ[index]

            # Assign the calculated value to the output grid
            output_grid[r][c] = output_value

    # 8. Return Output Grid
    return output_grid