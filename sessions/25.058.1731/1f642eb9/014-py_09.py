"""
1.  **Identify the azure (8) blob:** Locate the contiguous region of azure pixels in the input grid.
2.  **Identify surrounding pixels:** Find all single pixels that have colors and are not connected to anything on at least two sides.
3. Identify adjacent 8 pixels. For the pixels identified find the closest adjacent 8's.
4.  **Propagate/Mirror Colors**: Working from left to right, top to bottom. If an isolated pixel has a value different than 8, it will mirror its value to the adjacent 8 on its right, and the isolated pixel above will mirror to the 8 pixel below. If an isolated pixel of color is adjacent to an '8' along the shape's diagonal corners, it is assigned the value of the isolated color pixel.
"""

import numpy as np

def find_blob(grid, color):
    # Find the largest contiguous region of a specific color.
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    max_blob = []

    def dfs(r, c, current_blob):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_blob.append((r, c))
        dfs(r + 1, c, current_blob)
        dfs(r - 1, c, current_blob)
        dfs(r, c + 1, current_blob)
        dfs(r, c - 1, current_blob)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_blob = []
                dfs(r, c, current_blob)
                if len(current_blob) > len(max_blob):
                    max_blob = current_blob
    return max_blob

def get_neighbors(grid, r, c):
    # Get valid neighbors' coordinates and colors
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1,1), (-1,-1), (1, -1), (-1, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc, grid[nr, nc]))
    return neighbors

def find_isolated_pixels(grid):
   # Find single pixels of a different color surrounding the main blob.
    rows, cols = grid.shape
    isolated_pixels = []
    
    for r in range(rows):
        for c in range(cols):
             if grid[r,c] != 0 and grid[r,c] != 8:
                neighbors = get_neighbors(grid,r,c)
                count = 0
                for nr, nc, color in neighbors:
                    if color != 0 and color != 8:
                        count +=1
                
                if count <= 2:
                    isolated_pixels.append((r,c,grid[r,c]))

    return isolated_pixels


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find the azure (8) blob
    azure_blob = find_blob(input_grid, 8)

    # find isolated surrounding pixels
    isolated_pixels = find_isolated_pixels(input_grid)
    
    # Create a set for quick lookup of blob coordinates
    blob_coords = set(azure_blob)

    # Iterate through isolated pixels
    for r, c, color in isolated_pixels:
        neighbors = get_neighbors(input_grid, r, c)

        for nr, nc, ncolor in neighbors:
          #propagate color to right
          if nr == r and nc == (c + 1) and (nr,nc) in blob_coords:
              output_grid[nr,nc] = color

          #propagate color below
          if nr == (r+1) and nc == c and (nr,nc) in blob_coords:
              output_grid[nr,nc] = color
          
          #propagate color on the corners
          if (abs(nr-r) + abs(nc - c)) == 2 and (nr, nc) in blob_coords:
              output_grid[nr,nc] = color

    return output_grid