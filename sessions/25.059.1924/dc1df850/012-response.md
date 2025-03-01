# dc1df850 • 012 • refine_coder

---
```python
"""
The transformation rule identifies a shape composed of connected red and green pixels, 
creates a bounding box around it, shifts the box one row down and one column left,
and recolors the interior of the translated box. The top-right pixel of this new shape is red,
and the rest are blue.
"""

import numpy as np

def get_colored_shape(input_grid):
    """
    Finds the largest contiguous block of connected red and green pixels.
    Pixels are considered connected if they touch directly or diagonally.
    """
    red = 2
    green = 3
    rows, cols = np.where((input_grid == red) | (input_grid == green))
    pixels = list(zip(rows, cols))

    if not pixels:
        return []

    # create adjacency matrix, where 1 is adjacent and 0 is not
    adj_matrix = np.zeros((len(pixels), len(pixels)), dtype=int)
    for i in range(len(pixels)):
        for j in range(i + 1, len(pixels)):
            row_i, col_i = pixels[i]
            row_j, col_j = pixels[j]
            # two pixels are defined as adjacent if they are touching directly or diagonally
            if abs(row_i - row_j) <= 1 and abs(col_i - col_j) <= 1:
                adj_matrix[i, j] = adj_matrix[j, i] = 1
    
    # perform depth first search to find largest cluster of 1's
    visited = [False] * len(pixels)
    def depth_first_search(index, cluster):
        visited[index] = True
        cluster.append(pixels[index])
        for i in range(len(pixels)):
            if adj_matrix[index, i] == 1 and not visited[i]:
                depth_first_search(i, cluster)
        
    # find clusters
    clusters = []
    for i in range(len(pixels)):
        if not visited[i]:
            current_cluster = []
            depth_first_search(i, current_cluster)
            clusters.append(current_cluster)
            
    # sort and return largest cluster of coordinates
    if len(clusters) > 0:
      clusters.sort(key=len, reverse=True)
      return clusters[0]
    else:
      return []

def create_bounding_box(coords):
    """Creates a bounding box around the given coordinates."""
    if not coords:
        return None
    min_row = min(r for r, _ in coords)
    max_row = max(r for r, _ in coords)
    min_col = min(c for _, c in coords)
    max_col = max(c for _, c in coords)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # get the colored shape
    shape = get_colored_shape(input_grid)

    if shape:
        # create bounding box
        box_start, box_end = create_bounding_box(shape)

        # translate bounding box
        t_row = box_start[0] + 1
        t_col = box_start[1] - 1
        t_box_end_row = box_end[0] + 1
        t_box_end_col = box_end[1] - 1

        # recolor inside translated box
        for r in range(t_row, t_box_end_row + 1):
            for c in range(t_col, t_box_end_col + 1):
                if r == t_row and c == t_col + 1:
                  output_grid[r][c] = 2 # set top-right to red
                elif r >= 0 and c >= 0:
                  output_grid[r][c] = 1  # set remaining to blue

    # copy other non-white pixels except original shape
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r][c] != 0 and (r, c) not in shape:
                output_grid[r][c] = input_grid[r][c]

    return output_grid
```
