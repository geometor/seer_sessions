
## train_1

**input:**
```
0 0 0 0 0
4 4 7 0 0
4 4 4 0 0
4 4 4 0 0
0 0 0 0 0
```


**output:**
```
0 4 4 4 0
0 4 4 4 0
0 4 4 4 0
0 0 0 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
4 7 4 0 0
4 4 4 0 0
4 4 4 0 0
```


**output:**
```
0 0 0 0 0
4 4 4 0 0
4 4 4 0 0
4 4 4 0 0
0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0
0 4 4 4 0
0 4 4 4 0
0 4 4 7 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 4 4 4
0 0 4 4 4
0 0 4 4 4
```

*   **Perception:** The task involves transforming a 2D grid based on the location of a specific marker value (7). The input grid contains a background value (0), some structure elements (4), and a single marker (7). The output grid retains the dimensions of the input but replaces the original content. It consists of the background value (0) and a 3x3 square filled with a specific value (4). The key insight is that the position of the number 7 in the input grid determines the center position of the 3x3 square of 4s in the output grid. The original arrangement of 4s in the input is ignored in the output construction.

*   **Facts:**
    
```yaml
    task_elements:
      - element: grid
        properties:
          - type: 2D array
          - dimensions: variable (consistent between input and output per example, e.g., 5x5)
          - cell_values: integers
      - element: cell_value
        variants:
          - value: 0
            role: background
          - value: 4
            role:
              - input: structural_element (ignored for output construction)
              - output: fill_value_for_square
          - value: 7
            role: marker
            properties:
              - uniqueness: appears exactly once in the input
              - function: defines the center coordinates for the output square
    actions:
      - action: locate_marker
        input: input_grid
        marker_value: 7
        output: coordinates (row, column) of the marker
      - action: create_output_grid
        properties:
          - dimensions: same as input_grid
          - initial_fill_value: 0 (background)
      - action: draw_square
        target_grid: output_grid
        center_coordinates: coordinates from locate_marker action
        size: 3x3
        fill_value: 4
    relationships:
      - type: positional_mapping
        source: location of value 7 in input_grid
        target: center of the 3x3 square of value 4 in output_grid
      - type: content_replacement
        description: The original content of the input grid (except for the location of 7) is disregarded when creating the output. The output is constructed anew based on the marker location.
    constraints:
      - The marker (7) is always present exactly once in the input.
      - The 3x3 square is drawn centered at the marker's location, potentially clipped by the grid boundaries if the marker is near an edge.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filling it entirely with the background value (0).
    2.  Scan the input grid to find the row and column coordinates of the cell containing the marker value (7).
    3.  Determine the top-left corner coordinates for a 3x3 square centered at the found marker coordinates. This is (marker_row - 1, marker_col - 1).
    4.  Iterate through the 3x3 area defined by the top-left corner: for rows from `marker_row - 1` to `marker_row + 1` and for columns from `marker_col - 1` to `marker_col + 1`.
    5.  For each cell within this 3x3 area, check if its coordinates are within the valid bounds of the output grid.
    6.  If the coordinates are valid (within the grid dimensions), set the value of the corresponding cell in the output grid to the fill value (4).
    7.  Return the completed output grid.
