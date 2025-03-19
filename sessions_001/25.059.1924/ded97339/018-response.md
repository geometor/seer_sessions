# ded97339 • 018 • refine_coder

---
```python
"""
1.  **Identify Azure Regions:** Locate all contiguous regions of azure pixels in the input grid. Consider each connected region of azure pixels as a single object.
2.  **Connect nearest isolated regions:** Find the two closest isolated azure regions (measured by the Manhattan distance between their nearest edges/pixels).
3.  **Create Manhattan Path:** Draw a path of azure pixels connecting these two regions, using only horizontal and vertical movements (Manhattan distance).
4. **Repeat:** repeat steps 2 & 3 until all isolated azure regions have been combined into one region.
5.  **Output:** Return the modified grid.
"""

import numpy as np
from scipy.ndimage import label

def get_azure_regions(grid):
    """Identifies and labels contiguous regions of azure (8) pixels."""
    labeled_grid, num_regions = label(grid == 8)
    return labeled_grid, num_regions

def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_closest_regions(labeled_grid, num_regions):
    """Finds the two closest distinct azure regions."""
    min_dist = float('inf')
    closest_pair = None

    region_coords = {}
    for r in range(1, num_regions + 1):
        region_coords[r] = np.array(np.where(labeled_grid == r)).T

    for r1 in range(1, num_regions + 1):
        for r2 in range(r1 + 1, num_regions + 1):
            for p1 in region_coords[r1]:
                for p2 in region_coords[r2]:
                    dist = manhattan_distance(p1, p2)
                    if dist < min_dist:
                        min_dist = dist
                        closest_pair = (r1, r2, tuple(p1), tuple(p2)) # store regions and closest points

    return closest_pair


def connect_regions(grid, labeled_grid, region_pair):
    """Connects two regions with a Manhattan path of azure pixels."""
    if region_pair is None:
        return

    r1, r2, start, end = region_pair
    
    current = list(start)
    
    while current[0] != end[0] or current[1] != end[1]:
        grid[current[0], current[1]] = 8

        if current[0] < end[0]:
            current[0] += 1
        elif current[0] > end[0]:
            current[0] -= 1
        elif current[1] < end[1]:
            current[1] += 1
        elif current[1] > end[1]:
            current[1] -= 1

    grid[end[0], end[1]] = 8 # make sure end point is set to 8


def transform(input_grid):
    """Transforms the input grid by connecting azure regions using Manhattan distance paths."""
    output_grid = np.copy(input_grid)

    # Identify Azure Regions
    labeled_grid, num_regions = get_azure_regions(output_grid)

    # Connect nearest isolated regions until only one remains
    while num_regions > 1:
        # Find the two closest isolated azure regions
        closest_pair = find_closest_regions(labeled_grid, num_regions)

        # Create Manhattan Path
        connect_regions(output_grid, labeled_grid, closest_pair)
        
        labeled_grid, num_regions = get_azure_regions(output_grid)

    return output_grid
```
