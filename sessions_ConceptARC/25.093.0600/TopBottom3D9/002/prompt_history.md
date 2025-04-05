
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 0
1 1 1 3 3 3 3 1 1 1
1 1 1 3 3 3 3 1 1 1
1 1 1 3 3 3 3 1 1 1
0 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 0
0 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 0
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
0 1 1 1 1 1 1 1 1 0
0 1 1 1 1 1 1 1 1 0
0 1 1 1 1 1 1 1 1 0
0 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
2 2 4 4 4 4 4 4 4 4 4 4 2 2
2 2 2 2 0 0 0 0 0 0 2 2 2 2
2 2 2 2 0 0 0 0 0 0 2 2 2 2
2 2 2 2 0 0 0 0 0 0 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 0 0 0 0 0 0 4 4 4 4
4 4 4 4 0 0 0 0 0 0 4 4 4 4
4 4 4 4 0 0 0 0 0 0 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 6 6 0
0 0 0 6 6 6 6 6 6 6 0
0 0 0 6 6 6 6 6 6 6 0
0 0 0 6 6 6 6 6 6 6 0
0 0 0 6 6 6 6 6 6 6 0
0 0 0 6 6 6 6 8 8 8 8
0 0 0 6 6 6 6 8 8 8 8
0 0 0 6 6 6 6 8 8 8 8
0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 8 8 8 8 8 8 8 0
0 0 0 8 8 8 8 8 8 8 8
0 0 0 8 8 8 8 8 8 8 8
0 0 0 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The task operates on 2D grids of integers (colors).
    *   Each input grid contains multiple distinct non-zero integer values, representing different colored regions, plus a background color '0'.
    *   The '0' color typically forms an outer border around the non-zero colored regions.
    *   The transformation involves changing the color of some regions while leaving others (and the background) unchanged.
    *   Specifically, one non-zero color seems to "take over" or replace another non-zero color.
    *   The determining factor for which color replaces which appears related to proximity to the outer '0' border. The color that touches the '0' border persists and replaces the color(s) that do not touch the '0' border.

*   **YAML Documentation of Facts:**
    
```yaml
    task_elements:
      - object: Grid
        properties:
          - type: 2D array of integers
          - contains: Cells
          - has: background_color (usually 0)
          - has: non_zero_colors (set of integers > 0)
      - object: Cell
        properties:
          - position: (row, column)
          - value: integer (color)
      - object: ColorRegion
        properties:
          - color_value: integer > 0
          - cells: list of Cell objects with the same color_value
          - touches_background: boolean (indicates if any cell in the region is adjacent to a background_color cell)

    relationships:
      - type: adjacency
        between: Cell
        definition: Cells sharing an edge (up, down, left, right).
      - type: containment
        description: Grid contains Cells.
      - type: grouping
        description: Cells with the same non-zero value form a ColorRegion.

    actions:
      - action: identify_colors
        input: Input Grid
        output: Set of unique non-zero colors present.
      - action: identify_border_touching_color
        input: Input Grid, Set of non-zero colors
        process: For each non-zero color, check if any cell with that color is adjacent to a cell with the background color (0).
        output: The non-zero color that touches the background border. (Assumption: only one such color exists). Let's call this the 'replacement_color'.
      - action: identify_inner_colors
        input: Set of non-zero colors, replacement_color
        output: Set of non-zero colors that are not the replacement_color. Let's call these 'target_colors'.
      - action: replace_colors
        input: Input Grid, target_colors, replacement_color
        process: Create a copy of the Input Grid. Iterate through each cell. If a cell's color is in target_colors, change its value to replacement_color. Otherwise, keep the original value.
        output: Output Grid

    transformation_rule:
      goal: Modify the input grid based on color adjacency to the background border.
      steps:
        - Find all unique non-zero colors in the input grid.
        - Determine which non-zero color has at least one cell adjacent (up, down, left, right) to a cell with the background color (0). This is the 'replacement_color'.
        - Identify all other non-zero colors as 'target_colors'.
        - Create the output grid by replacing every cell containing a 'target_color' with the 'replacement_color'. Cells with the 'replacement_color' or the background color (0) remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify the set of all unique non-zero integer values (colors) present in the input grid.
    3.  Find the specific non-zero color (`replacement_color`) for which at least one cell with this color is directly adjacent (sharing an edge) to a cell with the value 0 (background).
    4.  Identify the set of all other non-zero colors (`target_colors`) present in the input grid (i.e., all non-zero colors excluding the `replacement_color`).
    5.  Iterate through each cell of the input grid.
    6.  If the current cell's color is one of the `target_colors`, change the color of the corresponding cell in the output grid to the `replacement_color`.
    7.  If the current cell's color is the `replacement_color` or the background color (0), keep its color unchanged in the output grid.
    8.  Return the modified output grid.
```python
import numpy as np

"""
Transformation Rule:
1. Identify all unique non-zero colors in the input grid.
2. Find the non-zero color that has at least one cell adjacent (up, down, left, right) 
   to a cell with the background color (0). This is the 'replacement_color'.
3. Identify all other non-zero colors as 'target_colors'.
4. Create the output grid by replacing every cell containing a 'target_color' 
   with the 'replacement_color'. Cells with the 'replacement_color' or the 
   background color (0) remain unchanged.
"""

def find_border_touching_color(grid, non_zero_colors):
    """Finds the non-zero color adjacent to the background (0)."""
    rows, cols = grid.shape
    background_color = 0
    
    # Check neighbors for each cell of each non-zero color
    for color in non_zero_colors:
        # Get coordinates of all cells with the current color
        coords = np.argwhere(grid == color)
        
        for r, c in coords:
            # Define potential neighbor offsets
            neighbor_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            
            for dr, dc in neighbor_offsets:
                nr, nc = r + dr, c + dc
                
                # Check if neighbor coordinates are within grid bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if the neighbor cell is the background color
                    if grid[nr, nc] == background_color:
                        return color # This color touches the border
                        
    # This part should ideally not be reached if the problem assumptions hold
    # (i.e., there's always one color touching the border)
    print("Warning: No border-touching color found. Returning first non-zero color.")
    return non_zero_colors[0] if non_zero_colors else None


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Identifies the color touching the '0' border and uses it to replace
    all other non-zero colors.
    """
    # Convert input list of lists to a numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(grid)
    
    # 1. Identify all unique non-zero colors
    unique_colors = np.unique(grid)
    non_zero_colors = unique_colors[unique_colors != 0].tolist()

    # Handle cases with no non-zero colors or only one non-zero color
    if not non_zero_colors:
        return output_grid.tolist() # No changes needed if no non-zero colors
    if len(non_zero_colors) == 1:
         return output_grid.tolist() # No changes needed if only one non-zero color

    # 2. Find the 'replacement_color' (the one touching the border)
    replacement_color = find_border_touching_color(grid, non_zero_colors)
    
    # 3. Identify 'target_colors' (all other non-zero colors)
    target_colors = [color for color in non_zero_colors if color != replacement_color]

    # 4. Replace 'target_colors' with 'replacement_color' in the output grid
    for target_color in target_colors:
        output_grid[output_grid == target_color] = replacement_color
        
    # Convert the result back to a list of lists if required by the environment,
    # but NumPy array is often convenient. Let's return list of lists.
    return output_grid.tolist()
```
