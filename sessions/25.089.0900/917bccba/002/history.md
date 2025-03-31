
## train_1

**input:**
```
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0
0 0 1 0 0 8 0 0 1 0 0 0
0 0 1 0 0 8 0 0 1 0 0 0
8 8 1 8 8 8 8 8 1 8 8 8
0 0 1 0 0 8 0 0 1 0 0 0
0 0 1 0 0 8 0 0 1 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
8 8 1 1 1 1 1 1 1 8 8 8
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
```


## train_2

**input:**
```
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0
0 0 2 0 3 0 0 2 0 0 0 0
0 0 2 0 3 0 0 2 0 0 0 0
3 3 2 3 3 3 3 2 3 3 3 3
0 0 2 0 3 0 0 2 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
3 3 2 2 2 2 2 2 3 3 3 3
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 3 0 4 0 3 0 0 0
4 4 4 4 3 4 4 4 3 4 4 4
0 0 0 0 3 0 4 0 3 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
4 4 4 4 3 3 3 3 3 4 4 4
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
```

Okay, let's analyze the provided examples for this ARC task.

## Perception of Task Elements

1.  **Grid Structure:** All examples use a 12x12 grid. The background is consistently white (0).
2.  **Colors:** Each example uses exactly two non-background colors. Let's call them C1 and C2.
    *   Train 1: C1=Blue(1), C2=Azure(8)
    *   Train 2: C1=Red(2), C2=Green(3)
    *   Train 3: C1=Green(3), C2=Yellow(4)
3.  **Objects/Shapes:**
    *   There's a central H-like or I-like structure composed of both C1 and C2. C1 forms the main "posts" and parts of the crossbar, while C2 forms a central vertical line segment within the structure and part of the crossbar.
    *   There are vertical lines composed solely of C2 located outside the central structure, aligned vertically with the C2 segment inside the structure.
    *   In train 1 and 3, the crossbar of the H-shape also extends horizontally beyond the main structure using color C2. In train 2, it seems C2 also forms the ends of the crossbar.
4.  **Transformation Pattern:**
    *   **Internal C2 Removal:** The C2 pixels forming the vertical segment *inside* the H-structure are removed (changed to white 0).
    *   **External C2 Line Movement:** The vertical lines of C2 outside the structure are moved horizontally. They appear to move to the column corresponding to the rightmost edge of the H-structure. The original column of these lines is cleared (changed to white 0).
    *   **Crossbar Transformation:** The horizontal crossbar undergoes a significant change. The segment of the crossbar *between* (and including) the C1 vertical posts of the H-structure is changed entirely to color C1. The parts of the crossbar extending *outside* these C1 posts retain their original color (which is C2).

## YAML Fact Sheet


```yaml
task_context:
  grid_size: [12, 12]
  background_color: 0 # white
  num_distinct_colors_per_example: 3 # background + 2 foreground colors

objects:
  - id: H_structure
    description: A central H-like shape composed of two colors, C1 and C2.
    properties:
      color_1: C1 # Forms vertical posts and part of the crossbar
      color_2: C2 # Forms internal vertical line and part of the crossbar
      bounding_box: Defines the spatial extent.
      crossbar_row: The row index containing the horizontal bar.
      left_post_col: Column index of the leftmost C1 segment defining the H structure on the crossbar row.
      right_post_col: Column index of the rightmost C1 segment defining the H structure on the crossbar row.
      right_edge_col: Column index of the rightmost extent of the H structure's bounding box.

  - id: external_lines
    description: Vertical lines outside the H_structure, composed solely of C2.
    properties:
      color: C2
      column_index: The original column where these lines appear.
      vertical_extent: The rows these lines occupy.

relationships:
  - C2 is present both inside the H_structure (vertical line, crossbar) and as external_lines.
  - external_lines are vertically aligned with the internal C2 vertical line segment.

actions:
  - action: clear_internal_vertical_C2
    object: H_structure
    details: Change pixels of color C2 within the H_structure's bounding box to background_color (0), *except* for those on the crossbar_row.
  - action: modify_crossbar
    object: H_structure
    details: >
      Iterate through the crossbar_row. For columns between left_post_col and right_post_col (inclusive),
      change the pixel color to C1. Pixels outside this column range retain their original color.
  - action: move_external_lines
    object: external_lines
    details: >
      Change the original external_lines pixels to background_color (0).
      Draw new vertical lines of color C2 at the column index defined by H_structure.right_edge_col,
      maintaining the original vertical_extent.

```


## Natural Language Program

1.  Identify the background color (white, 0) and the two foreground colors, C1 and C2. C2 is distinguishable as the color appearing both within the central structure's vertical axis and as separate external vertical lines. C1 forms the main 'posts' of the central H-like structure.
2.  Locate the central H-like structure composed of C1 and C2. Determine its bounding box, the row index of its horizontal crossbar (`crossbar_row`), the column index of the leftmost C1 pixel on the crossbar (`left_post_col`), the column index of the rightmost C1 pixel on the crossbar (`right_post_col`), and the column index of the overall rightmost extent of the structure (`right_edge_col`).
3.  Locate the external vertical lines composed solely of C2. Note their original column index (`external_line_col`) and their row indices (`external_line_rows`).
4.  Initialize the output grid as a copy of the input grid.
5.  Iterate through the input grid pixels *within* the H-structure's bounding box: If a pixel's color is C2 and its row index is *not* `crossbar_row`, change the corresponding pixel in the output grid to the background color (0).
6.  Iterate through the `external_line_rows`: Change the pixel at (`row`, `external_line_col`) in the output grid to the background color (0). Then, change the pixel at (`row`, `right_edge_col`) in the output grid to C2.
7.  Iterate through the columns (`c`) of the `crossbar_row` in the output grid:
    *   If `c` is between `left_post_col` and `right_post_col` (inclusive), set the pixel color at (`crossbar_row`, `c`) to C1.
    *   Otherwise (if `c` is less than `left_post_col` or greater than `right_post_col`), the pixel at (`crossbar_row`, `c`) retains its original color from the input grid.
8.  Return the modified output grid.
```python
import numpy as np
from typing import List, Tuple, Dict, Set

def find_colors(grid: np.ndarray) -> Tuple[int, int, int]:
    """
    Identifies the background color (0) and the two foreground colors (C1, C2).

    C2 is identified as the color forming vertical lines in columns containing
    only C2 and the background color. C1 is the other non-background color.

    Returns:
        Tuple[int, int, int]: (background_color, C1, C2)
    """
    unique_colors = np.unique(grid)
    background_color = 0
    foreground_colors = sorted([c for c in unique_colors if c != background_color])

    if len(foreground_colors) != 2:
        # Fallback or error handling if assumption of 2 foreground colors fails
        # For now, let's assume the first is C1, second is C2 if possible
        if len(foreground_colors) == 1:
             return background_color, foreground_colors[0], foreground_colors[0] # Handle edge case?
        elif len(foreground_colors) > 1:
             # Default assumption if identification fails
             print("Warning: Could not reliably identify C1 and C2 based on external lines. Assuming C1={}, C2={}".format(foreground_colors[0], foreground_colors[1]))
             return background_color, foreground_colors[0], foreground_colors[1]
        else:
             raise ValueError("No foreground colors found.")


    C1, C2 = -1, -1

    rows, cols = grid.shape
    for c_idx in range(cols):
        col_data = grid[:, c_idx]
        unique_in_col = np.unique(col_data)
        non_bg_in_col = [c for c in unique_in_col if c != background_color]

        # Check if this column contains only background and ONE foreground color
        if len(non_bg_in_col) == 1:
            potential_c2 = non_bg_in_col[0]
            # Check if this color exists elsewhere with the other foreground color
            other_fg_color = -1
            for fg in foreground_colors:
                if fg != potential_c2:
                    other_fg_color = fg
                    break

            # Does the other foreground color exist in the grid?
            if other_fg_color != -1 and np.any(grid == other_fg_color):
                 # Is potential_c2 truly isolated in this column?
                 # A simple check: if the column consists *only* of 0s and potential_c2
                 is_isolated_col = True
                 for val in unique_in_col:
                     if val != 0 and val != potential_c2:
                         is_isolated_col = False
                         break
                 if is_isolated_col:
                    # Found C2 based on isolated vertical line characteristic
                    C2 = potential_c2
                    C1 = other_fg_color
                    break # Found C1 and C2

    # If the above logic failed (e.g., no perfectly isolated column)
    if C1 == -1 or C2 == -1:
        # Fallback: Use the sorted order. This might be wrong if C1 < C2.
        # A better fallback might be needed based on other structural properties.
         print("Warning: Fallback color identification used. Assuming C1={}, C2={}".format(foreground_colors[0], foreground_colors[1]))
         C1 = foreground_colors[0]
         C2 = foreground_colors[1]


    return background_color, C1, C2

def find_structure_properties(grid: np.ndarray, C1: int, C2: int, background_color: int) -> Dict:
    """
    Finds key properties of the H-like structure and external lines.
    """
    properties = {}
    rows, cols = grid.shape

    # Find crossbar row (assuming it's the row containing C1)
    c1_rows, _ = np.where(grid == C1)
    if not len(c1_rows):
         raise ValueError("Cannot find C1 in the grid.")
    properties['crossbar_row'] = c1_rows[0] # Assume first row with C1 is the crossbar

    # Find C1 post columns on the crossbar
    crossbar_data = grid[properties['crossbar_row'], :]
    c1_cols_on_crossbar = np.where(crossbar_data == C1)[0]
    if not len(c1_cols_on_crossbar):
         # This might happen if C1 is not on the identified 'crossbar' based on first occurrence.
         # Re-evaluate crossbar finding or handle error.
         # Let's search all rows for C1 to define posts, assuming H structure
         all_c1_rows, all_c1_cols = np.where(grid == C1)
         if not len(all_c1_cols): raise ValueError("C1 not found")
         # Assume crossbar is where C1 has min/max column extent
         properties['left_post_col'] = np.min(all_c1_cols)
         properties['right_post_col'] = np.max(all_c1_cols)
         # Need to redefine crossbar row potentially based on where C2 connects these?
         # For now, stick to the first C1 row found. Revisit if needed.
         print(f"Warning: C1 not found on initial crossbar row guess ({properties['crossbar_row']}). Using overall min/max C1 columns.")
         properties['left_post_col'] = np.min(c1_cols_on_crossbar) if len(c1_cols_on_crossbar) else 0 # Needs better handling
         properties['right_post_col'] = np.max(c1_cols_on_crossbar) if len(c1_cols_on_crossbar) else cols -1# Needs better handling
    else:
        properties['left_post_col'] = np.min(c1_cols_on_crossbar)
        properties['right_post_col'] = np.max(c1_cols_on_crossbar)


    # Find right edge of the structure on the crossbar row
    non_bg_cols_on_crossbar = np.where(crossbar_data != background_color)[0]
    properties['right_edge_col'] = np.max(non_bg_cols_on_crossbar) if len(non_bg_cols_on_crossbar) > 0 else properties['right_post_col']

    # Find external C2 lines column and rows
    properties['external_line_col'] = -1
    properties['external_line_rows'] = []
    for c_idx in range(cols):
        col_data = grid[:, c_idx]
        unique_in_col = np.unique(col_data)
        # Check if this column contains ONLY C2 and background
        if all(uc == C2 or uc == background_color for uc in unique_in_col) and C2 in unique_in_col:
             # Check if this C2 column is truly separate (not touching C1 maybe?)
             # For simplicity, assume the first such column found is it.
             # A more robust check might involve connectivity analysis.
             is_external = True
             # Rough check: ensure C1 is not adjacent horizontally
             if c_idx > 0 and np.any(grid[:, c_idx-1] == C1): is_external = False
             if c_idx < cols - 1 and np.any(grid[:, c_idx+1] == C1): is_external = False
             # Rough check: ensure it's not the central C2 line (often shares column with C1/C2 on crossbar)
             if grid[properties['crossbar_row'], c_idx] != background_color:
                 is_external = False # If part of the crossbar structure, likely not external

             # A simpler primary assumption: The column identified during C1/C2 distinction is the external one.
             # Let's refine the C1/C2 identification step to return this column.

             # Re-evaluating external line finding:
             # Find all C2 locations
             c2_rows, c2_cols = np.where(grid == C2)
             c2_coords = set(zip(c2_rows, c2_cols))

             # Find all C1 locations
             c1_rows_all, c1_cols_all = np.where(grid == C1)
             c1_coords = set(zip(c1_rows_all, c1_cols_all))

             # Find connected components of C1 and C2 together
             q = list(c1_coords) # Start BFS/DFS from C1 pixels
             main_structure_coords = set(c1_coords)
             visited = set(c1_coords)

             while q:
                 r, c = q.pop(0)
                 for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-way connectivity
                     nr, nc = r + dr, c + dc
                     if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                          coord = (nr, nc)
                          # If neighbor is C1 or C2, add to structure
                          if grid[nr, nc] == C1 or grid[nr, nc] == C2:
                              if coord not in main_structure_coords:
                                  main_structure_coords.add(coord)
                                  q.append(coord)
                          visited.add(coord) # Mark visited even if background

             # External C2 coords are those C2 coords not in the main structure
             external_c2_coords = c2_coords - main_structure_coords

             if external_c2_coords:
                 # Assume all external C2 pixels are in the same column
                 properties['external_line_col'] = list(external_c2_coords)[0][1]
                 properties['external_line_rows'] = sorted([r for r, c in external_c2_coords])
             else:
                 # No external lines found
                 properties['external_line_col'] = -1
                 properties['external_line_rows'] = []
                 print("Warning: No external C2 lines identified.")


    # Find internal C2 column (the one part of the H structure, not external)
    properties['internal_c2_col'] = -1
    internal_c2_candidates = []
    for c_idx in range(cols):
        # Must contain C2
        if np.any(grid[:, c_idx] == C2):
             # Must not be the external line column
             if c_idx != properties['external_line_col']:
                 # Must have C2 pixels NOT on the crossbar row
                 if np.any(grid[grid[:, c_idx] == C2, c_idx] != properties['crossbar_row']):
                     # Check if this column is part of the main structure found via BFS
                     col_coords = set([(r, c_idx) for r in range(rows)])
                     if any(coord in main_structure_coords for coord in col_coords if grid[coord[0], coord[1]] == C2):
                          internal_c2_candidates.append(c_idx)


    if len(internal_c2_candidates) == 1:
         properties['internal_c2_col'] = internal_c2_candidates[0]
    elif len(internal_c2_candidates) > 1:
        # Ambiguous - pick the one closest to the center? Or the one on the crossbar?
        # Let's pick the one present on the crossbar row.
        for c_idx in internal_c2_candidates:
            if grid[properties['crossbar_row'], c_idx] == C2:
                properties['internal_c2_col'] = c_idx
                break
        if properties['internal_c2_col'] == -1: # If none on crossbar, just pick first?
             properties['internal_c2_col'] = internal_c2_candidates[0]
             print(f"Warning: Multiple internal C2 column candidates. Chose {properties['internal_c2_col']}.")
    else:
        # No internal C2 line found separate from external?
        print("Warning: No internal C2 vertical line identified.")
        # This might happen if C2 is only on the crossbar, or only external


    return properties


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the observed pattern:
    1. Identifies background (0), main structure color (C1), and secondary color (C2).
    2. Locates the central H-like structure and external C2 vertical lines.
    3. Clears the internal vertical C2 line segment within the H-structure (pixels not on the crossbar).
    4. Modifies the crossbar row: colors pixels between the C1 'posts' (inclusive) with C1.
    5. Moves the external C2 vertical lines to the column corresponding to the rightmost edge of the H-structure's crossbar.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    if np.all(grid == 0): # Handle empty grid case
        return input_grid

    # 1. Identify colors
    try:
        background_color, C1, C2 = find_colors(grid)
    except ValueError as e:
        print(f"Error identifying colors: {e}. Returning input.")
        return input_grid
    except Exception as e:
        print(f"Unexpected error identifying colors: {e}. Returning input.")
        # Fallback identification needed here based on simple counts?
        unique_colors = np.unique(grid)
        foreground_colors = sorted([c for c in unique_colors if c != 0])
        if len(foreground_colors) == 2:
             C1, C2 = foreground_colors
             print(f"Fallback color ID: C1={C1}, C2={C2}")
        else:
             print("Cannot determine C1/C2 with fallback.")
             return input_grid # Cannot proceed

    # 2. Locate structure properties
    try:
        props = find_structure_properties(grid, C1, C2, background_color)
        crossbar_row = props['crossbar_row']
        left_post_col = props['left_post_col']
        right_post_col = props['right_post_col']
        right_edge_col = props['right_edge_col']
        internal_c2_col = props['internal_c2_col']
        external_line_col = props['external_line_col']
        external_line_rows = props['external_line_rows']

    except ValueError as e:
         print(f"Error finding structure properties: {e}. Returning input.")
         return input_grid
    except KeyError as e:
         print(f"Error accessing structure property: {e}. Returning input.")
         return input_grid

    # 3. Clear internal C2 vertical line (off-crossbar part)
    if internal_c2_col != -1:
        for r in range(rows):
            if r != crossbar_row and output_grid[r, internal_c2_col] == C2:
                output_grid[r, internal_c2_col] = background_color

    # 4. Modify crossbar
    # Ensure indices are valid before slicing/iteration
    if 0 <= crossbar_row < rows and 0 <= left_post_col <= right_post_col < cols:
        for c in range(left_post_col, right_post_col + 1):
            # Only change if the column is valid
            if 0 <= c < cols:
                output_grid[crossbar_row, c] = C1
    else:
        print(f"Warning: Invalid crossbar indices: row={crossbar_row}, left={left_post_col}, right={right_post_col}. Skipping modification.")


    # 5. Move external C2 lines
    if external_line_col != -1 and external_line_rows:
        # Ensure target column is valid
        if 0 <= right_edge_col < cols:
             # Clear original location
            for r in external_line_rows:
                 if 0 <= r < rows and 0 <= external_line_col < cols:
                     output_grid[r, external_line_col] = background_color
             # Draw at new location
            for r in external_line_rows:
                 if 0 <= r < rows:
                     output_grid[r, right_edge_col] = C2
        else:
            print(f"Warning: Invalid target column for external lines: {right_edge_col}. Skipping move.")


    return output_grid.tolist()
```
