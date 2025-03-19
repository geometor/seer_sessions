"""
1.  **Identify Contiguous Regions:** Identify all contiguous regions of pixels, where "contiguous" means connected horizontally or vertically (not diagonally).
2.  **Gray Region Expansion:** The gray (5) regions expand, *but only to fill gaps within their own initial outer perimeter, and to enclose any colored pixels inside the region*. It's not a general expansion outwards in all directions, but a filling of internal concavities and complete surrounding of internal colors. It does not expand into "empty" (0-colored) areas beyond what could be considered its initial outline.
3. **Blue Region (and other colors) Expansion:** A single isolated colored pixels, surrounded by grey expands to fill a 3 x 1 region within the grey region, centered on its original location.
4. If any regions created by rules 2 and 3 overlap, prefer the color that was not grey in the input.
"""

import numpy as np

def get_contiguous_regions(grid):
    """
    Identifies contiguous regions of the same color.
    Returns a dictionary of regions, where the key is the color and the value is a list of (row, col) tuples.
    """
    visited = set()
    regions = {}
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if (r, c) not in visited and color != 0:
                if color not in regions:
                    regions[color] = []
                stack = [(r, c)]
                visited.add((r, c))
                while stack:
                    curr_r, curr_c = stack.pop()
                    regions[color].append((curr_r, curr_c))

                    neighbors = []
                    if curr_r > 0: neighbors.append((curr_r - 1, curr_c))
                    if curr_r < rows - 1: neighbors.append((curr_r + 1, curr_c))
                    if curr_c > 0: neighbors.append((curr_r, curr_c - 1))
                    if curr_c < cols - 1: neighbors.append((curr_r, curr_c + 1))

                    for nr, nc in neighbors:
                        if (nr, nc) not in visited and grid[nr, nc] == color:
                            stack.append((nr, nc))
                            visited.add((nr, nc))
    return regions

def get_perimeter(region_pixels, rows, cols):
    """Calculates the perimeter of a region."""
    perimeter = set()
    for r, c in region_pixels:
        neighbors = []
        if r > 0: neighbors.append((r - 1, c))
        if r < rows - 1: neighbors.append((r + 1, c))
        if c > 0: neighbors.append((r, c - 1))
        if c < cols - 1: neighbors.append((r, c + 1))

        for nr, nc in neighbors:
            if (nr, nc) not in region_pixels:
                perimeter.add((nr, nc)) #add all empty neighbors
    return list(perimeter)

def expand_blue_region(grid, regions):
  """Expands the blue region if its isolated and within a gray region"""
  rows, cols = grid.shape
  new_grid = np.copy(grid)

  for color, pixels in regions.items():
      if color != 5 and len(pixels) == 1:  # Check for single-pixel regions (non-gray)
        r,c = pixels[0]
        #check if it's sourrounded by gray
        is_surrounded = True
        if r > 0: is_surrounded = is_surrounded and (grid[r-1, c] == 5 or grid[r-1, c] == color) #allow self-expansion
        if r < rows - 1: is_surrounded = is_surrounded and (grid[r+1, c] == 5 or grid[r+1, c] == color)
        if c > 0: is_surrounded = is_surrounded and (grid[r, c - 1] == 5 or grid[r,c-1] == color)
        if c < cols - 1: is_surrounded =  is_surrounded and (grid[r, c + 1] == 5 or grid[r, c+1] == color)

        if is_surrounded:
          new_grid[r,c] = color #center
          if r > 0: new_grid[r - 1, c] = color  # Above
          if r < rows - 1: new_grid[r + 1, c] = color  # Below
  return new_grid
def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # get contiguous regions
    regions = get_contiguous_regions(input_grid)

    #expand blue region
    output_grid = expand_blue_region(output_grid, regions)

    # gray region expansion (fill gaps within perimeter)
    if 5 in regions:
        gray_perimeter = get_perimeter(regions[5], rows, cols)
        for r, c in gray_perimeter:
            if output_grid[r,c] == 0: #fill with grey, only if it's currently empty
              output_grid[r, c] = 5

    return output_grid.tolist()