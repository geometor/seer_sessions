
## train_1

**input:**
```
7 7 7 7 7 6 7 4 7 7 7
7 7 7 7 7 6 7 4 4 4 7
7 7 7 7 7 6 7 7 7 4 7
7 2 2 2 7 6 7 7 7 4 7
7 7 2 7 7 6 7 7 7 4 7
6 6 6 6 6 6 6 6 6 6 6
7 7 7 1 7 6 7 7 3 7 7
7 1 1 1 7 6 7 3 3 7 7
7 1 1 1 7 6 7 3 7 7 7
7 1 1 1 7 6 7 3 7 7 7
7 7 7 7 7 6 7 3 7 7 7
```


**output:**
```
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
7 2 2 2 7
7 7 2 7 7
6 6 6 6 6
7 7 3 7 7
7 3 3 7 7
7 3 7 7 7
7 3 7 7 7
7 3 7 7 7
6 6 6 6 6
7 4 7 7 7
7 4 4 4 7
7 7 7 4 7
7 7 7 4 7
7 7 7 4 7
6 6 6 6 6
7 7 7 1 7
7 1 1 1 7
7 1 1 1 7
7 1 1 1 7
7 7 7 7 7
```


## train_2

**input:**
```
7 7 7 7 7
7 7 8 8 7
7 7 8 8 7
8 8 8 7 7
7 7 7 7 7
6 6 6 6 6
7 7 7 7 7
2 2 2 7 7
7 7 2 2 7
7 7 7 2 2
7 7 7 7 7
6 6 6 6 6
7 7 7 7 7
7 9 7 9 9
7 9 9 9 7
7 9 7 7 7
7 7 7 7 7
```


**output:**
```
7 7 7 7 7 6 7 7 7 7 7 6 7 7 7 7 7
7 9 7 9 9 6 2 2 2 7 7 6 7 7 8 8 7
7 9 9 9 7 6 7 7 2 2 7 6 7 7 8 8 7
7 9 7 7 7 6 7 7 7 2 2 6 8 8 8 7 7
7 7 7 7 7 6 7 7 7 7 7 6 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 6 7 7 1 7 7 6 7 7 9 7 7
7 8 8 8 7 6 7 7 1 7 7 6 7 9 9 9 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
7 7 8 7 7 6 7 7 1 7 7 6 7 7 7 7 7
```


**output:**
```
7 7 7 7 7
7 8 8 8 7
7 7 8 7 7
7 7 8 7 7
7 7 8 7 7
6 6 6 6 6
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
7 7 1 7 7
6 6 6 6 6
7 7 9 7 7
7 9 9 9 7
7 7 7 7 7
7 7 7 7 7
7 7 7 7 7
```

*   **Perception:** The input grids are divided into distinct rectangular panels by single rows or columns of magenta (6) pixels. The task involves extracting these panels and rearranging them into a new grid, either stacked vertically or concatenated horizontally, with magenta separators placed between the rearranged panels. The specific arrangement (vertical vs. horizontal) and the order of panels depend on the orientation of the separators in the input grid.

*   **Facts:**
    
```yaml
    task_type: grid_rearrangement
    input_features:
      - grid: 2D array of integers (colors)
      - separators:
          - color: magenta (6)
          - type: complete single rows or complete single columns
          - function: divide the grid into panels
      - panels:
          - definition: rectangular subgrids bounded by separators or grid edges
          - content: typically contain a shape made of a specific color surrounded by a background color (orange, 7)
          - identification: extracted based on separator locations
    output_features:
      - grid: 2D array of integers (colors)
      - structure: composition of input panels rearranged
      - arrangement:
          - panels are either stacked vertically or concatenated horizontally
          - determined by separator orientation in the input
      - separators_in_output:
          - single row or column of magenta (6) placed between adjacent rearranged panels
      - panel_order:
          - depends on input separator orientation and arrangement type
    transformation_logic:
      - step_1: identify separator rows and columns (all magenta)
      - step_2: extract panels based on separator locations
      - step_3: determine output arrangement:
          - if only horizontal separators: horizontal concatenation
          - if only vertical separators: vertical stacking
          - if both horizontal and vertical separators: vertical stacking
      - step_4: determine panel order:
          - for vertical stacking: order panels top-to-bottom, then left-to-right from input
          - for horizontal concatenation: order panels top-to-bottom from input, then reverse this order for output
      - step_5: construct the output grid by placing panels in the determined order and arrangement, inserting magenta separators between them
    ```


*   **Natural Language Program:**
    1.  Identify all full rows and full columns in the input grid that consist entirely of the magenta color (6). These are the separators.
    2.  Use the coordinates of the separator rows and columns to define and extract the rectangular panels from the input grid. Panels are the areas between separators or between a separator and the grid boundary.
    3.  Determine the output arrangement based on the orientation of the separators found in step 1:
        *   If only horizontal separator rows were found, the panels will be arranged horizontally in the output.
        *   If only vertical separator columns were found, the panels will be arranged vertically in the output.
        *   If both horizontal rows and vertical columns were found as separators, the panels will be arranged vertically in the output.
    4.  Determine the order of the panels for the output arrangement:
        *   If arranging vertically: Order the panels based on their top-left corner's position in the input grid, first by row index (top-to-bottom), then by column index (left-to-right).
        *   If arranging horizontally: Order the panels based on their top-left corner's position in the input grid, first by row index (top-to-bottom), then by column index (left-to-right). Then, reverse this sequence of panels.
    5.  Construct the output grid:
        *   If arranging vertically: Stack the ordered panels one below the other, inserting a single row of magenta pixels between each adjacent pair of panels. The width of the output grid will match the width of the panels.
        *   If arranging horizontally: Concatenate the ordered panels side-by-side, inserting a single column of magenta pixels between each adjacent pair of panels. The height of the output grid will match the height of the panels.
