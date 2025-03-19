"""
1. Identify Objects: Locate all distinct contiguous regions of pixels with the same color within the input grid. Consider these regions as separate objects.
2. Filter by Color: Disregard all objects that are *not* colored azure (8).
3. Select Sub-grid: find, and extract the smallest 2x2 square sub-grid in azure. If no such subgrid exist output nothing.
4. output the sub-grid.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions of the same color in a grid.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        A list of objects, where each object is a list of (row, col) tuples.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, object_pixels):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        object_pixels.append((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                color = grid[row, col]
                object_pixels = []
                dfs(row, col, color, object_pixels)
                if object_pixels:
                    objects.append(object_pixels)
    return objects

def extract_subgrid(grid, object_pixels, size=2):
    """Extracts a square subgrid of given size from object, if exist"""
    min_row, min_col = float('inf'), float('inf')
    max_row, max_col = float('-inf'), float('-inf')

    for r, c in object_pixels:
         min_row = min(min_row, r)
         min_col = min(min_col, c)
         max_row = max(max_row, r)
         max_col = max(max_col, c)
    
    for r in range(min_row, max_row +1):
        for c in range(min_col, max_col +1):
            if (r+1 <= max_row and c + 1 <= max_col and grid[r,c] == grid[r+1,c] ==
            grid[r, c+1] == grid[r+1, c+1]):
                return np.array([[grid[r,c], grid[r,c+1]], [grid[r+1,c], grid[r+1, c+1]]])

    return None
    

def transform(input_grid):
    # Find all objects in the grid
    objects = find_objects(input_grid)

    # Filter objects by color (azure = 8)
    azure_objects = [obj for obj in objects if input_grid[obj[0]] == 8]
    
    output_grid = None
    # Extract the 2x2 sub-grid from the azure objects
    for azure_obj in azure_objects:
       output_grid =  extract_subgrid(input_grid, azure_obj)
       if output_grid is not None:
           break
    
    if output_grid is None:
        return np.array([])

    return output_grid