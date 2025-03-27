*   **Perception:**
    *   The input grids contain various small, colored objects (shapes composed of 1-3 pixels of the same color) scattered on a white background.
    *   A defining feature in all input grids is a solid vertical line of yellow pixels. This line acts as a separator.
    *   The output grids are smaller than the input grids, specifically in width. The height remains the same.
    *   The output grid's content appears derived primarily from the objects located to the *left* of the yellow line in the input. These objects seem shifted one position to the right in the output.
    *   Additionally, one specific pixel from the *right* side of the yellow line in the input appears in the output, but its position is determined by a different rule related to its distance from the yellow line.
    *   The yellow line itself is not present in the output.

*   **Facts:**
    
```yaml
    elements:
      - type: grid_feature
        name: separator_line
        color: yellow
        orientation: vertical
        location: variable column index (column 7 in examples)
      - type: object_set
        name: left_objects
        description: Contiguous blocks of non-white color located entirely to the left of the separator_line.
      - type: object_set
        name: right_objects
        description: Contiguous blocks of non-white color located entirely to the right of the separator_line.
      - type: special_pixel
        description: The first non-white pixel encountered scanning top-to-bottom, left-to-right within the right_objects region.
        color: variable (gray in examples)
      - type: background
        color: white
      - type: output_grid
        properties:
          height: same as input grid height
          width: equal to the column index of the separator_line
    actions:
      - action: find_separator
        input: input_grid
        output: column index of the yellow vertical line (yellow_col)
      - action: define_output_grid
        based_on: input grid height, yellow_col
        result: output grid initialized with white pixels
      - action: transfer_left_objects
        input: left_objects
        target: output_grid
        rule: For each pixel at input[r, c] where c < yellow_col, copy its color to output[r, c + 1], if c + 1 < yellow_col.
      - action: find_special_pixel
        input: right_objects region (columns > yellow_col)
        rule: Scan row by row, then column by column. Identify the first non-white pixel.
        output: coordinates (r_special, c_special) and color of the special pixel.
      - action: place_special_pixel
        input: special_pixel (if found), yellow_col
        target: output_grid
        rule: Place the special pixel's color at output[r_special, c_special - yellow_col - 1].
    ```


*   **Natural Language Program:**
    1.  Identify the column index (`yellow_col`) of the vertical yellow line in the input grid.
    2.  Create a new output grid with the same number of rows as the input grid and a width equal to `yellow_col`, filled initially with white pixels (color 0).
    3.  Iterate through each cell `(r, c)` of the input grid where the column index `c` is less than `yellow_col`.
    4.  If the input cell `input[r, c]` is not white, copy its color to the output grid at position `output[r, c + 1]`, but only if `c + 1` is less than `yellow_col` (i.e., it fits within the output grid's bounds).
    5.  Search the region of the input grid to the right of the yellow line (where column index `c` is greater than `yellow_col`). Scan this region row by row from top to bottom, and within each row, scan column by column from left to right.
    6.  Find the coordinates `(r_special, c_special)` and color of the *first* non-white pixel encountered in this right-side region.
    7.  If such a special pixel is found, place its color into the output grid at the calculated position `output[r_special, c_special - yellow_col - 1]`.
    8.  The resulting grid is the final output.