```python
import numpy as np
from collections import deque

"""
Identifies clusters of red (2) pixels in the input grid where clusters are defined by 8-directional adjacency (including diagonals). For each cluster containing two or more red pixels, calculates the bounding box that encompasses all pixels in the cluster *plus* all of their 8-directional neighbors. Fills this bounding box area in the output grid with green (3). Finally, restores the original red pixels belonging to the cluster within the filled area back to red (2). Isolated red pixels (clusters of size 1) and the background remain unchanged.
"""

def get_neighbors(grid_shape, r, c, connectivity=8):
    """Gets valid neighbor coordinates for a pixel."""
    neighbors = []
    rows, cols = grid_shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            if connectivity == 4 and abs(dr) + abs(dc) > 1: # Skip diagonals for 4-connectivity
                 continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def find_clusters(grid, color):
    """Finds connected components (clusters) of a given color using 8-way adjacency."""
    rows, cols = grid.shape
    visited = set()
    clusters = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                # Start BFS for a new cluster
                current_cluster = []
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_cluster.append((curr_r, curr_c))
                    
                    # Check 8 neighbors
                    for nr, nc in get_neighbors((rows, cols), curr_r, curr_c, connectivity=8):
                        if grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                if current_cluster:
                    clusters.append(current_cluster)
                    
    return clusters

def transform(input_grid):
    """
    Transforms the input grid based on red pixel clusters.

    1. Finds clusters of red pixels (color 2).
    2. Filters clusters to keep only those with size >= 2.
    3. For each valid cluster:
       a. Determines the region including cluster pixels and their neighbors.
       b. Calculates the bounding box of this region.
       c. Fills the bounding box with green (color 3) in the output grid.
       d. Restores the original red pixels of the cluster within the bounding box.
    """
    
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Define the target color (red)
    target_color = 2
    fill_color = 3
    
    # Find all clusters of the target color
    clusters = find_clusters(input_grid, target_color)
    
    # Filter clusters to keep only those with size 2 or more
    valid_clusters = [cluster for cluster in clusters if len(cluster) >= 2]
    
    # Process each valid cluster
    for cluster in valid_clusters:
        # Determine the region of interest (cluster pixels + neighbors)
        region_coords = set()
        for r, c in cluster:
            region_coords.add((r, c)) # Add the cluster pixel itself
            # Add all 8 neighbors
            for nr, nc in get_neighbors((rows, cols), r, c, connectivity=8):
                 region_coords.add((nr, nc))

        # If no region coords found (should not happen for valid clusters), skip
        if not region_coords:
             continue

        # Calculate the bounding box of the region
        min_r = min(r for r, c in region_coords)
        max_r = max(r for r, c in region_coords)
        min_c = min(c for r, c in region_coords)
        max_c = max(c for r, c in region_coords)
        
        # Fill the bounding box area in the output grid with the fill color (green)
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                # Ensure we don't go out of bounds (although bounding box should be within bounds)
                if 0 <= r < rows and 0 <= c < cols:
                     output_grid[r, c] = fill_color
                     
        # Restore the original target color pixels (red) belonging to this cluster
        for r, c in cluster:
             # Check bounds just in case, though cluster pixels should be valid
             if 0 <= r < rows and 0 <= c < cols:
                output_grid[r, c] = target_color
                
    return output_grid
```