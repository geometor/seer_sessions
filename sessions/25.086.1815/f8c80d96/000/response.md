**Perception:**

The input grids contain mostly white pixels (0) and one or more objects composed of a single, non-white color (blue=1 in example 1, azure=8 in example 2, red=2 in example 3). The output grids retain the original colored objects in their exact positions. However, many of the white pixels from the input have been replaced in the output. Specifically, rows and columns that were entirely white in the input are filled with new colors in the output. The filling colors appear to be gray (5) and the original object color. Columns that were entirely white in the input are filled with gray (5). Rows that were entirely white in the input are filled with the original object's color, but only in positions that were not already filled with gray by the column-filling step.

**Facts:**


```yaml
examples:
  - id: train_1
    input_grid_size: [10, 10]
    output_grid_size: [10, 10]
    input_colors: [0, 1] # white, blue
    output_colors: [1, 5] # blue, gray
    input_objects:
      - color: 1 # blue
        pixels: [[0,4],[1,4],[2,4],[3,4],[4,4],[5,4],[0,7],[1,7],[2,7],[2,8],[2,9],[5,5],[5,6],[5,7],[5,8],[5,9]]
    output_changes:
      - action: identify_empty_columns
        criteria: columns containing only white (0) pixels in input
        target_columns: [0, 1, 2, 3, 5, 6, 9]
      - action: fill_columns
        color: 5 # gray
        target: columns identified above
      - action: identify_empty_rows
        criteria: rows containing only white (0) pixels in input
        target_rows: [6, 7, 8, 9]
      - action: fill_rows
        color: 1 # blue (original object color)
        target: rows identified above, excluding pixels already changed to gray(5)
  - id: train_2
    input_grid_size: [10, 10]
    output_grid_size: [10, 10]
    input_colors: [0, 8] # white, azure
    output_colors: [5, 8] # gray, azure
    input_objects:
      - color: 8 # azure
        pixels: [[4,0],[4,1],[4,2],[4,3],[4,4],[4,5],[5,5],[6,0],[6,1],[6,2],[6,3],[6,5],[7,3],[7,5],[8,0],[8,1],[8,3],[8,5],[9,1],[9,3],[9,5]]
    output_changes:
      - action: identify_empty_columns
        criteria: columns containing only white (0) pixels in input
        target_columns: [6, 7, 8, 9]
      - action: fill_columns
        color: 5 # gray
        target: columns identified above
      - action: identify_empty_rows
        criteria: rows containing only white (0) pixels in input
        target_rows: [0, 1, 2, 3]
      - action: fill_rows
        color: 8 # azure (original object color)
        target: rows identified above, excluding pixels already changed to gray(5)
  - id: train_3
    input_grid_size: [10, 10]
    output_grid_size: [10, 10]
    input_colors: [0, 2] # white, red
    output_colors: [2, 5] # red, gray
    input_objects:
      - color: 2 # red
        pixels: [[0,1],[0,3],[0,5],[0,7],[1,1],[1,3],[1,4],[1,5],[1,7],[2,1],[2,7],[3,1],[3,2],[3,3],[3,4],[3,5],[3,6],[3,7]]
    output_changes:
      - action: identify_empty_columns
        criteria: columns containing only white (0) pixels in input
        target_columns: [0, 2, 8, 9]
      - action: fill_columns
        color: 5 # gray
        target: columns identified above
      - action: identify_empty_rows
        criteria: rows containing only white (0) pixels in input
        target_rows: [4, 5, 6, 7, 8, 9]
      - action: fill_rows
        color: 2 # red (original object color)
        target: rows identified above, excluding pixels already changed to gray(5)

general_transformation:
  - step: Identify the single non-white color present in the input grid (object_color).
  - step: Create a copy of the input grid to serve as the initial output grid.
  - step: Identify all columns in the input grid that contain only white (0) pixels.
  - step: For each identified empty column, change all pixels in the corresponding column of the output grid to gray (5).
  - step: Identify all rows in the input grid that contain only white (0) pixels.
  - step: For each identified empty row, change all pixels in the corresponding row of the output grid to the object_color, *but only if* the pixel was not already changed to gray (5) in the previous column-filling step.
  - step: The resulting grid is the final output.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Find the single non-white color present in the input grid; let this be `object_color`.
3.  Identify the indices of all columns in the input grid that contain exclusively white (0) pixels.
4.  For each identified column index `c`:
    *   Iterate through all rows `r` from 0 to the grid height minus 1.
    *   Set the pixel at `(r, c)` in the output grid to gray (5).
5.  Identify the indices of all rows in the input grid that contain exclusively white (0) pixels.
6.  For each identified row index `r`:
    *   Iterate through all columns `c` from 0 to the grid width minus 1.
    *   If the pixel at `(r, c)` in the output grid is still white (0) (meaning it wasn't changed to gray in step 4), set the pixel at `(r, c)` in the output grid to `object_color`.
7.  Return the modified output grid.