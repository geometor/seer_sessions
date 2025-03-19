import numpy as np

def grid_diff(grid1, grid2):
    """element by element diff of the grids"""
    if grid1.shape != grid2.shape:
        return "Shapes are different"
    diff = grid1 != grid2
    return diff

def count_pixel_colors(grid):
    """Counts the number of occurrences of each color in a grid."""
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    return color_counts

def find_single_pixels(grid):
    """Finds isolated pixels of unique colors, not part of larger same-color blocks."""
    rows, cols = grid.shape
    single_pixels = []
    visited = np.zeros((rows, cols), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color):
      
        count = 0
        stack = [(r,c)]
        elements = []

        while stack:
          row, col = stack.pop()

          if not is_valid(row, col) or visited[row, col] or grid[row,col] != color:
            continue
          
          visited[row,col] = True
          count += 1
          elements.append((row,col))

          neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
          for nr, nc in neighbors:
            stack.append((nr, nc))
        
        return count, elements
    
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r,c] != 0:
              color = grid[r,c]
              count, elements = dfs(r,c, color)
              if count == 1:
                single_pixels.append((r, c, color))
    return single_pixels

def get_grid_info(grid):
    """get metrics for the grid"""
    
    rows, cols = grid.shape
    
    color_count = count_pixel_colors(grid)
    
    single_pixels = find_single_pixels(grid)
    
    return {
        "rows":rows,
        "cols":cols,
        "color_counts": color_count,
        "single_pixel_count": len(single_pixels)
        }