
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 1 1 1
2 2 2 0 0 0 0 0 1 1 1
2 2 2 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 3 0 0 0 4 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 3 0 0 0 4 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 3 0 3 0 0 0 0 0 0 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 3 0 0 0 0 0 0 0 0 0 4 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 3 0 3 0 0 0 0 0 0 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The input consists of a 2D grid containing mostly zeros and some distinct groups of non-zero numbers. The output is a grid of the same dimensions where these non-zero groups have been moved horizontally. Groups initially located on the left side of the grid are moved to the leftmost columns, and groups initially on the right side are moved to the rightmost columns, while maintaining their relative internal structure and vertical position.

*   **YAML Facts:**
    
```yaml
    task_description: "Horizontally shift groups of non-zero numbers to the grid edges based on their initial horizontal position."
    elements:
      - element: grid
        properties:
          - type: 2D array of integers
          - contains: background (0) and objects (non-zero integers)
      - element: object
        properties:
          - definition: collection of cells with the same non-zero value
          - value: a specific integer > 0
          - position: defined by the set of coordinates (row, column) it occupies
          - bounding_box: minimum/maximum row and column indices
          - horizontal_center: average of minimum and maximum column index
    actions:
      - action: identify_objects
        input: input grid
        output: list of unique non-zero values and their corresponding coordinates
      - action: calculate_grid_center
        input: grid width
        output: horizontal center column index
      - action: determine_shift_direction
        input: object horizontal center, grid center
        output: direction ('left' or 'right')
      - action: calculate_shift_amount
        input: object bounding box, grid width, shift direction
        output: horizontal shift value (integer offset)
      - action: apply_shift
        input: object coordinates, shift amount
        output: new object coordinates
      - action: construct_output_grid
        input: grid dimensions, shifted object coordinates and values
        output: output grid
    relationships:
      - relationship: object_position_determines_destination
        description: "Objects whose horizontal center is less than or equal to the grid's horizontal center move left; otherwise, they move right."
      - relationship: shift_maintains_relative_structure
        description: "The relative positions of cells within an object remain unchanged after the horizontal shift."
      - relationship: shift_maintains_vertical_position
        description: "The row indices of all cells within an object remain unchanged after the horizontal shift."
    transformations:
      - transformation: move_object_left
        condition: object's horizontal center <= grid's horizontal center
        effect: "Shift object horizontally so its minimum column index becomes 0."
      - transformation: move_object_right
        condition: object's horizontal center > grid's horizontal center
        effect: "Shift object horizontally so its maximum column index becomes the grid's maximum column index (width - 1)."

    ```


*   **Natural Language Program:**
    1.  Create a new output grid with the same dimensions as the input grid, initialized with zeros.
    2.  Identify all unique non-zero integer values present in the input grid.
    3.  For each unique non-zero value `V`:
        a.  Find all coordinates `(row, col)` in the input grid where the cell value is `V`.
        b.  Determine the minimum column index (`min_col`) and maximum column index (`max_col`) among these coordinates.
        c.  Calculate the horizontal center of the grid: `grid_center_col = (grid_width - 1) / 2`.
        d.  Calculate the horizontal center of the group of cells with value `V`: `object_center_col = (min_col + max_col) / 2`.
        e.  If `object_center_col` is less than or equal to `grid_center_col`:
            i.  Calculate the required horizontal shift: `shift = 0 - min_col`.
            ii. For each original coordinate `(row, col)` with value `V`, set the value `V` at the corresponding coordinate `(row, col + shift)` in the output grid.
        f.  Else (if `object_center_col` is greater than `grid_center_col`):
            i.  Calculate the required horizontal shift: `shift = (grid_width - 1) - max_col`.
            ii. For each original coordinate `(row, col)` with value `V`, set the value `V` at the corresponding coordinate `(row, col + shift)` in the output grid.
    4.  Return the completed output grid.
