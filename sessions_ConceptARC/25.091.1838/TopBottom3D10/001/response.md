Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import Counter

"""
Transforms the input grid based on specific horizontal adjacency rules observed in the examples:
1. If a Blue(2) pixel is horizontally adjacent to a Green(3) pixel, the Blue pixel becomes Green.
2. If a White(0) pixel is horizontally adjacent to an Azure(8) pixel, the White pixel adopts the color of the most frequent non-White(0), non-Azure(8) pixel among its 8 neighbors. If there's no unique most frequent neighbor (e.g., empty, tie), the pixel remains White(0).
"""

def get_neighbors_colors(grid, r, c):
    """Gets the colors of the 8 neighbors (Moore neighborhood) of a cell (r, c)."""
    neighbors_colors = []
    height, width = grid.shape
    # Iterate through the 3x3 neighborhood centered at (r, c)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the center cell itself
            if dr == 0 and dc == 0:
                continue
            # Calculate neighbor coordinates
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                neighbors_colors.append(grid[nr, nc])
    return neighbors_colors

def find_most_frequent(colors):
    """
    Finds the most frequent element in a list of colors.
    Returns the color if there is a unique most frequent one.
    Returns None if the list is empty, or if there is a tie for the most frequent color.
    """
    if not colors:
        return None # Return None if the list is empty

    # Count occurrences of each color
    count = Counter(colors)

    # Find the maximum frequency
    max_freq = 0
    for color in count:
         if count[color] > max_freq:
            max_freq = count[color]

    # If max_freq is 0 (e.g., input was []), it means no colors were found
    if max_freq == 0:
         return None

    # Collect all colors that have the maximum frequency
    most_frequent_colors = [color for color, freq in count.items() if freq == max_freq]

    # Return the color only if it's uniquely the most frequent
    if len(most_frequent_colors) == 1:
        return most_frequent_colors[0]
    else:
        # Handle ties
        return None

def transform(input_grid):
    """
    Applies the transformation rules based on horizontal adjacency and neighborhood context.

    Args:
        input_grid (list of lists): The input grid representing colors as integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Create a copy to store the output, ensuring changes are based on the original input state
    output_grid_np = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # Iterate through each cell (pixel) in the grid
    for r in range(height):
        for c in range(width):
            current_color = input_grid_np[r, c]

            # Determine the colors of horizontal neighbors (if they exist)
            left_color = input_grid_np[r, c - 1] if c > 0 else None
            right_color = input_grid_np[r, c + 1] if c < width - 1 else None

            # --- Apply Transformation Rules ---
            # The rules are checked sequentially, assuming they are mutually exclusive based on the current_color.

            # Rule 1: Derived from Example 1
            # If the current pixel is Blue(2) and is horizontally adjacent to a Green(3) pixel,
            # change the corresponding pixel in the output grid to Green(3).
            if current_color == 2 and (left_color == 3 or right_color == 3):
                output_grid_np[r, c] = 3

            # Rule 2: Derived from Example 2
            # If the current pixel is White(0) (background) and is horizontally adjacent to an Azure(8) pixel,
            # attempt to change the corresponding pixel in the output grid based on neighborhood context.
            elif current_color == 0 and (left_color == 8 or right_color == 8):
                # Define the set of colors to exclude when determining the dominant neighbor color.
                # This includes the background color (0) itself and the 'influencing' color (8).
                exclude_colors = {0, 8}

                # Get the colors of all 8 neighbors from the *
---
