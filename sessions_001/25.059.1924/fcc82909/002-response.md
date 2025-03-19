# fcc82909 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate all contiguous regions (objects) of non-zero pixels in the input grid.
2.  **Color Replacement Area:** Locate all 2x2 clusters.
3.  **Green Expansion:** Create the target area. Add green (value 3) pixels:
    *   Below each original 2x2 cluster of non-zero pixels, fill up empty space.
    *   Below each original non-zero pixels that don't contain in 2x2 cluster, fill with two rows of green pixels.
    *   If any 2x2 cluster adjacent at row, fill with one row of green color, and put this row in between these objects.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-zero pixels."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 0:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def find_2x2_clusters(grid):
    """Finds 2x2 clusters of non-zero pixels."""
    clusters = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if all(grid[r+dr, c+dc] != 0 for dr in range(2) for dc in range(2)):
                clusters.append([(r, c), (r+1, c), (r, c+1), (r+1, c+1)])
    return clusters

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Find 2x2 clusters
    clusters_2x2 = find_2x2_clusters(grid)

    # Find objects
    objects = find_objects(grid)    
    
    # Green expansion for 2x2 clusters
    for cluster in clusters_2x2:
        # Find the lowest row in the cluster
        min_row = min(r for r, _ in cluster)
        max_row = max(r for r, _ in cluster)
        
        # check adjacent at same row
        adjacent_row = False
        for obj in clusters_2x2:
            if obj == cluster:
                continue            
            if min(row for row, _ in obj) == min_row:
                adjacent_row = True
                break

        if adjacent_row:       
            for c in range(cols):
                if output_grid[max_row,c] != 0:
                    output_grid[max_row+1,c] = 3
        else:   
            # Fill downwards with green
            for r in range(max_row + 1, rows):
                for r_c, c in cluster:
                    output_grid[r,c%cols] = 3
    
    # Fill two rows for separate objects
    added = set()
    for obj in objects:       
        is_2x2 = False

        # Check if this object include any 2x2 item
        for c_obj in clusters_2x2:
            if set(obj).issuperset(set(c_obj)):            
                is_2x2 = True
                break
        
        if is_2x2 == False:
            max_row = 0
            for r, c in obj:
                if output_grid[r,c] != 0:
                    if (r,c) not in added:                        
                        max_row = max(max_row, r)
                        added.add((r,c))

            for r, c in obj:   
                output_grid[max_row+1,c] = 3
                output_grid[max_row+2,c] = 3

    return output_grid.tolist()
```
