"""
1.  **Identify the relevant Grey and Red Regions:** Find the single contiguous grey region and the single contiguous red region that are involved in the transformation. These regions *must* share a direct boundary (adjacent pixels, not diagonal).
2.  **Identify White Pixels within Grey:** Locate all white pixels (0) contained *within* the identified grey region.
3.  **Mirror Across Boundary:** For each white pixel in the grey region:
    *   Find the *closest* grey pixel that is part of the grey-red boundary.
    *   Find the corresponding red pixel on the other side of that boundary point.
    *    Calculate the relative position vector between the white pixel and the grey boundary pixel.
    *   Apply this same relative position vector, starting from the corresponding *red* boundary pixel, to find the target pixel in the red region.
    *   Change the color of the target pixel in the red region to white (0), *if* the target pixel is within the bounds of the grid and is currently red.
4. Regions which do not have adjacent boundaries should remain unchanged.
"""

import numpy as np

def get_contiguous_region(grid, start_row, start_col, color):
    """
    Finds a single contiguous region of a given color, starting from a given cell.
    Returns a list of coordinates.
    """
    rows, cols = grid.shape
    visited = set()
    region = []

    def dfs(r, c):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            return
        visited.add((r, c))
        region.append((r, c))
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(start_row, start_col)
    return region

def find_adjacent_region(grid, region, target_color):
    """
    Finds a region of target_color adjacent to the given region.
    Returns None if no adjacent region of the target color is found.
    """
    rows, cols = grid.shape
    for r, c in region:
        # Check neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == target_color:
                return get_contiguous_region(grid, nr, nc, target_color)
    return None
    
def find_boundary(region1, region2):
    """
    Finds the boundary pixels between two regions.  Returns a list of tuples,
    where each tuple contains a pair of adjacent boundary pixels (one from each region).
    """
    boundary = []
    for r1, c1 in region1:
        for r2, c2 in region2:
            if abs(r1 - r2) + abs(c1 - c2) == 1:
                boundary.append(((r1, c1), (r2, c2)))
    return boundary

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the relevant Grey and Red Regions
    grey_regions = []
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] == 5:
          grey_regions.append(get_contiguous_region(input_grid, r, c, 5))
    
    for grey_region in grey_regions:
      red_region = find_adjacent_region(input_grid, grey_region, 2)

      if red_region: # Proceed only if an adjacent red region is found
          # 2. Identify White Pixels within Grey
          white_pixels_grey = [(r, c) for r, c in grey_region if input_grid[r, c] == 0]

          # 3. Mirror Across Boundary
          boundary = find_boundary(grey_region, red_region)

          for wr, wc in white_pixels_grey:
              # Find closest grey boundary pixel
              closest_boundary_grey = None
              min_dist = float('inf')
              for (gr, gc), (rr, rc) in boundary:
                  dist = abs(wr - gr) + abs(wc - gc)
                  if dist < min_dist:
                      min_dist = dist
                      closest_boundary_grey = (gr, gc)
                      closest_boundary_red = (rr, rc) # Corresponding red pixel

              # Calculate and apply relative position
              if closest_boundary_grey:  # Ensure we found a boundary pixel
                rel_row = wr - closest_boundary_grey[0]
                rel_col = wc - closest_boundary_grey[1]

                target_r = closest_boundary_red[0] + rel_row
                target_c = closest_boundary_red[1] + rel_col

                # Check bounds and color before changing
                if 0 <= target_r < rows and 0 <= target_c < cols and output_grid[target_r, target_c] == 2:
                    output_grid[target_r, target_c] = 0

    return output_grid