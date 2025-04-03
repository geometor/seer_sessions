
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 3 3 3
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 0 0 2 0 0 0
0 0 0 2 0 0 0
0 0 0 2 0 0 0
0 0 0 2 0 0 0
0 0 0 2 0 0 0
0 0 0 2 0 0 0
0 0 0 2 0 0 0
```

*   **Perception:** The task involves modifying a grid containing a single, solid, non-zero colored rectangular or square shape against a zero background. The modification extends a line from the center of the shape either horizontally to the right edge or vertically to the bottom edge, depending on the shape's aspect ratio. The color of the extended line matches the color of the shape.

*   **YAML Facts:**
    
```yaml
    task_type: grid_modification
    components:
      - input_grid:
          type: 2D_array
          description: Contains a background (value 0) and a single contiguous non-zero shape.
      - output_grid:
          type: 2D_array
          description: The input grid with an added line extending from the center of the shape.
      - shape:
          description: The single contiguous block of non-zero identical values in the input grid.
          properties:
            - color: The non-zero value of the cells in the shape.
            - bounding_box: The minimum and maximum row and column indices enclosing the shape.
            - height: The number of rows spanned by the shape.
            - width: The number of columns spanned by the shape.
            - center_row: The row index corresponding to the geometric center of the shape (using integer division for midpoint).
            - center_column: The column index corresponding to the geometric center of the shape (using integer division for midpoint).
      - added_line:
          description: A line of cells filled with the shape's color, added to the input grid to produce the output grid.
          properties:
            - orientation: Either 'horizontal' or 'vertical'.
            - start_position: Adjacent to the center row/column on one edge of the shape.
            - end_position: The edge of the grid (right or bottom).
            - color: Same as the shape's color.
    relationships:
      - The output grid is derived from the input grid.
      - The added_line's color is determined by the shape's color.
      - The added_line's orientation and direction depend on the shape's height and width:
          - If height > width, the line is vertical, extending downwards from the bottom edge of the shape in the center column.
          - If width >= height, the line is horizontal, extending rightwards from the right edge of the shape in the center row.
      - The added_line starts from the cell adjacent to the shape's bounding box along the center row/column.
      - The added_line extends to the grid boundary (bottom edge for vertical, right edge for horizontal).
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify the single contiguous block of non-zero numbers (the shape) in the input grid. Determine its color (`C`), its minimum row (`min_r`), maximum row (`max_r`), minimum column (`min_c`), and maximum column (`max_c`).
    3.  Calculate the height (`H = max_r - min_r + 1`) and width (`W = max_c - min_c + 1`) of the shape's bounding box.
    4.  Calculate the central row index `center_r = (min_r + max_r) // 2`.
    5.  Calculate the central column index `center_c = (min_c + max_c) // 2`.
    6.  Compare the height and width:
        a.  If `H > W`, iterate through the rows from `max_r + 1` down to the last row of the grid. For each row `r` in this range, set the cell at `(r, center_c)` in the output grid to the color `C`.
        b.  If `W >= H`, iterate through the columns from `max_c + 1` rightwards to the last column of the grid. For each column `c` in this range, set the cell at `(center_r, c)` in the output grid to the color `C`.
    7.  Return the modified output grid.
