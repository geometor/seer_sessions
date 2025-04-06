
## train_1

**input:**
```
7 6 6 3 7
7 7 7 4 7
7 7 7 6 7
7 7 6 6 6
7 7 7 6 7
```


**output:**
```
7 3 3 7 7
7 7 7 7 7
7 7 7 4 7
7 7 4 4 4
7 7 7 4 7
```


## train_2

**input:**
```
7 7 7 6
3 7 6 6
7 7 6 7
7 7 7 7
1 6 6 6
7 7 6 7
```


**output:**
```
7 7 7 6
7 7 6 6
7 7 6 7
7 7 7 7
7 1 1 1
7 7 1 7
```

Okay, let's analyze the transformation.

## Perception of Elements

1.  **Grid Structure:** Both input and output are 2D grids of numbers. The grid dimensions are preserved in each example (5x5 for train_1, 6x4 for train_2).
2.  **Color Palette:** The numbers likely represent colors. The dominant color is `7` (background/neutral). Color `6` appears frequently and is the primary subject of transformations. Colors `1`, `3`, and `4` act as "active" colors or sources.
3.  **Core Transformation:** The central logic revolves around how the color `6` changes based on its adjacent neighbors (up, down, left, right).
4.  **Source Color Behavior:** The active colors (`1`, `3`, `4`) seem to influence adjacent `6`s. If they successfully influence a `6`, the original source color cell turns into the background color `7`. If they are not adjacent to any `6`, they also turn into `7`.
5.  **Connected Components:** Groups of connected `6`s (sharing horizontal or vertical borders) seem to behave as a single unit when determining their transformation.
6.  **Conditional Rule for `6`:**
    *   If a component of `6`s is adjacent to exactly one unique active color (non-`6`, non-`7`), all `6`s in that component adopt that active color.
    *   If a component of `6`s is *not* adjacent to any active color (i.e., only adjacent to `7`s or other `6`s within the same component), its fate depends on whether the color `4` exists anywhere in the *input* grid:
        *   If `4` exists in the input grid (as seen in train_1), these isolated `6`s change to `4`.
        *   If `4` does *not* exist in the input grid (as seen in train_2), these isolated `6`s remain unchanged (`6`).
7.  **Background Stability:** The background color `7` generally remains unchanged, unless it replaces a source color cell (`1`, `3`, or `4`).

## YAML Facts


```yaml
task_type: grid_transformation
components:
  - object: grid
    properties:
      - type: 2D array of integers
      - preserves_dimensions: true
  - object: cell
    properties:
      - value: integer (representing color)
      - position: (row, column)
  - object: color
    properties:
      - role: background (color 7)
      - role: mutable (color 6)
      - role: source (colors 1, 3, 4)
actions:
  - action: identify_components
    target: color 6
    connectivity: 4-neighbor (horizontal/vertical)
    output: sets of coordinates for each connected component of 6s
  - action: find_neighbors
    target: component of 6s
    scope: adjacent cells (non-diagonal)
    filter: unique non-6, non-7 colors
    output: set of unique adjacent source colors
  - action: change_color
    target: cells in a component of 6s
    condition: based on adjacent source colors or global presence of color 4
    outcome: target cells adopt source color or default color (4) or remain unchanged
  - action: neutralize_source
    target: source color cells (1, 3, 4)
    condition:
      - if adjacent to a 6-component that changed color due to it
      - if not adjacent to any 6-component
    outcome: target cell value becomes 7
  - action: check_global_presence
    target: color 4
    scope: entire input grid
    output: boolean (true if color 4 exists anywhere, false otherwise)
relationships:
  - type: adjacency
    between: cells (horizontal/vertical)
  - type: membership
    between: cell (color 6) and connected component
```


## Natural Language Program

1.  Create an output grid initialized as a copy of the input grid.
2.  Identify all connected components of cells with the value `6` in the input grid, using 4-way adjacency (up, down, left, right).
3.  Determine if the color `4` exists anywhere in the input grid. Store this information (e.g., `input_contains_4`).
4.  Create a set to store the coordinates of "used" source cells (initially empty).
5.  For each identified component of `6`s:
    a.  Find all unique non-`6`, non-`7` colors that are present in cells directly adjacent (4-way) to any cell within this component. Let this set of unique adjacent source colors be `S`.
    b.  If `S` contains exactly one color, `c`:
        i.  Change the value of all cells belonging to this component to `c` in the output grid.
        ii. Find the coordinates of the source cell(s) with color `c` that were adjacent to this component and add them to the "used" source cells set.
    c.  If `S` is empty (the component is only adjacent to `7`s or other `6`s in the same component):
        i.  If `input_contains_4` is true, change the value of all cells belonging to this component to `4` in the output grid.
        ii. If `input_contains_4` is false, leave the cells in this component unchanged (they remain `6`) in the output grid.
    d.  If `S` contains more than one unique color, leave the cells in this component unchanged (`6`) in the output grid.
6.  Iterate through all cells in the input grid that contain a source color (`1`, `3`, or `4`):
    a.  If the coordinates of this cell are in the "used" source cells set, change its value to `7` in the output grid.
    b.  If the coordinates of this cell are *not* in the "used" source cells set, change its value to `7` in the output grid.
7.  The final state of the output grid represents the result of the transformation.
