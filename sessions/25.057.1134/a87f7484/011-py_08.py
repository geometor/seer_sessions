"""
1. **Identify Orange Clusters:** Find all contiguous clusters of orange (7) pixels in the input grid. A cluster can be a single pixel or a larger connected shape.
2. **Determine Output Size:**. Observe the size of the output grid.
3. **Copy Per Output Size:**
    - If the output size is the same as input and input contains only one color, copy input to output.
    - Otherwise, create an output grid filled with black (0).
    - For the given output size and for each orange object in the input, copy the object to the output centered relative to its location in the input. If multiple object would overlap, only keep the latest object.
"""

import numpy as np

def get_clusters(grid, key_color):
    """
    Finds clusters of the key color in the grid.
    Returns a list of (pixels), where pixels is a list of (row, col) tuples.
    """
    visited = set()
    clusters = []

    def dfs(row, col):
        """Depth-first search to find connected components."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or grid[row, col] != key_color
            or (row, col) in visited
        ):
            return []

        visited.add((row, col))
        cluster_pixels = [(row, col)]

        cluster_pixels.extend(dfs(row + 1, col))
        cluster_pixels.extend(dfs(row - 1, col))
        cluster_pixels.extend(dfs(row, col + 1))
        cluster_pixels.extend(dfs(row, col - 1))
        return cluster_pixels

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == key_color and (row, col) not in visited:
                cluster_pixels = dfs(row, col)
                if cluster_pixels:
                    clusters.append(cluster_pixels)
    return clusters

def get_object_bounds(cluster_pixels):
    """
    Find the top-left and bottom-right corner for object
    """
    rows, cols = zip(*cluster_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return (min_row, min_col), (max_row, max_col)
    

def transform(input_grid, output_grid_shape):
    input_grid = np.array(input_grid)
    output_grid = np.zeros(output_grid_shape, dtype=int)
    
    # Check if the input grid is all one color and output sizes match
    unique_colors = np.unique(input_grid)
    if len(unique_colors) == 1 and input_grid.shape == output_grid_shape:
        return input_grid.copy()
    
    orange_clusters = get_clusters(input_grid, 7)
    
    for cluster_pixels in orange_clusters:
        # find bounds of object
        (min_row, min_col), (max_row, max_col) = get_object_bounds(cluster_pixels)

        # calculate the center of input object
        obj_center_row = (min_row + max_row) // 2
        obj_center_col = (min_col + max_col) // 2
        
        # determine shift needed
        output_center_row = output_grid.shape[0] // 2
        output_center_col = output_grid.shape[1] // 2
        
        row_shift = output_center_row - obj_center_row
        col_shift = output_center_col - obj_center_col
        
        # copy object to output using shift
        for row, col in cluster_pixels:
          output_row = row + row_shift
          output_col = col + col_shift
          if 0 <= output_row < output_grid.shape[0] and 0 <= output_col < output_grid.shape[1]:
              output_grid[output_row, output_col] = 7
              
    return output_grid