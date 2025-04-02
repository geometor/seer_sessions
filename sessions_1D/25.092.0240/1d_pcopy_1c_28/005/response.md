```python
import numpy as np
import copy

"""
Transforms a grid based on the following rule:
1. Identify the single non-white (non-zero) color present ('active_color'). If none exists, return the input grid unchanged.
2. Create a copy of the input grid for the output.
3. Iterate through the input grid to find 'isolated' active color pixels. A pixel is isolated horizontally if both its immediate left and right neighbors are white (0), considering grid boundaries (a pixel at the edge only needs its single horizontal neighbor to be white).
4. For each isolated active pixel identified in the *input* grid:
    a. If its left neighbor exists and is white in the input grid, change the color of that neighbor in the *output* grid to the active_color.
    b. If its right neighbor exists and is white in the input grid, change the color of that neighbor in the *output* grid to the active_color.
5. Return the modified output grid.
"""

def find_active_color(grid: np.ndarray) -> int:
    """
    Finds the unique non-zero color in the grid.
    Returns the color value or 0 if none is found or multiple non-zero colors exist (though examples suggest only one).
    """
    unique_colors = np.unique(grid)
    active_color = 0
    non_zero_count = 0
    for color in unique_colors:
        if color != 0:
            # In case of multiple non-zero colors, based on ARC structure,
            # it's usually safe to assume the 'most prominent' or just one matters.
            # Here, we'll just take the first one encountered that isn't zero.
            if non_zero_count == 0:
                active_color = int(color) # Ensure it's a standard int
            non_zero_count += 1

    # The rule implies a single active color. If 0 or >1 non-zero colors found,
    # return 0 to indicate the rule might not apply or the grid is all white.
    if non_zero_count != 1:
         if np.all(grid == 0):
             return 0 # All white, no active color
         else:
             # If multiple non-zeros exist, the examples don't cover this.
             # Returning the first found non-zero is a guess based on simplicity.
             # If the logic strictly requires ONE active color, we could return 0 here too.
             # Let's stick to returning the first found for now.
             for color in unique_colors:
                 if color != 0:
                     return int(color)
             return 0 # Should not be reached if unique_colors had non-zeros

    return active_color


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Find the active color
    active_color = find_active_color(input_grid)

    # If no single active color identified (e.g., all white), return a copy
    if active_color == 0:
        return copy.deepcopy(input_grid)

    # Get grid dimensions
    rows, cols = input_grid.shape

    # Initialize output_grid as a copy of the input
    output_grid = copy.deepcopy(input_grid)

    # Use a set to store coordinates of white neighbors to color (avoids duplicates if neighbours overlap)
    pixels_to_color = set()

    # Iterate through the input grid to find ISOLATED active pixels
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel has the active color
            if input_grid[r, c] == active_color:
                # Check if the pixel is isolated horizontally
                is_left_isolated = (c == 0) or (input_grid[r, c - 1] == 0)
                is_right_isolated = (c == cols - 1) or (input_grid[r, c + 1] == 0)

                # If the pixel is isolated
                if is_left_isolated and is_right_isolated:
                    # Mark the left neighbor for coloring if it exists and is white
                    if c > 0 and input_grid[r, c - 1] == 0:
                        pixels_to_color.add((r, c - 1))

                    # Mark the right neighbor for coloring if it exists and is white
                    if c < cols - 1 and input_grid[r, c + 1] == 0:
                        pixels_to_color.add((r, c + 1))

    # Apply the color changes to the output grid
    for r_change, c_change in pixels_to_color:
        output_grid[r_change, c_change] = active_color

    return output_grid
```