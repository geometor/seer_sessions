```python
import numpy as np
from collections import Counter

"""
Identify all non-white pixels in the input grid whose four cardinal neighbors (up, down, left, right) are also non-white and within the grid boundaries. These are considered "inner pixels". Collect the colors of all such inner pixels. The output is the single color digit that appears most frequently among these collected inner pixel colors.
"""

def transform(input_grid_list):
    """
    Finds the most frequent color among pixels whose four cardinal neighbors are also non-white.

    Args:
        input_grid_list (list): A list of lists representing the input grid.

    Returns:
        int: The most frequent inner color found in the grid. Returns 0 if none found.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape
    
    # List to store the colors of pixels that meet the "inner pixel" criteria
    inner_colors = []

    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            pixel_color = input_grid[r, c]

            # Rule 1: Pixel must not be white (background color 0)
            if pixel_color == 0:
                continue

            # Assume the pixel is an inner pixel initially
            is_inner = True
            
            # Define the four cardinal neighbors
            neighbors_deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

            # Check each neighbor
            for dr, dc in neighbors_deltas:
                nr, nc = r + dr, c + dc

                # Rule 2: Neighbor must be within grid boundaries
                if not (0 <= nr < rows and 0 <= nc < cols):
                    is_inner = False
                    break  # Stop checking neighbors for this pixel

                # Rule 3: Neighbor must not be white (background color 0)
                if input_grid[nr, nc] == 0:
                    is_inner = False
                    break  # Stop checking neighbors for this pixel

            # If all neighbors satisfied the conditions (is_inner is still True)
            if is_inner:
                inner_colors.append(pixel_color)

    # If no inner pixels were found, return 0 (based on previous failed attempts, although examples don't explicitly cover this)
    if not inner_colors:
        return 0

    # Count the frequency of each inner color
    counts = Counter(inner_colors)
    
    # Find the mode (most frequent color). 
    # Counter.most_common(1) returns a list like [(element, count)]
    # If there are ties, it returns one of the most common ones arbitrarily.
    most_common_color = counts.most_common(1)[0][0] 
    
    # Return the single integer representing the most frequent inner color
    return int(most_common_color) # Ensure return type is standard int
```