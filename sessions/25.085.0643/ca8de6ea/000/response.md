*   **Perception:**
    *   The input grids are all 5x5, and the output grids are all 3x3.
    *   The input grids contain a pattern of non-white pixels (colors 1-9) surrounded by white pixels (color 0). There are exactly 9 non-white pixels in each input example.
    *   The output grid consists only of the non-white pixels found in the input grid.
    *   The white pixels from the input grid are discarded.
    *   The relative order of the non-white pixels, when read from the input grid row by row, top to bottom, and left to right within each row, is preserved in the output grid, filling it in the same order (row by row, left to right).

*   **Facts:**
    
```yaml
    task_elements:
      - Input Grid:
          type: 2D array
          size: 5x5
          pixels:
            - type: Background
              color: white (0)
            - type: Data
              color: non-white (1-9)
              count: 9
              distribution: Specific pattern (corners, center, plus sign offset by 1)
      - Output Grid:
          type: 2D array
          size: 3x3
          pixels:
            - type: Data
              color: non-white (1-9)
              source: Extracted from Input Grid
              count: 9
    transformation:
      - action: Identify and Extract
        target: Non-white pixels from Input Grid
        order: Preserve scanline order (top-to-bottom, left-to-right)
      - action: Create Grid
        target: Output Grid
        size: 3x3
      - action: Populate
        target: Output Grid
        source: Extracted non-white pixels
        order: Fill sequentially using scanline order (top-to-bottom, left-to-right)
    relationship:
      - The position of a non-white pixel in the output grid is determined by its rank in the scanline order of non-white pixels in the input grid. The first non-white pixel goes to (0,0), the second to (0,1), ..., the ninth to (2,2).
    ```


*   **Natural Language Program:**
    1.  Initialize an empty list called `extracted_colors`.
    2.  Iterate through the input grid, row by row from top (row 0) to bottom (row 4).
    3.  For each row, iterate through its columns from left (column 0) to right (column 4).
    4.  If the color of the current pixel is not white (0), add its color to the end of the `extracted_colors` list.
    5.  Create a new 3x3 grid, initialized with a default color (e.g., white, although it will be overwritten).
    6.  Initialize a counter `k` to 0.
    7.  Iterate through the rows of the new 3x3 grid, from top (row 0) to bottom (row 2).
    8.  For each row, iterate through its columns from left (column 0) to right (column 2).
    9.  Set the color of the pixel at the current (row, column) in the 3x3 grid to the color stored at index `k` in the `extracted_colors` list.
    10. Increment the counter `k`.
    11. Return the populated 3x3 grid as the output.