Okay, let's analyze the task examples.

## Perception

1.  **Input Structure:** The input grids contain various colored pixels, including white (0) background pixels. A key feature in all inputs is the presence of two distinct, solid vertical lines spanning the full height of the grid and two distinct, solid horizontal lines spanning the full width of the grid. These lines are composed of single, non-white colors. Other non-white pixels might be scattered within the grid.
2.  **Output Structure:** The output is a rectangular subgrid extracted from the input.
3.  **Transformation:** The transformation involves identifying the boundaries defined by the pairs of vertical and horizontal lines and extracting the rectangular region enclosed by these boundaries (inclusive of the boundary lines themselves).
4.  **Boundary Identification:**
    *   The left and right boundaries of the output subgrid correspond to the column indices of the two vertical lines found in the input.
    *   The top and bottom boundaries of the output subgrid correspond to the row indices of the two horizontal lines found in the input.
5.  **Content Preservation:** The pixel values within the extracted rectangular region are preserved directly from the input to the output. The relative positions of the pixels within the extracted region remain the same.

## Facts


```yaml
task_elements:
  - element: input_grid
    description: A 2D grid of pixels with integer values 0-9 representing colors.
  - element: output_grid
    description: A 2D grid of pixels, representing a subgrid extracted from the input_grid.
  - element: vertical_line
    description: An object within the input_grid consisting of a contiguous column of identical non-white pixels spanning the full height of the grid.
    properties:
      - color: The single color of the pixels forming the line.
      - column_index: The index of the column containing the line.
      - extent: Spans the full height of the grid.
    count: Exactly 2, with distinct colors and distinct column indices.
  - element: horizontal_line
    description: An object within the input_grid consisting of a contiguous row of identical non-white pixels spanning the full width of the grid.
    properties:
      - color: The single color of the pixels forming the line.
      - row_index: The index of the row containing the line.
      - extent: Spans the full width of the grid.
    count: Exactly 2, with distinct colors and distinct row indices.
  - element: bounding_box
    description: An implicit rectangular region defined by the intersection of the rows and columns marked by the identified lines.
    properties:
      - top_row: The minimum row index of the two horizontal lines.
      - bottom_row: The maximum row index of the two horizontal lines.
      - left_col: The minimum column index of the two vertical lines.
      - right_col: The maximum column index of the two vertical lines.

transformation:
  action: extract_subgrid
  input: input_grid
  output: output_grid
  logic: The output_grid is formed by extracting the pixels from the input_grid located within the bounding_box, inclusive of the boundaries.
  steps:
    - Identify the two vertical_lines in the input_grid.
    - Determine their column_indices (col1, col2).
    - Identify the two horizontal_lines in the input_grid.
    - Determine their row_indices (row1, row2).
    - Define the bounding_box using min/max of these indices: top=min(row1, row2), bottom=max(row1, row2), left=min(col1, col2), right=max(col1, col2).
    - Extract the subgrid from input_grid[top:bottom+1, left:right+1].
```


## Natural Language Program

1.  Scan the input grid to identify two distinct columns that consist entirely of the same, non-white color from top to bottom. Record the column indices of these two vertical lines.
2.  Scan the input grid to identify two distinct rows that consist entirely of the same, non-white color from left to right. Record the row indices of these two horizontal lines.
3.  Determine the minimum and maximum column indices found in step 1 (`left_col`, `right_col`).
4.  Determine the minimum and maximum row indices found in step 2 (`top_row`, `bottom_row`).
5.  Create the output grid by copying the rectangular portion of the input grid starting at `top_row` and ending at `bottom_row` (inclusive), and starting at `left_col` and ending at `right_col` (inclusive).