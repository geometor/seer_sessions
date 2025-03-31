*   **Perception:** The input grids contain vertical segments of 'azure' pixels (8) at the top, a background of 'white' pixels (0), and sometimes a 'red' object (2) located below the 'azure' segments. The output grids are modifications of the input grids where the 'azure' segments are extended downwards. The extension seems to originate from below the existing 'azure' segments in specific columns and continues towards the bottom of the grid, potentially interacting with or being limited by the 'red' object, although closer inspection reveals the extension goes all the way down regardless of the red object, only changing white pixels.

*   **Facts YAML:**
    
```yaml
    Grid:
      - background_color: white (0)
      - contains: objects
    Objects:
      - type: azure_segment
        color: azure (8)
        description: Typically vertical segments or single pixels located in the upper part of the grid. Multiple segments can exist in different columns.
        properties:
          - column_index
          - lowest_row_index
      - type: red_shape
        color: red (2)
        description: A contiguous shape made of red pixels, located below the azure segments in some examples. Its presence or exact shape does not seem to affect the primary transformation logic directly, other than its pixels not being overwritten.
    Transformation:
      - type: vertical_extension
        color: azure (8)
        target_columns: Columns containing at least one azure pixel in the input.
        starting_point: For each target column, the extension starts from the row directly below the lowest existing azure pixel in that column.
        affected_pixels: Only white (0) pixels within the target columns and below the starting point are changed.
        ending_point: The extension continues downwards to the bottom edge of the grid.
        overwrite_rule: Existing non-white pixels (e.g., red pixels) are not changed.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the output grid.
    2.  Identify all columns in the input grid that contain at least one 'azure' (8) pixel.
    3.  For each identified column:
        a.  Find the row index (`r_low`) of the lowest 'azure' pixel in that column.
        b.  Iterate through the rows from `r_low + 1` down to the last row of the grid.
        c.  For each cell in the current column and iterated row, if the cell's color is 'white' (0), change its color to 'azure' (8) in the output grid. Leave non-'white' cells unchanged.
    4.  Return the modified output grid.