
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
6 0 0 6 4 4 0 0 0 0 0 0
0 0 6 0 4 4 4 0 0 0 0 0
0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 0 0
0 0 0 0 3 3 7 0 0 0 0 0
0 0 0 0 3 3 0 7 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
6 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 4 4 4 6 6 0 0 0
0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 0 0
0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0 0 0
0 7 7 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 6 0 0
0 0 3 0 0 0 6 0 6 0
0 3 9 3 0 0 6 9 6 0
3 9 0 0 3 0 0 0 0 0
0 0 9 0 3 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 9 0 0 0 0 9 0 0
0 0 3 0 0 0 0 6 0 0
0 0 3 0 0 0 6 0 6 0
0 3 0 3 0 0 6 0 6 0
3 0 0 0 3 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 6 6 0 0 6 0 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 6 7 7 7 7 0 6 0 0 0
0 0 6 0 0 0 7 0 6 0 0 0
0 0 6 7 0 7 0 0 6 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 6 6 0 0 6 0 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

## Perception of Elements

The task involves transforming grids containing different non-zero integers (colors) on a zero background. The transformation operates on connected components of non-zero cells.

1.  **Objects:** The primary objects are connected components (using 8-way adjacency, i.e., edges or corners) of non-zero cells. These components can be composed of a single color or multiple colors.
2.  **Properties:** Each cell has a color (integer value). Components have properties like the set of colors they contain, their minimum color (`min_color`), their maximum color (`max_color`), and their spatial extent (bounding box, boundary cells). The interface between different colors within a component is a key property.
3.  **Transformation:** The transformation only affects components containing *more than one* distinct non-zero color. Single-color components remain unchanged.
4.  **Core Logic:** The interaction between different colors within a component drives the change. The `max_color` generally "wins" or expands, while the `min_color` or interface cells are often removed.
5.  **Removal:** Cells are removed (changed to 0). This removal primarily targets cells involved in the interface between different colors. In some cases (like Train 3), *all* cells of the `max_color` are removed. In others (like Train 2), cells of *both* colors at the interface are removed.
6.  **Propagation/Conversion:** The `max_color` often appears in new locations. This can manifest as:
    *   **Upward Propagation:** Filling empty background (0) cells vertically above the original component, specifically in columns related to removed `max_color` cells (Train 2, Train 3). This propagation seems to target the highest contiguous block of 0s located immediately below the lowest non-zero cell in that column.
    *   **Conversion:** Changing existing `min_color` cells to `max_color` cells, particularly those not directly adjacent to the original `max_color` cells (Train 1 Bottom).
    *   **Horizontal Propagation:** Filling adjacent background cells horizontally (Train 1 Top - though this seems anomalous or requires a different interpretation).

7.  **Variability:** The exact rules for removal (all max vs. interface) and propagation/conversion (upward block vs. single cell vs. conversion vs. horizontal) appear to differ between examples, possibly depending on the specific colors involved, their relative values, or the geometric configuration of the component. The most consistent pattern involves removing interface cells and upward propagation of the `max_color` into the empty block below the component's top edge in relevant columns.

## YAML Facts

```yaml
elements:
  - element: grid
    properties:
      - width: integer
      - height: integer
      - cells: list of lists of integers (colors)
      - background_color: 0
  - element: cell
    properties:
      - row: integer
      - column: integer
      - color: integer (0 for background, non-zero otherwise)
  - element: component
    description: A connected group of non-zero cells (8-way adjacency)
    properties:
      - cells: list of cell objects
      - colors: set of unique non-zero integers present
      - num_colors: count of unique non-zero colors
      - min_color: minimum color value in the component
      - max_color: maximum color value in the component
      - interface_cells: subset of cells adjacent (8-way) to another cell in the component with a different non-zero color
      - min_row: minimum row index occupied by the component

actions:
  - action: identify_components
    description: Find all connected components of non-zero cells in the input grid.
  - action: filter_components
    description: Select components with more than one unique non-zero color.
  - action: identify_interface_cells
    description: For a multi-color component, find all cells adjacent (8-way) to a cell of a different non-zero color within the same component.
  - action: remove_cells
    description: Change the color of specified cells to the background color (0).
    variants:
      - remove_interface_cells: Remove all cells identified as interface_cells.
      # - remove_max_color_cells: Remove all cells with max_color in the component. (Alternative rule seen in Train 3)
      # - remove_interface_max_cells: Remove only interface cells with max_color. (Alternative rule seen in Train 1)
  - action: propagate_color
    description: Fill certain background cells (0) with the max_color.
    variants:
      - propagate_upwards_block: >
          For columns containing removed max_color interface cells,
          find the lowest row occupied by the component in that column (min_row_col).
          Identify the contiguous block of background cells (0) ending just below min_row_col.
          Fill this block with max_color. ( Matches Train 2 Top, Train 3 if combined with different removal)
      # - propagate_upwards_single: >
      #     For columns containing removed max_color interface cells,
      #     find the lowest row occupied by the component in that column (min_row_col).
      #     If the cell directly below min_row_col is background(0), fill it with max_color. (Matches Train 2 Middle)
      # - convert_min_to_max: >
      #     Find min_color cells not adjacent to any original max_color cells and change them to max_color. (Matches Train 1 Bottom)

relationships:
  - relationship: adjacency
    description: Cells sharing an edge or corner (8-way).
  - relationship: within_component
    description: A cell belongs to a specific connected component.
  - relationship: color_interface
    description: A cell is adjacent to another cell within the same component, but they have different non-zero colors.

```

## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct connected components of non-zero cells in the input grid using 8-way adjacency.
3.  For each identified component:
    a.  Determine the set of unique non-zero colors present in the component.
    b.  If the component contains only one unique non-zero color, leave it unchanged in the output grid.
    c.  If the component contains multiple unique non-zero colors:
        i.  Find the minimum color value (`min_color`) and the maximum color value (`max_color`) present in the component.
        ii. Identify all "interface cells" within this component: these are cells that are adjacent (8-way) to at least one other cell *within the same component* that has a *different non-zero color*. Keep track of the original color of these interface cells.
        iii. Identify the subset of interface cells that originally had the `max_color` (`interface_max_cells`). Record the columns where these cells are located.
        iv. **Removal Step:** In the output grid, change the color of *all* identified interface cells (regardless of their original color) to 0 (background).
        v. **Propagation Step:** For each column `c` that contained at least one `interface_max_cell`:
            1.  Find the minimum row index (`min_row_col`) occupied by *any* non-zero cell of the original component in that column `c`.
            2.  Starting from row `r = min_row_col - 1` and going upwards (decreasing `r`): Find the contiguous block of cells `(r, c)` that have a color of 0 in the *input* grid.
            3.  If such a block exists directly below `min_row_col`, change the color of all cells in this block to `max_color` in the *output* grid.
4.  Return the modified output grid.

*Self-Correction/Refinement during thought process:* Initial hypotheses involving removing only max-color cells, or converting min-color cells, or different propagation rules (single cell, horizontal) were considered. The chosen program (based primarily on Train 2 Top) involves removing *all* interface cells and propagating the max color into the empty block just below the component's minimum row in relevant columns. This seems to be the most frequent pattern, although it doesn't perfectly replicate every detail of all examples (specifically Train 1 variations, Train 2 Middle's single-cell propagation, and Train 3's 'remove all max' behavior). It represents a plausible generalization capturing key aspects of the transformation.
```python
import copy
import collections

"""
Processes a grid of integers based on connected components of non-zero cells.

1. Identifies connected components (8-way adjacency) of non-zero cells.
2. For components containing multiple distinct non-zero colors:
   a. Finds the minimum (min_color) and maximum (max_color) colors within the component.
   b. Identifies "interface cells": cells within the component adjacent (8-way) to another cell of a different non-zero color within the same component.
   c. Identifies interface cells that have the max_color and notes their columns.
   d. Removes (sets to 0) all interface cells in the output grid.
   e. For each column that contained a max_color interface cell:
      i. Finds the minimum row index (min_row_col) of the original component in that column.
      ii. Identifies the contiguous block of background cells (0) in the input grid directly above the component's top edge in that column (i.e., ending at row min_row_col - 1).
      iii. Fills this block with the max_color in the output grid.
3. Components with only a single non-zero color remain unchanged.
"""

def get_neighbors(r, c, rows, cols):
    """ Helper function to get 8-way neighbors within grid bounds. """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def find_components(grid: list[list[int]]) -> list[tuple[set[tuple[int, int]], set[int]]]:
    """
    Finds all connected components of non-zero cells using BFS.

    Args:
        grid: The input grid.

    Returns:
        A list of tuples, where each tuple contains:
        - A set of (row, col) coordinates belonging to the component.
        - A set of unique non-zero colors present in the component.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = set()
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                component_cells = set()
                component_colors = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    component_cells.add((curr_r, curr_c))
                    component_colors.add(grid[curr_r][curr_c])

                    for nr, nc in get_neighbors(curr_r, curr_c, rows, cols):
                        if grid[nr][nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

                components.append((component_cells, component_colors))
    return components

def find_interface_cells(grid: list[list[int]], component_cells: set[tuple[int, int]]) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    """
    Identifies interface cells within a component.

    Args:
        grid: The input grid.
        component_cells: Set of (row, col) coordinates for the component.

    Returns:
        A tuple containing:
        - A set of (row, col) coordinates of all interface cells.
        - A set of (row, col) coordinates of interface cells with the max_color.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    interface_cells = set()
    
    component_data = {cell: grid[cell[0]][cell[1]] for cell in component_cells}
    
    for r, c in component_cells:
        cell_color = component_data[(r, c)]
        is_interface = False
        for nr, nc in get_neighbors(r, c, rows, cols):
            if (nr, nc) in component_data: # Check if neighbor is in the same component
                neighbor_color = component_data[(nr, nc)]
                if neighbor_color != 0 and neighbor_color != cell_color:
                    is_interface = True
                    break
        if is_interface:
            interface_cells.add((r, c))
            
    return interface_cells


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on multi-color component interactions.
    """
    # initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # Find all connected components
    components = find_components(input_grid)

    # Process each component
    for component_cells, component_colors in components:
        # Skip components with only one color (or background only, though find_components shouldn't return those)
        if len(component_colors) <= 1:
            continue

        # Calculate min and max color for the multi-color component
        min_color = min(component_colors)
        max_color = max(component_colors)
        
        # Find interface cells within this component
        interface_cells = find_interface_cells(input_grid, component_cells)

        # Identify interface cells with max_color and their columns
        interface_max_cells = set()
        propagate_cols = set()
        for r_int, c_int in interface_cells:
            if input_grid[r_int][c_int] == max_color:
                interface_max_cells.add((r_int, c_int))
                propagate_cols.add(c_int)

        # Removal Step: Set all interface cells to 0 in the output grid
        for r_int, c_int in interface_cells:
            output_grid[r_int][c_int] = 0

        # Propagation Step:
        for c_prop in propagate_cols:
            # Find the minimum row for this component in this column
            min_row_col = rows # Initialize higher than possible
            for r_comp, c_comp in component_cells:
                if c_comp == c_prop:
                    min_row_col = min(min_row_col, r_comp)
            
            # If no component cell was found in this column (shouldn't happen if it's in propagate_cols, but safety check)
            if min_row_col == rows:
                continue 

            # Trace upwards from min_row_col - 1 in the *input* grid to find the block of 0s
            fill_cells = []
            r_trace = min_row_col - 1
            while r_trace >= 0 and input_grid[r_trace][c_prop] == 0:
                fill_cells.append((r_trace, c_prop))
                r_trace -= 1
            
            # Fill the identified block in the *output* grid with max_color
            for r_fill, c_fill in fill_cells:
                 output_grid[r_fill][c_fill] = max_color


    return output_grid
```
