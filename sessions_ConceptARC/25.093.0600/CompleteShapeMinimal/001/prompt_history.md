
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 0 0 1 0
0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0
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
0 6 0 0 6 6 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 0 0 0 0 6 0
0 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0
3 3 3 3 3 0 3 3
3 3 3 3 3 3 0 3
3 3 0 3 3 3 3 3
3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

*   **Perception:** The task operates on grids of numbers. Each grid contains a background color (0) and a primary foreground shape defined by a single non-zero digit (e.g., 1, 6, or 3). This foreground shape may contain internal 'holes' represented by the background color (0). The transformation identifies these internal holes within the main shape and fills them with the foreground color, effectively making the shape solid. The background surrounding the main shape remains unchanged.

*   **YAML:**
    
```yaml
    Elements:
      - type: Grid
        properties:
          - contains_cells: True
          - dimensions: constant (e.g., 8x8)
      - type: Cell
        properties:
          - value: digit (0-9)
          - role: background (if value is 0)
          - role: foreground (if value is non-zero)
      - type: Shape
        properties:
          - composed_of: foreground cells
          - color: dominant non-zero digit in the grid
          - may_contain: internal holes (background cells)
    Relationships:
      - Background cells can be external (connected to the grid border) or internal (enclosed by foreground cells).
      - Foreground cells form a connected or nearly connected region.
    Action:
      - Identify the dominant non-zero color (foreground color).
      - Identify all background cells (0s) that are not connected to the grid's border via a path of other background cells.
      - Change the value of these identified internal background cells to the foreground color.
    ```


*   **Natural Language Program:**
    1.  Identify the dominant non-zero digit in the input grid; this is the 'foreground color'. The digit 0 is the 'background color'.
    2.  Create a copy of the input grid to serve as the output grid.
    3.  Identify all background cells (value 0) located on the border of the grid.
    4.  Perform a flood fill (or similar connectivity analysis like Breadth-First Search or Depth-First Search) starting from these border background cells. Mark all reachable background cells as 'external'.
    5.  Iterate through every cell in the input grid.
    6.  If a cell contains the background color (0) and has *not* been marked as 'external' during the flood fill, change its value in the output grid to the identified 'foreground color'.
    7.  All other cells in the output grid retain their original values from the input grid.
    8.  Return the modified output grid.
