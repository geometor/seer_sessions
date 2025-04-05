
## train_1

**input:**
```
0 3 0 0 3
0 0 3 0 0
3 0 0 0 3
3 0 0 3 3
0 0 0 0 0
```


**output:**
```
0 3 0 0 3
0 0 3 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 3 3 3 0
3 0 0 0 0
3 0 3 0 3
3 0 3 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 3
0 0 0 0 0
0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 3
0 0 0 3 0
0 0 3 0 0
0 3 0 0 0
0 0 0 0 3
```


**output:**
```
0 0 0 0 3
0 0 0 3 0
0 0 3 0 0
0 3 0 0 0
0 0 0 0 3
```


## train_4

**input:**
```
0 3 3 3 3
0 0 3 0 3
0 0 0 0 0
0 0 3 3 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

*   **Perception of the Elements:**
    *   The inputs and outputs are 5x5 grids containing integers 0 and 3.
    *   The transformation involves selectively keeping or removing the '3's based on their spatial arrangement in the input grid.
    *   Cells containing '0' in the input generally remain '0' in the output, unless they were part of a group of '3's that gets removed.
    *   The key factor appears to be the connectivity of the '3's. '3's that are adjacent (horizontally, vertically, or diagonally) form connected components.
    *   The transformation retains only those '3's that are isolated, meaning they are not adjacent (including diagonally) to any other '3'. All other '3's (those part of components larger than one cell) are turned into '0's.

*   **Facts:**
    
```yaml
    objects:
      - grid:
          description: A 2-dimensional array (5x5) representing the input and output state.
          properties:
            - dimensions: [5, 5]
            - cell_values: [0, 3]
      - cell:
          description: An individual element within the grid.
          properties:
            - value: 0 or 3
            - position: (row, column) coordinates
            - neighbors: Adjacent cells (horizontally, vertically, and diagonally)
      - connected_component:
          description: A group of cells containing the value '3' where each cell is connected to at least one other cell in the group through horizontal, vertical, or diagonal adjacency.
          properties:
            - cells: List of cell positions belonging to the component.
            - size: The number of cells in the component.
    actions:
      - identify_components:
          description: Find all connected components of cells with value '3' in the input grid, using 8-way adjacency (including diagonals).
      - filter_components:
          description: Select components based on a specific property. In this task, the property is size.
          criteria: Keep only components where size is equal to 1.
      - generate_output:
          description: Create the output grid. Cells that were part of the kept components retain their value '3'. All other cells are set to '0'.
    relationships:
      - A cell belongs to at most one connected_component.
      - The output grid is derived from the input grid by applying the identify_components, filter_components, and generate_output actions sequentially.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid of the same dimensions as the input grid, filled with zeros.
    2.  Identify all connected components of cells containing the value '3' in the input grid. Consider cells to be connected if they are adjacent horizontally, vertically, or diagonally (8-way connectivity).
    3.  For each identified connected component:
        a.  Determine the size of the component (the number of '3's it contains).
        b.  If the size of the component is exactly 1, then locate the position of that single '3' in the input grid and set the corresponding cell in the output grid to '3'.
    4.  Return the generated output grid.
