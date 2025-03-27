```python
"""
Transforms an input grid by identifying non-background colors, detecting shapes and their adjacencies, and applying mirroring or extension transformations based on these adjacencies.
"""

import numpy as np
from collections import Counter

def get_background_color(grid):
    """Determines the most frequent (background) color in the grid."""
    flattened = grid.flatten()
    count = Counter(flattened)
    return count.most_common(1)[0][0]

def find_objects(grid, background_color):
    """Identifies connected components (objects) of non-background colors."""
    visited = set()
    objects = []

    def dfs(row, col, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] == background_color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)
        dfs(row + 1, col + 1, current_object)
        dfs(row - 1, col - 1, current_object)
        dfs(row + 1, col -1, current_object)
        dfs(row -1, col + 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != background_color and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append((grid[row,col], current_object))  # Store color and object
    return objects

def get_neighbors(grid, pixel):
    """Get the neighbors, including diagonals"""
    row,col = pixel
    neighbors = []
    for i in range(-1,2):
        for j in range(-1,2):
            if i==0 and j == 0:
                continue
            neighbor_row, neighbor_col = row+i, col+j
            if 0 <= neighbor_row < grid.shape[0] and 0 <= neighbor_col < grid.shape[1]:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors
    

def transform(input_grid):
    """Applies the transformation rules to the input grid."""
    grid = np.array(input_grid)  # Convert to NumPy array
    output_grid = np.copy(grid)
    background_color = get_background_color(grid)
    objects = find_objects(grid, background_color)

    for color, object_pixels in objects:
        for row, col in object_pixels:
            neighbors = get_neighbors(grid, (row,col))
            neighbor_colors = [grid[r,c] for r, c in neighbors]
            
            # Horizontal Extension
            
            left_neighbors = [c for r, c in neighbors if c < col and grid[r,c] != background_color]
            right_neighbors = [c for r, c in neighbors if c > col and grid[r,c] != background_color]
            
            if left_neighbors:
                min_col = min(left_neighbors)
                neighbor_color = grid[row, min_col]
                if neighbor_color != background_color and neighbor_color != color:
                    for i in range(col + 1, min(grid.shape[1], col + (col-min_col) + 1)):
                        output_grid[row, i] = neighbor_color
                        for n_r, n_c in get_neighbors(output_grid, (row,i)):
                            if grid[n_r,n_c] == color:
                                output_grid[n_r, n_c] = neighbor_color
            if right_neighbors:
                max_col = max(right_neighbors)
                neighbor_color = grid[row,max_col]
                if neighbor_color != background_color and neighbor_color != color:
                    for i in range(max(0, col - (max_col - col)), col):
                        output_grid[row, i] = neighbor_color
                        for n_r, n_c in get_neighbors(output_grid, (row,i)):
                            if grid[n_r,n_c] == color:
                                output_grid[n_r, n_c] = neighbor_color
            

            # Vertical Extension
            up_neighbors = [r for r, c in neighbors if r < row and grid[r,c] != background_color]
            down_neighbors =  [r for r, c in neighbors if r > row and grid[r,c] != background_color]

            if up_neighbors:
                min_row = min(up_neighbors)
                neighbor_color = grid[min_row,col]
                if neighbor_color != background_color and neighbor_color != color:
                    for i in range(row+1, min(grid.shape[0], row+(row-min_row)+1)):
                         output_grid[i, col] = neighbor_color
                         for n_r, n_c in get_neighbors(output_grid, (i,col)):
                            if grid[n_r,n_c] == color:
                                output_grid[n_r, n_c] = neighbor_color
            if down_neighbors:
                max_row = max(down_neighbors)
                neighbor_color = grid[max_row, col]
                if neighbor_color != background_color and neighbor_color != color:
                    for i in range(max(0, row-(max_row-row)), row):
                        output_grid[i,col] = neighbor_color
                        for n_r, n_c in get_neighbors(output_grid, (i,col)):
                            if grid[n_r,n_c] == color:
                                output_grid[n_r, n_c] = neighbor_color

    return output_grid.tolist()
```