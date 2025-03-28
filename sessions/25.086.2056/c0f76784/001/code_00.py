"""
Transforms the input grid based on two rules:
1.  Find hollow rectangles made of gray (5) pixels enclosing a region of white (0) pixels.
    Fill the enclosed white region with a color based on its area:
    - Area 1: magenta (6)
    - Area 4: orange (7)
    - Area 6: orange (7)
    - Area 9: azure (8)
2.  Identify gray (5) pixels in the input grid that are not adjacent (up, down, left, right)
    to any white (0) pixels. Change these specific gray pixels to magenta (6) in the output grid.
"""

import numpy as np
from collections import deque

def _get_neighbors(r, c, height, width, connectivity=4):
    """Gets valid neighbor coordinates for a pixel."""
    neighbors = []
    if connectivity == 4:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elif connectivity == 8:
        directions = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else:
        raise ValueError("Connectivity must be 4 or 8")

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def _find_regions(grid, target_color):
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
                    for nr, nc in _get_neighbors(curr_r, curr_c, height, width, connectivity=4):
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

    # --- Rule 1: Fill hollow gray rectangles ---

    # Define the area-to-color mapping
    area_color_map = {
        1: 6,  # magenta
        4: 7,  # orange
        6: 7,  # orange
        9: 8,  # azure
    }

    # Find all white regions
    white_regions = _find_regions(input_np, 0)

    for region in white_regions:
        is_hollow_rectangle = True
        bordering_pixels_colors = set()
        
        # Check neighbors of all pixels in the white region
        for r, c in region:
            # Use 8-connectivity to check surrounding border
            for nr, nc in _get_neighbors(r, c, height, width, connectivity=8):
                if (nr, nc) not in region: # Check only pixels outside the region
                    neighbor_color = input_np[nr, nc]
                    bordering_pixels_colors.add(neighbor_color)

        # Verify if all bordering pixels are gray (5)
        if not bordering_pixels_colors or not all(color == 5 for color in bordering_pixels_colors):
            is_hollow_rectangle = False

        # If it's a hollow rectangle, calculate area and fill
        if is_hollow_rectangle:
            area = len(region)
            fill_color = area_color_map.get(area) # Get color from map, returns None if area not found

            if fill_color is not None:
                # Fill the region in the output grid
                for r, c in region:
                    output_grid[r, c] = fill_color

    # --- Rule 2: Modify isolated gray pixels ---

    # Iterate through the *input* grid to find target gray pixels
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 5: # Check if the pixel is gray in the original grid
                has_white_neighbor = False
                # Check 4 cardinal neighbors in the original grid
                for nr, nc in _get_neighbors(r, c, height, width, connectivity=4):
                    if input_np[nr, nc] == 0: # Check for white neighbor
                        has_white_neighbor = True
                        break
                
                # If no white neighbor was found, change color in the output grid
                if not has_white_neighbor:
                    output_grid[r, c] = 6 # Change to magenta

    # Convert back to list of lists if necessary, otherwise return NumPy array
    # Assuming the standard test framework expects list of lists
    return output_grid.tolist()
