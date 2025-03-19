"""
1. **Identify Clusters:** Locate distinct clusters of non-white (non-zero) pixels in the input grid.  A cluster is defined as a group of contiguous (adjacent horizontally or vertically, not diagonally) non-white pixels.
2. **Bounding Box:** For each identified cluster, determine the smallest rectangular bounding box that completely encloses all pixels of that cluster.
3. **Sample from Bounding Boxes:** Extract pixels by selecting information from the columns where non-white pixels first appear, and the rows where those pixels are in the input grid.
4. **Assemble Output:** Arrange these extracted pixels/rows in a condensed rectangular grid, and remove all complete rows and columns with white pixels. The output grid will contain only the information from that sampling.
"""

import numpy as np

def find_clusters(grid):
    """Finds clusters of non-zero pixels in a grid."""
    visited = set()
    clusters = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_cluster):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 0:
            return
        visited.add((r, c))
        current_cluster.append((r, c))
        neighbors = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        for nr, nc in neighbors:
            dfs(nr, nc, current_cluster)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_cluster = []
                dfs(r, c, current_cluster)
                clusters.append(current_cluster)
    return clusters

def bounding_box(cluster):
    """Calculates the bounding box of a cluster."""
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')
    for r, c in cluster:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return min_r, min_c, max_r, max_c

def extract_rows_cols(grid, clusters):
    """Extracts rows and columns of interest based on clusters."""
    rows_of_interest = set()
    cols_of_interest = set()

    for cluster in clusters:
        min_r, min_c, max_r, max_c = bounding_box(cluster)
        
        for r, c in cluster:
          rows_of_interest.add(r)
          cols_of_interest.add(c)

    #convert sets to sorted lists.
    rows_of_interest = sorted(list(rows_of_interest))
    cols_of_interest = sorted(list(cols_of_interest))

    return rows_of_interest, cols_of_interest



def transform(input_grid):
    # Convert input grid to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Clusters
    clusters = find_clusters(input_grid)

    # 2. & 3. Bounding Box and Sample
    rows_of_interest, cols_of_interest = extract_rows_cols(input_grid, clusters)


    # 4. Assemble Output - create a grid with the selected rows and columns
    # Create a subgrid
    subgrid = input_grid[np.ix_(rows_of_interest, cols_of_interest)]

    return subgrid.tolist()