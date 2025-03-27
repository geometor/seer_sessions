*   **Perception:**
    *   The input grids are consistently 10x10, sparsely populated with single, non-white pixels (values 1-9) scattered amidst a white background (value 0).
    *   The output grids are consistently 3x3.
    *   The output grids contain the same non-white pixels found in the corresponding input grids.
    *   The number of non-white pixels varies across examples (7 in train_1, 6 in train_2, 9 in train_3).
    *   The output grid appears to be filled with the non-white pixels from the input, potentially padded with white (0) if there are fewer than 9 non-white pixels.
    *   The arrangement of pixels in the output grid suggests a specific ordering derived from the input grid. Standard reading order (row by row, left to right) of the input pixels does not match the output order. However, scanning the input grid column by column (top to bottom within each column, then moving left to right across columns) and collecting the non-white pixels precisely matches the order they appear in the output grid (filled row by row, left to right).

*   **Facts:**
    
```yaml
    task_type: extraction_and_reshaping
    input_grid_size: 10x10
    output_grid_size: 3x3
    background_color: white (0)
    objects:
      - type: individual pixels
        color: non-white (1-9)
        properties:
          - value (color)
          - position (row, column)
    actions:
      - identify: locate all non-white pixels in the input grid.
      - order: arrange the identified pixels based on their position in the input grid, using a column-major order (scan columns from left to right, and within each column, scan from top to bottom).
      - reshape: place the ordered pixels into a 3x3 output grid, filling row by row, left to right.
      - padding: if the number of non-white pixels is less than 9, fill the remaining cells of the 3x3 output grid with the background color (white, 0).
    relationships:
      - the sequence of pixels in the output grid is determined by the column-major traversal of non-white pixels in the input grid.
    ```


*   **Natural Language Program:**
    1.  Initialize an empty list to store the non-white pixels found in the input grid.
    2.  Iterate through the columns of the input grid, from the leftmost column (index 0) to the rightmost column.
    3.  Within each column, iterate through the rows from the top row (index 0) to the bottom row.
    4.  If the current pixel's value is not white (0), add its value to the list.
    5.  Create a new 3x3 grid, initialized with white (0) pixels.
    6.  Iterate through the cells of the 3x3 output grid, row by row, from top to bottom, and left to right within each row.
    7.  For each cell in the output grid, if there are still pixels remaining in the list collected in step 4, take the next pixel value from the list and place it in the current output grid cell. Remove the pixel value from the list.
    8.  If the list of collected pixels becomes empty before filling the entire 3x3 output grid, the remaining cells will keep their initial white (0) value.
    9.  Return the filled 3x3 output grid.