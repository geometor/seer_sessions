"""
1.  **Identify Colored Regions:** Scan the input grid and identify contiguous regions of non-white (non-zero) pixels.  Consider each such region as a separate object.
2.  **Discard Background:** Ignore the white (0) pixels, treating them as background.
3.  **Extract Colors:** For each identified colored region, record its color value.
4. **Determine 3x3 Regions**: Divide the input into 9 regions, corresponding to the layout of the 3x3 output grid
5.  **Construct Output:** Create a 3x3 output grid. Place the identified colors into the output grid. If a region contains a color, put the color into the corresponding output cell.

"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-zero pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        """Depth-first search to find connected components."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_coords = []
                dfs(row, col, grid[row, col], obj_coords)
                objects.append({
                    'color': grid[row, col],
                    'coords': obj_coords
                })
    return objects

def transform(input_grid):
    # initialize output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find objects
    objects = find_objects(input_grid)
    
    # Get input grid dimensions
    height, width = input_grid.shape
    
    # Calculate region boundaries
    row_thirds = height // 3
    col_thirds = width // 3
    
    # Iterate over the objects and place the colors
    for obj in objects:
        # get a representative coordinate
        row, col = obj['coords'][0]
        # Determine the region
        y = min(row // row_thirds, 2)
        x = min(col // col_thirds, 2)
        # Place color if the output cell is empty
        if output_grid[y,x] == 0:
            output_grid[y,x] = obj['color']

    return output_grid