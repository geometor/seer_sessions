"""
1.  **Identify Objects:** Locate all contiguous blocks of non-zero pixels. Each block is an object.
2.  **Replicate Objects:** Find all objects with an initial shape of a single pixel.
3. **Horizontal Replication, Spaced**: Replicate the object horizontally until they touch another object, the edge of the object or the edge of the grid.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append(obj)
    return objects

def replicate_horizontally(grid, obj):
    """Replicates a single-pixel object horizontally."""
    output_grid = np.copy(grid)
    if len(obj) == 1:
        r, c = obj[0]
        color = grid[r,c]

        # Replicate to the right
        for i in range(c + 1, grid.shape[1]):
            if output_grid[r,i] == 0:
                output_grid[r, i] = color
            else:
                break #stop when blocked
        #replicate to the left
        for i in range(c-1, -1, -1):
            if output_grid[r, i] == 0:
                output_grid[r,i] = color
            else:
                break

    return output_grid



def transform(input_grid):
    """Transforms the input grid according to the replication rules."""
    # Find objects
    objects = find_objects(input_grid)
    # Initialize the output grid as a copy of the input.
    output_grid = np.copy(input_grid)


    # Replicate single-pixel objects.
    for obj in objects:
            output_grid = replicate_horizontally(output_grid, obj)
    
    # Move objects (if necessary, based on further examples).
    #  (Not needed for the provided example, but good to keep for future iterations)

    return output_grid