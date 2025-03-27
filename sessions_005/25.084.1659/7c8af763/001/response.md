```python
"""
Transforms the input grid by performing a flood fill operation within regions defined by gray (5) boundaries.
The fill color for each region is determined by the highest priority marker pixel (red=2 > blue=1) present within that region in the input grid.
All non-gray pixels within a region are replaced by the determined fill color.
Gray (5) boundary pixels remain unchanged.
"""

import numpy as np
from collections import deque

def find_connected_regions(grid):
    """
    Identifies contiguous regions of non-gray pixels.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of lists, where each inner list contains the (row, col) coordinates
        of the pixels belonging to a single connected region.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []
    gray_color = 5

    for r in range(rows):
        for c in range(cols):
            # Start a search if the pixel is not gray and not yet visited
            if grid[r, c] != gray_color and not visited[r, c]:
                current_region = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_region.append((row, col))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds and if neighbor is valid for the region
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != gray_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if current_region:
                    regions.append(current_region)
    return regions

def transform(input_grid):
    """
    Applies the flood fill transformation based on marker priorities within regions.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Define marker colors and priorities
    red_color = 2
    blue_color = 1
    gray_color = 5

    # Find all connected regions of non-gray pixels
    regions = find_connected_regions(input_grid)

    # Process each region
    for region_coords in regions:
        contains_red = False
        contains_blue = False # Though not strictly needed due to red's priority

        # Check for marker colors within the region in the original input_grid
        for r, c in region_coords:
            if input_grid[r, c] == red_color:
                contains_red = True
                break # Red has highest priority, no need to check further
        
        # Determine the fill color based on marker presence
        if contains_red:
            fill_color = red_color
        else:
            # If no red, check if there was any blue marker (or even just white)
            # The rule implies fill blue if only blue markers are present.
            # If only white (0) were present, the examples suggest filling with blue (1).
            # Let's confirm by checking if any blue marker exists, otherwise default to blue if no red.
             fill_color = blue_color # Default to blue if no red is found
             # Optional check if explicit blue marker presence is required:
             # for r, c in region_coords:
             #    if input_grid[r,c] == blue_color:
             #        contains_blue = True
             #        break
             # if contains_blue:
             #    fill_color = blue_color
             # else:
             #     # Handle case where region only contains 0s? Examples suggest blue fill.
             #     fill_color = blue_color


        # Apply the fill color to all pixels in the region in the output grid
        for r, c in region_coords:
            # Ensure we don't accidentally overwrite a gray pixel if logic flawed
            if output_grid[r, c] != gray_color: 
                 output_grid[r, c] = fill_color

    return output_grid
```