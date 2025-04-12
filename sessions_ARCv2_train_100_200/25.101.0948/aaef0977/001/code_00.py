"""
Transforms an input grid based on a single unique pixel.

1.  **Identify Unique Pixel**: Scan the input grid to find the pixel whose color
    is different from the majority background color. Record its row `r0`,
    column `c0`, and color `v0`.
2.  **Initialize Output Grid**: Create a new grid with the same height and
    width as the input grid.
3.  **Calculate Output Pixel Values**: Iterate through each cell `(r, c)` of the
    grid.
4.  **Determine Pixel Color**: For the current cell `(r, c)`, calculate its color
    based on the rule: `Output[r][c] = (|r - r0| + |c - c0| + v0) % 10`, where
    `|x|` denotes the absolute value (Manhattan distance calculation).
5.  **Populate Output Grid**: Assign the calculated color to the cell `(r, c)`
    in the output grid.
6.  **Return Output Grid**: Once all cells are calculated, return the completed
    output grid.
"""

import collections
import math

def find_unique_pixel(grid: list[list[int]]) -> tuple[int, int, int]:
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
                    than one unique pixel is found.
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
         # This case would only happen if the grid dimensions were non-zero
         # but the grid itself was somehow empty, which is unlikely with checks above.
         raise ValueError("Could not count colors in the grid.")

    # Determine background color (most frequent). Handles uniform grids implicitly.
    background_color = counts.most_common(1)[0][0]

    # Find the unique pixel (the one not matching the background)
    unique_pixel_info = None
    unique_count = 0
    for r in range(height):
        for c in range(width):
            pixel_value = grid[r][c]
            if pixel_value != background_color:
                # Check if we already found a unique pixel
                if unique_count > 0:
                     raise ValueError("More than one unique pixel found.")
                unique_pixel_info = (r, c, pixel_value)
                unique_count += 1

    # Check if a unique pixel was found
    if unique_pixel_info is None:
        # This happens if all pixels are the same (background) color.
        # The problem description implies a unique pixel always exists.
         raise ValueError("No unique pixel found.")

    return unique_pixel_info

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule derived from the examples.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # 1. Identify Unique Pixel
    # Find the location (r0, c0) and value (v0) of the pixel
    # that differs from the background.
    try:
        r0, c0, v0 = find_unique_pixel(input_grid)
    except ValueError as e:
        # Handle cases where the input doesn't match expectations
        print(f"Error processing input grid: {e}")
        # Depending on requirements, might return input grid, empty grid, or re-raise
        return [] # Or raise e

    height = len(input_grid)
    width = len(input_grid[0])

    # 2. Initialize Output Grid
    # Create a new grid of the same size, initialized with zeros or any placeholder.
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # 3. & 5. Calculate Output Pixel Values and Populate Output Grid
    # Iterate through each cell (r, c) of the grid.
    for r in range(height):
        for c in range(width):
            # 4. Determine Pixel Color
            # Calculate the Manhattan distance from the unique pixel (r0, c0)
            manhattan_distance = abs(r - r0) + abs(c - c0)
            # Apply the formula: (distance + unique_value) mod 10
            output_value = (manhattan_distance + v0) % 10
            # Assign the calculated value to the output grid
            output_grid[r][c] = output_value

    # 6. Return Output Grid
    return output_grid