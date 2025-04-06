
## train_1

**input:**
```
0 0 0 4 1 0 0
0 7 0 4 0 1 1
0 0 0 4 0 1 0
4 4 4 4 4 4 4
0 0 0 4 1 1 0
0 3 0 4 0 1 0
0 0 0 4 1 1 1
4 4 4 4 4 4 4
0 0 0 4 1 1 0
0 8 0 4 0 1 1
0 0 0 4 1 0 1
```


**output:**
```
0 0 0 4 7 0 0
0 7 0 4 0 7 7
0 0 0 4 0 7 0
4 4 4 4 4 4 4
0 0 0 4 3 3 0
0 3 0 4 0 3 0
0 0 0 4 3 3 3
4 4 4 4 4 4 4
0 0 0 4 8 8 0
0 8 0 4 0 8 8
0 0 0 4 8 0 8
```


## train_2

**input:**
```
0 0 0 4 0 0 0 4 0 0 0
0 3 0 4 0 2 0 4 0 6 0
0 0 0 4 0 0 0 4 0 0 0
4 4 4 4 4 4 4 4 4 4 4
1 0 0 4 0 1 0 4 1 0 1
0 1 0 4 1 1 1 4 1 0 1
1 1 1 4 1 0 1 4 0 1 0
```


**output:**
```
0 0 0 4 0 0 0 4 0 0 0
0 3 0 4 0 2 0 4 0 6 0
0 0 0 4 0 0 0 4 0 0 0
4 4 4 4 4 4 4 4 4 4 4
3 0 0 4 0 2 0 4 6 0 6
0 3 0 4 2 2 2 4 6 0 6
3 3 3 4 2 0 2 4 0 6 0
```

Okay, let's analyze the transformation.

**Perception of Elements:**

1.  **Grid Structure:** The input and output are numerical grids.
2.  **Separators:** The number `4` acts as a separator, forming consistent horizontal and vertical lines across examples. These lines partition the grid into distinct rectangular regions or "cells".
3.  **Background:** The number `0` appears to be a background or empty value, generally remaining unchanged.
4.  **Target Number:** The number `1` appears to be a placeholder or target number that gets transformed in the output.
5.  **Color Numbers:** Other numbers (2, 3, 6, 7, 8 in the examples) act like "colors". Their key role seems to be determining the replacement value for the `1`s.
6.  **Transformation Logic:** The core transformation involves replacing the `1`s based on the "color" found in related cells, respecting the boundaries defined by the `4`s. There appears to be a priority system for determining which color source to use.

**YAML Facts:**


```yaml
Grid:
  Properties:
    - dimensions: [rows, columns]
    - contains: Numbers
    - partitioned_by: Number_4
Objects:
  - Number:
      Values: [0, 1, 2, 3, 4, 5, 6, 7, 8] # Assuming standard digits
      Roles:
        - 0: Background
        - 4: Separator
        - 1: Target (placeholder to be replaced)
        - Others (2,3,5,6,7,8): SourceColor
  - Cell:
      Definition: A rectangular region within the grid bounded by grid edges or lines of Number_4.
      Properties:
        - boundaries: [top_row, bottom_row, left_col, right_col]
        - contains: Numbers
      Relationships:
        - above: Cell (same columns, previous row section)
        - below: Cell (same columns, next row section)
        - left_of: Cell (same rows, previous column section)
        - right_of: Cell (same rows, next column section)
Actions:
  - Identify_Cells: Determine the boundaries of all cells based on Number_4 separators.
  - Find_Unique_SourceColor: Within a given Cell, find if there is exactly one unique Number that is not 0, 1, or 4.
  - Replace_Target: Change all occurrences of Number_1 within a target Cell to a specified SourceColor.
Relationships:
  - Propagation_Rule: The SourceColor used to replace Number_1 in a target Cell is determined by checking other Cells in a specific order of priority (Vertical > Horizontal).
  - Boundary_Respect: Transformations occur strictly within the boundaries of each Cell defined by Number_4. Number_4 itself is never changed.
```


**Natural Language Program:**

1.  Initialize the output grid as an identical copy of the input grid.
2.  Identify all horizontal rows and vertical columns consisting entirely of the number `4`. These act as separators.
3.  Use the separators and grid boundaries to define distinct rectangular `Cells`. Each cell is a maximal block of numbers not containing `4`. Note the row-section and column-lane index for each cell.
4.  Iterate through each `Cell` in the grid (e.g., row-section by row-section, then column-lane by column-lane within that section). Let the current cell be `TargetCell`, located at section `i` and lane `j`.
5.  Check if `TargetCell` contains any instance of the number `1`. If it does not, proceed to the next cell.
6.  If `TargetCell` contains `1`s, attempt to find a `SourceColor` to replace them:
    a.  **Vertical Priority:** Look at the `SourceCellAbove` located at section `i-1` and lane `j` (if `i > 0`). Find if `SourceCellAbove` contains exactly one unique number that is *not* `0`, `1`, or `4`. If such a unique number exists, designate it as the `PaintColor`.
    b.  **Horizontal Priority:** If no `PaintColor` was found from `SourceCellAbove` (either because `i=0` or the cell above didn't have a unique source color), look at the `SourceCellLeft` located at section `i` and lane `j-1` (if `j > 0`). Find if `SourceCellLeft` contains exactly one unique number that is *not* `0`, `1`, or `4`. If such a unique number exists, designate it as the `PaintColor`.
    c.  **(Self Check - Lower Priority, inferred):** *If no `PaintColor` was found from above or left, check within the `TargetCell` itself. Find if `TargetCell` contains exactly one unique number that is *not* `0`, `1`, or `4`. If such a unique number exists, designate it as the `PaintColor`.* (Note: This step wasn't strictly necessary for the examples but seems a logical fallback).
7.  If a `PaintColor` was successfully determined in step 6, replace *all* instances of the number `1` within the `TargetCell` in the *output grid* with the found `PaintColor`.
8.  If no `PaintColor` was determined after checking all priority sources, leave the `1`s in the `TargetCell` unchanged in the output grid.
9.  After iterating through all cells, the final output grid is complete.
```python
"""
Transforms an input grid based on the following rules:
1. Identifies horizontal rows and vertical columns entirely composed of the number 4, treating them as separators.
2. These separators divide the grid into rectangular cells.
3. For each cell containing the number 1:
    a. It first checks the cell directly above it (if one exists). If that cell contains exactly one unique number other than 0, 1, or 4, that number (the 'PaintColor') is used.
    b. If no PaintColor is found from the cell above, it checks the cell directly to its left (if one exists). If that cell contains exactly one unique number other than 0, 1, or 4, that number is used as the PaintColor.
    c. If a PaintColor is determined from either the cell above or the cell to the left, all instances of the number 1 within the current cell are replaced by the PaintColor in the output grid.
    d. If no PaintColor is found, the 1s in the current cell remain unchanged.
4. Numbers 0 and 4, and cells not containing 1, remain unchanged.
"""

import numpy as np
from typing import List, Tuple, Optional, Set

def _find_separators(grid: np.ndarray) -> Tuple[List[int], List[int]]:
    """Finds the indices of rows and columns that consist entirely of the separator value (4)."""
    rows, cols = grid.shape
    separator_rows = [r for r in range(rows) if np.all(grid[r, :] == 4)]
    separator_cols = [c for c in range(cols) if np.all(grid[:, c] == 4)]
    return separator_rows, separator_cols

def _get_cell_boundaries(grid_shape: Tuple[int, int], sep_rows: List[int], sep_cols: List[int]) -> List[Tuple[int, int, int, int]]:
    """Determines the boundaries (start_row, end_row, start_col, end_col) of each cell."""
    rows, cols = grid_shape
    cell_boundaries = []

    row_starts = [0] + [r + 1 for r in sep_rows]
    row_ends = [r for r in sep_rows] + [rows]

    col_starts = [0] + [c + 1 for c in sep_cols]
    col_ends = [c for c in sep_cols] + [cols]

    for r_start, r_end in zip(row_starts, row_ends):
        if r_start >= r_end: continue
        for c_start, c_end in zip(col_starts, col_ends):
            if c_start >= c_end: continue
            cell_boundaries.append((r_start, r_end, c_start, c_end))

    return cell_boundaries

def _get_cell_subgrid(grid: np.ndarray, boundaries: Tuple[int, int, int, int]) -> np.ndarray:
    """Extracts the subgrid corresponding to the given cell boundaries."""
    r_start, r_end, c_start, c_end = boundaries
    return grid[r_start:r_end, c_start:c_end]

def _find_unique_source_color(cell_subgrid: np.ndarray) -> Optional[int]:
    """
    Finds if a cell contains exactly one unique number other than 0, 1, or 4.
    Returns that number if found, otherwise None.
    """
    # Flatten the cell and get unique values
    unique_values = np.unique(cell_subgrid)
    # Filter out background (0), target (1), and separator (4)
    source_colors: Set[int] = {val for val in unique_values if val not in {0, 1, 4}}
    # Return the color if exactly one unique source color exists
    if len(source_colors) == 1:
        return source_colors.pop()
    return None

def _get_cell_at(row: int, col: int, cell_map: dict) -> Optional[Tuple[int, int, int, int]]:
    """Finds the cell boundaries containing the given row and col."""
    for boundaries, _ in cell_map.items():
        r_start, r_end, c_start, c_end = boundaries
        if r_start <= row < r_end and c_start <= col < c_end:
            return boundaries
    return None

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Find separator rows and columns
    sep_rows, sep_cols = _find_separators(grid)

    # Define all cell boundaries
    cell_boundaries = _get_cell_boundaries((rows, cols), sep_rows, sep_cols)

    # Create a mapping for quick lookup of boundaries given a coordinate (optional, but can optimize)
    # For simplicity here, we'll iterate and find adjacent cells as needed.

    # Iterate through each defined cell
    for r_start, r_end, c_start, c_end in cell_boundaries:
        current_cell_boundaries = (r_start, r_end, c_start, c_end)
        current_cell_subgrid = _get_cell_subgrid(grid, current_cell_boundaries)

        # Check if the current cell contains any '1's
        if 1 not in current_cell_subgrid:
            continue # Skip if no target '1's are present

        paint_color: Optional[int] = None

        # 1. Check cell directly above
        if r_start > 0:
            # Find the boundaries of the cell above (it must end just before a separator or the current cell start)
            potential_above_row_end = r_start -1 # separator is at r_start - 1
            # Find a cell whose end row matches potential_above_row_end and columns overlap
            for br, er, bc, ec in cell_boundaries:
                if er == r_start and bc < c_end and ec > c_start: # Check if cell ends exactly above and columns overlap
                    # Refine check for exact vertical alignment
                    if bc == c_start and ec == c_end:
                        cell_above_boundaries = (br, er, bc, ec)
                        cell_above_subgrid = _get_cell_subgrid(grid, cell_above_boundaries)
                        paint_color = _find_unique_source_color(cell_above_subgrid)
                        break # Found the directly above cell
            if paint_color is not None:
                 # Replace 1s in the current cell in the output grid
                 output_grid[r_start:r_end, c_start:c_end][current_cell_subgrid == 1] = paint_color
                 continue # Color found and applied, move to next cell


        # 2. Check cell directly to the left (only if color not found above)
        if paint_color is None and c_start > 0:
             # Find the boundaries of the cell left (it must end just before a separator or the current cell start)
            potential_left_col_end = c_start -1 # separator is at c_start - 1
            # Find a cell whose end col matches potential_left_col_end and rows overlap
            for br, er, bc, ec in cell_boundaries:
                 if ec == c_start and br < r_end and er > r_start: # Check if cell ends exactly left and rows overlap
                     # Refine check for exact horizontal alignment
                     if br == r_start and er == r_end:
                        cell_left_boundaries = (br, er, bc, ec)
                        cell_left_subgrid = _get_cell_subgrid(grid, cell_left_boundaries)
                        paint_color = _find_unique_source_color(cell_left_subgrid)
                        break # Found the directly left cell
            if paint_color is not None:
                 # Replace 1s in the current cell in the output grid
                 output_grid[r_start:r_end, c_start:c_end][current_cell_subgrid == 1] = paint_color
                 continue # Color found and applied, move to next cell

        # If no paint_color was found from above or left, the 1s remain unchanged (already handled by copying)

    # Convert back to list of lists for the final output
    return output_grid.tolist()
```
