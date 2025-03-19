"""
1.  **Identify the central "island":** Locate the contiguous region of azure (8) pixels surrounding the blue (1) and yellow (4) pixels in the input.

2. **Mirror/Reflect:**
    - Notice that the central "island" of azure, blue, and yellow has its colors mirrored on either side of the central yellow and blue regions.
    - The azure acts as the mirror boundary and the colors are reflected in this boundary.

3.  **Color Replacement (within the mirrored region):**
    -   Within the region that's reflected, replace azure with a new reflected color in the output grid based on reflection across the boundary:
        -   Yellow on the right boundary becomes azure on the right hand side of the output
        -   Blue on the right boundary becomes Yellow on the right hand side of the output
        -   Azure on the right boundary becomes blue on the right hand side of the output

4.  **Color preservation (outside defined region):** All pixels not explicitly mentioned above retain their original color from the input grid in the output grid.
"""

import numpy as np

def find_island(grid, core_colors):
    """Finds the contiguous azure region around the core colors."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    island_pixels = []

    # Find a starting pixel of a core color
    start_row, start_col = -1, -1
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in core_colors:
                start_row, start_col = r, c
                break
        if start_row != -1:
            break

    if start_row == -1:
        return []

    # Explore the connected region using DFS
    stack = [(start_row, start_col)]
    while stack:
        r, c = stack.pop()
        if 0 <= r < rows and 0 <= c < cols and not visited[r, c]:
            visited[r, c] = True
            if grid[r, c] == 8 or grid[r,c] in core_colors :  # Include azure and core colors
                island_pixels.append((r, c))
                # Add neighbors to the stack
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    stack.append((r + dr, c + dc))

    return island_pixels

def transform(input_grid):
    """Transforms the input grid according to the mirroring and color replacement rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the central "island"
    core_colors = [1, 4]  # Blue and Yellow
    island_pixels = find_island(input_grid, core_colors)
    if not island_pixels:
      return output_grid
    
    island_pixels_set = set(island_pixels)

    #find yellow and blue regions
    yellow_pixels = []
    blue_pixels = []
    for r,c in island_pixels:
      if input_grid[r,c] == 4:
        yellow_pixels.append((r,c))
      elif input_grid[r,c] == 1:
        blue_pixels.append((r,c))

    min_yellow_col = min(c for r,c in yellow_pixels)
    max_yellow_col = max(c for r,c in yellow_pixels)
    
    min_blue_col = min(c for r,c in blue_pixels)
    max_blue_col = max(c for r,c in blue_pixels)
        
    # 3. Color Replacement (within the island)
    for r, c in island_pixels:

        #mirror from the perspective of yellow
        if c < min_yellow_col:
          mirror_c =  min_yellow_col + (min_yellow_col - c) -1
          if (r,mirror_c) in island_pixels_set:
              if input_grid[r,mirror_c] == 4: #yellow
                output_grid[r, c] = 8       #azure   
              elif input_grid[r,mirror_c] == 1: #blue
                output_grid[r,c] = 4     #yellow
              elif input_grid[r,mirror_c] == 8: #azure
                output_grid[r,c] = 1 #blue
        
        #mirror from the perspective of blue
        if c > max_yellow_col:
          mirror_c =  max_yellow_col - (c - max_yellow_col) + 1
          
          if (r,mirror_c) in island_pixels_set:
            
            if input_grid[r,mirror_c] == 4:
              output_grid[r, c] = 8  #azure
            elif input_grid[r,mirror_c] == 1:
              output_grid[r,c] = 4    #yellow
            elif input_grid[r,mirror_c] == 8:
              output_grid[r,c] = 1 #blue

    return output_grid