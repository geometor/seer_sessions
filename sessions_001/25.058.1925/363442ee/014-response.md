# 363442ee • 014 • refine_coder

---
```python
"""
The input grid's top-left cluster (containing non-zero pixels) is replicated across the entire output grid. The output grid maintains the same dimensions as the input grid. Transparent pixels (value 0) within the identified cluster are not copied during replication. The size of the cluster is determined dynamically based on the input grid.
"""

import numpy as np

def get_top_left_cluster(grid, cluster_dims):
    """Extracts the top-left cluster from the input grid based on calculated dimensions."""
    return grid[:cluster_dims[0], :cluster_dims[1]]

def transform(input_grid):
    """Transforms the input grid by replicating the top-left cluster."""

    # Initialize output grid with the same dimensions as the input.
    output_grid = np.zeros_like(input_grid)

    #find dimensions
    input_dims = input_grid.shape

    # Find non-zero pixels in the top-left region of the input
    input_nonzero = np.transpose(np.nonzero(input_grid))

    #cluster
    #find the unique values in output
    unique_values = np.unique(input_grid) #use input grid
    cluster_values = [uv for uv in unique_values if uv != 0]


    #find matching section:
    cx_max = 0
    cy_max = 0

    if len(input_nonzero) > 0:
        for (cx,cy) in input_nonzero:
            if input_grid[cx,cy] in cluster_values:
                if cx > cx_max:
                    cx_max = cx
                if cy > cy_max:
                    cy_max = cy

    cluster_dims = (cx_max+1,cy_max+1)

    # Get the top-left cluster.
    cluster = get_top_left_cluster(input_grid, cluster_dims)
    rows_cluster, cols_cluster = cluster.shape

    #find grey background in input
    rows, cols = input_grid.shape
    
    # Replicate and position the cluster horizontally and vertically
    for i in range(0, rows, rows_cluster):
        for j in range(0, cols, cols_cluster):
             for x in range(rows_cluster):
                 for y in range(cols_cluster):
                    if i + x < rows and j + y < cols:
                      if cluster[x,y] != 0:  #dont copy if grey
                         output_grid[i + x, j + y] = cluster[x, y]

    return output_grid
```
