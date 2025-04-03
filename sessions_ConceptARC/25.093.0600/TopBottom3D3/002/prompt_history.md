
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 0 2 2 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0
0 3 4 4 4 4 3 0
0 3 4 4 4 4 3 0
0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 0
0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 6 0 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves transforming a 2D grid of colored cells. The input grids contain distinct regions of non-zero colors, typically with one color region partially or fully surrounding another. The transformation replaces the "inner" color with the "outer" color, effectively filling the inner region with the color of the surrounding region. The background color (0) remains unchanged. The key is identifying which non-zero color is "inner" (doesn't touch the background) and which is "outer" (touches the background).

*   **YAML Facts:**
    
```yaml
    objects:
      - grid:
          description: A 2D array of integer values representing colors.
          properties:
            - dimensions: rows and columns.
            - cells: individual elements with color values.
      - cell:
          description: An element within the grid at a specific row and column.
          properties:
            - coordinates: (row, column).
            - color: integer value.
      - color_region:
          description: A connected area of cells sharing the same non-zero color.
          properties:
            - color_value: The integer color of the region.
            - touches_background: Boolean flag indicating if any cell in the region is adjacent (up, down, left, right) to a cell with color 0.
    relationships:
      - adjacency: Cells can be adjacent horizontally or vertically.
      - containment: One color region might border or surround another.
    actions:
      - identify_colors: Find all unique non-zero colors in the input grid.
      - check_background_adjacency: For each non-zero color, determine if any cell of that color is adjacent to a background cell (color 0).
      - classify_colors:
          - inner_color: The non-zero color that does NOT touch the background (0).
          - outer_color: The non-zero color that DOES touch the background (0).
      - transform_grid: Create the output grid by replacing all cells with the inner_color with the outer_color, keeping all other cells (outer_color and background) the same.
    ```


*   **Natural Language Program:**
    1.  Identify all unique non-zero integer values (colors) present in the input grid.
    2.  For each unique non-zero color, determine if any cell containing this color is directly adjacent (horizontally or vertically) to a cell with the value 0 (background).
    3.  Designate the unique non-zero color whose cells are *never* adjacent to the background (0) as the `inner_color`.
    4.  Designate the unique non-zero color whose cells *are* adjacent to the background (0) as the `outer_color`.
    5.  Construct the output grid by iterating through each cell of the input grid:
        *   If the input cell's color is the `inner_color`, set the corresponding output cell's color to the `outer_color`.
        *   Otherwise (if the input cell's color is the `outer_color` or 0), keep the original color for the corresponding output cell.
```python
import numpy as np

"""
Identify the unique non-zero colors in the input grid. Determine which color region is entirely surrounded by another non-zero color region (the 'inner_color') and which color region touches the background (0) (the 'outer_color'). Transform the grid by replacing all cells of the 'inner_color' with the 'outer_color', leaving the 'outer_color' and background cells unchanged.
"""

def get_neighbors(grid, r, c):
    """Gets the coordinates of the 4 cardinal neighbors of a cell."""
    neighbors = []
    rows, cols = grid.shape
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def find_non_zero_colors(grid):
    """Finds all unique non-zero colors in the grid."""
    return np.unique(grid[grid != 0])

def transform(input_grid):
    """
    Transforms the input grid based on inner/outer color region replacement.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    # Initialize output grid as a copy of the input
    output_grid = grid.copy()

    # Find all unique non-zero colors
    colors = find_non_zero_colors(grid)

    # If there are fewer than two non-zero colors, no transformation is needed
    # (or the logic doesn't apply as described)
    if len(colors) < 2:
        return output_grid.tolist() 

    inner_color = -1 # Use -1 to indicate not found yet
    outer_color = -1

    # Iterate through each unique non-zero color to classify it
    for color in colors:
        touches_background = False
        # Get coordinates of all cells with the current color
        color_coords = np.argwhere(grid == color)
        
        # Check if any cell of this color is adjacent to the background (0)
        for r, c in color_coords:
            neighbors_coords = get_neighbors(grid, r, c)
            for nr, nc in neighbors_coords:
                if grid[nr, nc] == 0:
                    touches_background = True
                    break # No need to check other neighbors for this cell
            if touches_background:
                break # No need to check other cells of this color

        # Classify the color based on background adjacency
        if touches_background:
            outer_color = color
        else:
            inner_color = color

    # Apply the transformation: replace inner_color with outer_color
    # This check handles cases where the logic might misidentify or if only one color exists
    if inner_color != -1 and outer_color != -1:
        output_grid[grid == inner_color] = outer_color
    # If only one color was found, it must be the 'outer' one touching the background,
    # so no change is needed from the initial copy. The case len(colors) < 2 handles 0 or 1 color.
    # If two colors were found but one wasn't classified (e.g., both touch background),
    # the original logic doesn't perfectly fit, but we default to no change.

    # Convert output grid back to list of lists
    return output_grid.tolist()
```
