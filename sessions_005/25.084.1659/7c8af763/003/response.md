```python
"""
Transforms the input grid by performing a flood fill operation within contiguous regions bounded by gray (5) pixels. 
The fill color for each distinct region is determined by the presence of marker pixels (red=2 or blue=1) within that region in the input grid.
Red (2) markers have higher priority than blue (1) markers.
If a region contains at least one red pixel, the entire region (excluding boundaries) is filled with red.
If a region contains no red pixels but contains at least one blue pixel, the entire region is filled with blue.
If a region contains neither red nor blue pixels (only white=0), it is filled with blue.
Gray (5) boundary pixels remain unchanged.
"""

import numpy as np
from collections import deque

def find_connected_regions(grid):
    """
    Identifies contiguous regions of non-gray pixels using Breadth-First Search (BFS).

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of lists, where each inner list contains the (row, col) coordinates
        of the pixels belonging to a single connected region of non-gray pixels.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []
    gray_color = 5

    for r in range(rows):
        for c in range(cols):
            # Start a BFS if the pixel is not gray and not yet visited
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

                        # Check bounds and if neighbor is valid for the region (not gray, not visited)
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != gray_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Add the completed region to the list of regions
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
    
    # Define marker colors and boundary color
    red_color = 2
    blue_color = 1
    gray_color = 5 # Although not explicitly used for filling, it defines boundaries

    # Find all connected regions of non-gray pixels
    regions = find_connected_regions(input_grid)

    # Process each identified region
    for region_coords in regions:
        region_contains_red = False
        region_contains_blue = False

        # Check for the presence of marker colors (red or blue) within the current region
        # using the original input_grid values.
        for r, c in region_coords:
            pixel_value = input_grid[r, c]
            if pixel_value == red_color:
                region_contains_red = True
                # Optimization: If red is found, no need to check for blue as red has priority.
                break 
            elif pixel_value == blue_color:
                region_contains_blue = True
                # Continue checking in case a red pixel appears later in the region list

        # Determine the fill color for this specific region based on marker priority
        if region_contains_red:
            fill_color = red_color
        elif region_contains_blue:
            fill_color = blue_color
        else:
            # If the region contains neither red nor blue (implicitly, only white=0),
            # the rule derived from examples is to fill with blue.
            fill_color = blue_color

        # Apply the determined fill color to all pixels within this region in the output grid.
        # Since region_coords only contains non-gray pixels, we don't need to check for gray here.
        for r, c in region_coords:
            output_grid[r, c] = fill_color

    return output_grid
```