*   **Perception:**
    *   Each input grid contains two distinct colored patterns, separated vertically by one or more rows composed entirely of white pixels (0).
    *   The upper pattern uses one primary color (e.g., red in train_1, azure in train_2, blue in train_3) mixed with white.
    *   The lower pattern uses a *different* primary color (e.g., green in train_1, red in train_2, yellow in train_3) mixed with white.
    *   The output grid corresponds exactly to the lower pattern found in the input grid.
    *   The transformation involves identifying the block of separator rows (all white) and then extracting the content found below this separator.
    *   The extraction preserves the dimensions and colors (including internal white pixels) of the lower pattern. The boundaries for extraction are determined by the minimum bounding box containing all non-white pixels within the rows belonging to the lower pattern.

*   **Facts:**
    
```yaml
    task_description: Extract the lower pattern from an input grid, where patterns are separated by horizontal white space.

    elements:
      - element: grid
        role: input
        properties:
          - contains two distinct non-white patterns (upper and lower)
          - patterns are separated by one or more rows of only white pixels
          - each pattern consists of one primary non-white color and white pixels

      - element: grid
        role: output
        properties:
          - is a subgrid of the input
          - corresponds exactly to the lower pattern identified in the input
          - dimensions match the bounding box of the non-white pixels in the lower pattern section of the input

    relationships:
      - type: separation
        between: upper pattern, lower pattern
        via: horizontal rows of white pixels (value 0)
      - type: extraction
        source: input grid
        target: output grid
        details: The output grid is the minimal bounding box containing all non-white pixels found in the rows below the separating white rows in the input grid.

    actions:
      - action: locate_separator
        description: Find the contiguous block of rows containing only white pixels. Identify the last row index of this block.
      - action: identify_lower_pattern_rows
        description: Find the range of rows below the separator block that contain at least one non-white pixel.
      - action: identify_lower_pattern_columns
        description: Within the identified lower pattern rows, find the range of columns that contain at least one non-white pixel.
      - action: extract_subgrid
        description: Copy the portion of the input grid defined by the identified row and column ranges to create the output grid.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid row by row from top to bottom.
    2.  Identify the first contiguous block of one or more rows where all pixels are white (0). Record the row index of the *last* row in this separator block.
    3.  Consider only the rows *below* this separator block.
    4.  Find the minimum row index (`row_start`) and maximum row index (`row_end`) of rows in this lower section that contain at least one non-white pixel.
    5.  Within the rows from `row_start` to `row_end` (inclusive), find the minimum column index (`col_start`) and maximum column index (`col_end`) that contain a non-white pixel.
    6.  Extract the subgrid from the input grid starting at `row_start`, ending at `row_end`, starting at `col_start`, and ending at `col_end`. This extracted subgrid is the output.