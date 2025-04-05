```python
import numpy as np
from collections import Counter

"""
Transforms the input grid according to two main steps:
1. Fill background cells (color 0): Iterate through each cell in the input grid. If a cell has color 0, examine its 8 neighbors (N, S, E, W, NE, NW, SE, SW) in the *original input grid*. Count the occurrences of each neighbor color, excluding colors 0 and 8. If any single color appears 3 or more times among these valid neighbors, change the cell's color in an intermediate grid to that majority color.
2. Remove noise color (color 8): Iterate through the intermediate grid resulting from step 1. Change any cell with color 8 to color 0. The final grid after this step is the output.
"""

def transform(input_grid):
    """
    Applies the fill and noise removal transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    intermediate_grid = np.copy(input_array) # Start intermediate grid as copy of input

    # Step 1: Fill background cells based on neighbors in the original input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell in the *input* is a background cell (0)
            if input_array[r, c] == 0:
                neighbor_colors = []
                # Iterate over the 8 potential neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        # Skip the cell itself
                        if dr == 0 and dc == 0:
                            continue
                        
                        nr, nc = r + dr, c + dc
                        
                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            neighbor_color = input_array[nr, nc]
                            # Consider only non-background (0) and non-noise (8) neighbors
                            if neighbor_color != 0 and neighbor_color != 8:
                                neighbor_colors.append(neighbor_color)

                # If there are any valid neighbors to consider
                if neighbor_colors:
                    # Count the frequency of each neighbor color
                    color_counts = Counter(neighbor_colors)
                    # Find the most common color and its count
                    most_common = color_counts.most_common(1)
                    if most_common:
                        majority_color, count = most_common[0]
                        # If the most common color appears 3 or more times
                        if count >= 3:
                            # Update the cell in the intermediate grid
                            intermediate_grid[r, c] = majority_color

    # Step 2: Remove noise color (8) from the intermediate grid
    output_grid = np.copy(intermediate_grid) # Start output grid from intermediate
    for r in range(height):
        for c in range(width):
            # If a cell in the intermediate grid is 8, set it to 0 in the output
            if intermediate_grid[r, c] == 8:
                output_grid[r, c] = 0
                
    # Convert back to list of lists for the required output format
    return output_grid.tolist()

```