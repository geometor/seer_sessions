"""
Transforms the input grid based on two rules applied sequentially:

1.  Identify contiguous white (0) regions completely enclosed by a border of only gray (5) pixels (using 8-connectivity for border definition). Fill these enclosed white regions with a specific color based on their area:
    - Area 1: Fill with magenta (6)
    - Area 4: Fill with orange (7)
    - Area 6: Fill with orange (7)
    - Area 9: Fill with azure (8)
    Keep track of the gray border pixels associated with these filled regions.

2.  Identify gray (5) pixels in the original input grid that meet two conditions:
    a. They do not have any adjacent (up, down, left, right) white (0) neighbors in the input grid.
    b. They were *not* part of the gray border of a region that was filled in Rule 1.
    Change the color of these specific gray pixels to magenta (6) in the output grid.
"""

import numpy as np
from collections import deque

def _get_neighbors(r, c, height, width, connectivity=4):
    """Gets valid neighbor coordinates for a pixel."""
    neighbors = []
    if connectivity == 4:
        # Cardinal directions (up, down, left, right)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elif connectivity == 8:
        # Cardinal and diagonal directions
        directions = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else:
        raise ValueError("Connectivity must be 4 or 8")

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def _find_regions(grid, target_color, connectivity=4):
    """Finds all contiguous regions of a specified color using BFS."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color and not visited[r, c]:
                region_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                region_pixels.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    # Use specified connectivity for region finding
                    for nr, nc in _get_neighbors(curr_r, curr_c, height, width, connectivity=connectivity):
                        if grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            region_pixels.add((nr, nc))
                            q.append((nr, nc))
                if region_pixels:
                    regions.append(region_pixels)
    return regions

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Set to store coordinates of gray pixels that form the border of filled regions
    filled_region_borders = set()

    # --- Rule 1: Find and fill enclosed white regions ---

    # Define the area-to-color mapping for Rule 1
    area_color_map = {
        1: 6,  # magenta
        4: 7,  # orange
        6: 7,  # orange
        9: 8,  # azure
    }

    # Find all white regions using 4-connectivity (regions are defined by cardinal adjacency)
    white_regions = _find_regions(input_np, 0, connectivity=4)

    for region in white_regions:
        potential_border_pixels = set()
        is_enclosed_by_gray = True

        # Check the border using 8-connectivity
        for r, c in region:
            for nr, nc in _get_neighbors(r, c, height, width, connectivity=8):
                if (nr, nc) not in region: # Pixel is outside the region
                    potential_border_pixels.add((nr, nc))

        # Verify if the entire border is gray
        if not potential_border_pixels: # Should not happen for enclosed regions unless grid edge
            is_enclosed_by_gray = False
        else:
            for br, bc in potential_border_pixels:
                if input_np[br, bc] != 5: # Check color in the original input grid
                    is_enclosed_by_gray = False
                    break

        # If enclosed by gray, check area and fill
        if is_enclosed_by_gray:
            area = len(region)
            fill_color = area_color_map.get(area)

            if fill_color is not None:
                # Add the gray border pixels to our tracking set
                for br, bc in potential_border_pixels:
                     filled_region_borders.add((br, bc))

                # Fill the region in the output grid
                for r, c in region:
                    output_grid[r, c] = fill_color

    # --- Rule 2: Modify specific gray pixels ---

    # Iterate through the *input* grid to find target gray pixels
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 5: # Check if the pixel is gray in the original grid
                # Check if this gray pixel was part of a filled region's border
                if (r, c) in filled_region_borders:
                    continue # Skip this gray pixel if it was part of a filled border

                has_white_neighbor = False
                # Check 4 cardinal neighbors in the original input grid
                for nr, nc in _get_neighbors(r, c, height, width, connectivity=4):
                    if input_np[nr, nc] == 0: # Check for white neighbor
                        has_white_neighbor = True
                        break

                # If no white neighbor was found AND it wasn't a border pixel, change color
                if not has_white_neighbor:
                    output_grid[r, c] = 6 # Change to magenta

    # Return the result as a list of lists
    return output_grid.tolist()