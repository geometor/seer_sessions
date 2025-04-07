```python
"""
Fill horizontally between marker pixels on each row with red (2).

1. Identify the background color (azure, 8).
2. Identify the "marker color" by finding the pixel color in the input grid that is not the background color.
3. Create a copy of the input grid to serve as the output grid.
4. Iterate through each row of the input grid.
5. For the current row, find the column indices of all pixels that match the marker color.
6. If there are two or more marker pixels found in the current row:
    a. Sort the identified column indices in ascending order.
    b. Iterate through the sorted list of column indices, considering pairs of adjacent indices (col1, col2).
    c. For each adjacent pair, change the color of the pixels in the current row of the output grid from column col1 + 1 up to (but not including) column col2 to red (2).
7. Return the modified grid copy.
"""

import numpy as np

BACKGROUND_COLOR = 8
FILL_COLOR = 2

def find_marker_color(grid):
    """Finds the first color in the grid that is not the background color."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != BACKGROUND_COLOR:
            return color
    # Should not happen based on task description, but handle defensively
    return None 

def transform(input_grid):
    """
    Fills the horizontal space between consecutive marker pixels in each row with red.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy() # Initialize output_grid as a copy

    # Identify the marker color (assuming one non-background color)
    marker_color = find_marker_color(grid)
    if marker_color is None:
        # If no marker color found (e.g., grid is all background), return the copy
        return output_grid.tolist() 

    # Get grid dimensions
    height, width = grid.shape

    # Process each row independently
    for r in range(height):
        # Find the column indices of marker pixels in the current row
        marker_indices = np.where(grid[r, :] == marker_color)[0]

        # Sort indices (np.where usually returns sorted, but explicit sort is safer)
        marker_indices.sort()

        # If there are at least two marker pixels in the row
        if len(marker_indices) >= 2:
            # Iterate through adjacent pairs of marker indices
            for i in range(len(marker_indices) - 1):
                col1 = marker_indices[i]
                col2 = marker_indices[i+1]

                # Fill the segment between col1 and col2 (exclusive) with red
                if col1 + 1 < col2: # Check if there's space between them
                    output_grid[r, col1 + 1 : col2] = FILL_COLOR

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```