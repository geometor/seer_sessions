```python
import numpy as np
from collections import Counter

"""
Transformation Rule:

1. Iterate through each non-background pixel (color != 0) in the input grid.
2. For each such pixel, examine its 8 adjacent neighbors (Moore neighborhood).
3. Filter these neighbors to include only those within the grid boundaries and whose color is not background (color != 0).
4. If there are no valid, non-background neighbors, the pixel's color remains unchanged.
5. If there are valid, non-background neighbors, count the frequency of each color among them.
6. Determine the color(s) that appear most frequently (majority color(s)).
7. If there is exactly one unique majority color and this majority color is different from the current pixel's color, change the pixel's color in the output grid to this majority color.
8. Otherwise (if the pixel is background, has no valid non-background neighbors, has multiple majority colors, or its color already matches the single majority color), the pixel's color in the output grid remains the same as in the input grid.
9. All changes are based on the state of the input grid; modifications to the output grid during the process do not affect subsequent neighbor calculations for other pixels.
"""

def get_valid_neighbors(grid, r, c):
    """
    Gets the colors of valid, non-background neighbors for a given cell.

    Args:
        grid (np.array): The input grid.
        r (int): Row index of the cell.
        c (int): Column index of the cell.

    Returns:
        list: A list of colors of valid, non-background neighbors.
    """
    height, width = grid.shape
    neighbor_colors = []
    # Define offsets for Moore neighborhood (8 neighbors)
    offsets = [(-1, -1), (-1, 0), (-1, 1),
               (0, -1),           (0, 1),
               (1, -1), (1, 0), (1, 1)]

    for dr, dc in offsets:
        nr, nc = r + dr, c + dc
        # Check if neighbor is within grid boundaries
        if 0 <= nr < height and 0 <= nc < width:
            neighbor_color = grid[nr, nc]
            # Check if neighbor is not background
            if neighbor_color != 0:
                neighbor_colors.append(neighbor_color)
    return neighbor_colors

def transform(input_grid):
    """
    Applies the cellular automaton-like transformation based on neighbor majority color.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # Iterate through each cell in the grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            pixel_color = input_np[r, c]

            # Skip background pixels
            if pixel_color == 0:
                continue

            # Get the colors of valid, non-background neighbors
            neighbor_colors = get_valid_neighbors(input_np, r, c)

            # If there are no valid neighbors, skip transformation for this pixel
            if not neighbor_colors:
                continue

            # Count the frequency of each neighbor color
            color_counts = Counter(neighbor_colors)
            
            # Find the maximum frequency
            max_count = 0
            if color_counts: # Ensure color_counts is not empty
                 max_count = max(color_counts.values())

            # Find all colors with the maximum frequency
            majority_colors = [color for color, count in color_counts.items() if count == max_count]

            # Apply the transformation rule
            # Change only if there is exactly one majority color AND it's different from the current pixel color
            if len(majority_colors) == 1:
                majority_color = majority_colors[0]
                if majority_color != pixel_color:
                    output_grid[r, c] = majority_color
            # Otherwise (tie or pixel already matches majority), the color remains unchanged (already copied)

    # Convert the result back to a list of lists
    return output_grid.tolist()
```