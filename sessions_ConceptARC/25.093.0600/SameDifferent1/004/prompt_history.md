
## train_1

**input:**
```
0 0 0 0 0 0 8 0 0 0
0 2 2 2 0 8 8 8 0 0
0 2 2 2 0 0 8 8 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 5 5 5 0
0 0 1 1 1 0 0 5 5 0
0 0 1 1 1 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
6 6 0 0 0 0 4 4
0 0 0 0 0 0 4 4
0 0 4 0 0 0 4 4
0 4 4 4 0 0 0 0
0 0 4 0 0 2 0 0
0 0 0 0 2 2 2 0
7 7 0 0 0 2 0 0
7 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 4 4 4 0 0 0 0
0 0 4 0 0 2 0 0
0 0 0 0 2 2 2 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 7 7 7 0 3 3 3 0
0 0 7 0 0 0 3 0 0
0 7 7 7 0 3 3 3 0
0 0 0 0 0 7 7 7 0
0 3 3 3 0 7 7 7 0
0 0 3 0 0 7 7 7 0
0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 7 7 7 0 3 3 3 0
0 0 7 0 0 0 3 0 0
0 7 7 7 0 3 3 3 0
0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception of Elements:**

1.  **Input/Output:** Both are 2D grids (matrices) containing single-digit integers (0-9). The digit '0' consistently represents the background.
2.  **Objects:** The core objects are "regions" or "blobs" of connected cells sharing the same non-zero digit. Connectivity is defined by horizontal and vertical adjacency (not diagonal).
3.  **Properties:**
    *   Each region has a specific color (the digit value).
    *   Each region has a shape and size (number of cells).
    *   Each region has a position within the grid.
    *   A key property seems to be whether any part of the region touches the outer border/edge of the grid.
4.  **Transformation:** The transformation involves selectively removing entire regions based on a specific property. Regions that are removed are replaced by the background color '0'. Regions that are not removed remain unchanged in the output.
5.  **Underlying Rule:** Based on the examples, the rule appears to be: Identify all connected regions of non-zero colors. If *any* cell belonging to a region is located on the grid's outermost border (top row, bottom row, leftmost column, or rightmost column), then the *entire* region is removed (set to '0'). If a region is entirely contained within the grid and does not touch any border, it is preserved in the output.

**YAML Fact Documentation:**


```yaml
task_description: Remove connected regions of color if they touch the grid border.

elements:
  - element: grid
    properties:
      - type: 2D array of integers
      - dimensions: variable (e.g., 10x10, 8x8, 9x9)
      - cell_values: integers 0-9
      - background_color: 0

  - element: region
    properties:
      - type: connected component of non-zero cells
      - connectivity: horizontal and vertical adjacency
      - color: the integer value (1-9) shared by cells in the region
      - location: set of coordinates (row, col) occupied by the region
      - border_touching: boolean (true if any cell in the region is in row 0, last row, col 0, or last col)

actions:
  - action: identify_regions
    input: input grid
    output: list of regions (each with color, coordinates, border_touching property)
    description: Finds all connected components of non-zero cells. For each component, determine its color, cell coordinates, and whether it touches the grid border.

  - action: filter_regions
    input: list of regions
    output: list of regions_to_keep
    description: Selects only those regions where the 'border_touching' property is false.

  - action: generate_output_grid
    input:
      - input grid dimensions
      - list of regions_to_keep
    output: output grid
    description: Creates a new grid filled with the background color ('0'). Then, for each region in 'regions_to_keep', place its color value at its corresponding coordinates in the new grid.

relationships:
  - relationship: border_determines_removal
    subject: region
    object: grid border
    description: A region's 'border_touching' status determines if it is kept or removed in the output grid. Removal applies to the entire region if any part touches the border.
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color '0'.
2.  Find all distinct connected regions of cells in the input grid that have the same non-zero color. Use 4-way adjacency (up, down, left, right) to determine connectivity.
3.  For each identified region:
    a.  Check if any cell belonging to this region is located at row 0, the last row, column 0, or the last column of the input grid.
    b.  If *none* of the cells in the region touch any of the grid's borders, then copy all cells belonging to this region (with their original color) from the input grid to the corresponding positions in the output grid.
4.  Return the final output grid.
```python
import numpy as np
from collections import deque

"""
Identifies connected regions of non-zero colors in the input grid. 
If any part of a region touches the outer border of the grid, the entire region is removed (set to 0). 
Regions entirely contained within the grid (not touching any border) are preserved in the output.
"""

def _find_regions(grid):
    """
    Finds all connected regions of non-zero cells using BFS.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a region
              and contains 'color', 'cells' (a set of (row, col) tuples),
              and 'touches_border' (boolean).
    """
    rows, cols = grid.shape
    visited = set()
    regions = []

    for r in range(rows):
        for c in range(cols):
            # If the cell is non-zero and not yet visited, start a BFS
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                current_region_cells = set()
                touches_border = False
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    current_region_cells.add((row, col))

                    # Check if the current cell is on the border
                    if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                        touches_border = True

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, if not visited, and if it's part of the same color region
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and \
                           grid[nr, nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                regions.append({
                    'color': color,
                    'cells': current_region_cells,
                    'touches_border': touches_border
                })
    return regions

def transform(input_grid):
    """
    Transforms the input grid by removing connected regions of non-zero colors
    if they touch the grid border.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # Initialize output_grid with zeros (background color)
    output_grid = np.zeros_like(grid_np)

    # Find all regions in the input grid
    regions = _find_regions(grid_np)

    # Iterate through the found regions
    for region in regions:
        # If a region does NOT touch the border, copy it to the output grid
        if not region['touches_border']:
            color = region['color']
            for r, c in region['cells']:
                output_grid[r, c] = color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```
```python
import numpy as np
from collections import deque

"""
Identifies connected regions of non-zero colors in the input grid using 4-way 
adjacency (up, down, left, right). If any cell belonging to a specific region 
is located on the grid's outermost border (top row, bottom row, leftmost 
column, or rightmost column), then the entire region is removed (replaced 
with the background color '0'). Regions that are entirely contained within the 
grid and do not touch any border are preserved in the output grid.
"""

def _find_regions_and_filter(grid_np):
    """
    Finds all connected regions of non-zero cells using BFS and determines
    if they touch the border. Returns only the regions that do NOT touch
    the border.

    Args:
        grid_np (np.array): The input grid as a NumPy array.

    Returns:
        list: A list of dictionaries, where each dictionary represents a region
              to keep and contains 'color' and 'cells' (a list of 
              (row, col) tuples).
    """
    rows, cols = grid_np.shape
    visited = set()
    regions_to_keep = []

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # If the cell is non-zero and hasn't been visited yet, it's the start of a new potential region
            if grid_np[r, c] != 0 and (r, c) not in visited:
                color = grid_np[r, c]
                current_region_cells = []
                touches_border = False
                q = deque([(r, c)])
                visited.add((r, c))
                
                # Perform Breadth-First Search (BFS) to find all connected cells of the same color
                while q:
                    row, col = q.popleft()
                    current_region_cells.append((row, col))

                    # Check if the current cell is on the border
                    # Use >= rows - 1 and >= cols - 1 for safety, although == should suffice
                    if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                        touches_border = True # Mark the entire region as touching the border

                    # Explore neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the same color and hasn't been visited
                            if grid_np[nr, nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                                
                # After exploring the entire region, decide whether to keep it
                if not touches_border:
                    regions_to_keep.append({
                        'color': color,
                        'cells': current_region_cells,
                    })
                    
    return regions_to_keep

def transform(input_grid):
    """
    Transforms the input grid by removing connected regions of non-zero colors
    if they touch the grid border.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid with the same dimensions, filled with the background color (0)
    output_grid = np.zeros_like(grid_np)

    # Find all regions in the input grid that do NOT touch the border
    regions_to_keep = _find_regions_and_filter(grid_np)

    # Iterate through the regions that should be kept
    for region in regions_to_keep:
        color = region['color']
        # Place the color of the kept region onto the corresponding cells in the output grid
        for r, c in region['cells']:
            output_grid[r, c] = color

    # Convert the resulting NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()
```
