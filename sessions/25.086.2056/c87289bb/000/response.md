*   **Perception:**
    *   The input and output grids have the same dimensions.
    *   The input grids contain azure (8) pixels, typically forming horizontal lines or patterns near the top.
    *   They also contain at least one distinct object made of non-white pixels (red (2) in the examples) located below the azure patterns.
    *   The rest of the grid is filled with white (0) pixels.
    *   In the output grids, the original azure pixels and the non-white objects remain in their positions.
    *   New azure pixels appear below the original azure patterns. Specifically, vertical lines of azure extend downwards from the columns that contained azure pixels in the upper part of the input grid.
    *   These downward extensions fill only the white pixels.
    *   The extension of an azure line in a column stops when it encounters a non-white pixel in that column or reaches the bottom edge of the grid.

*   **Facts:**
    
```yaml
    task_description: "Extend vertical azure lines downwards from existing azure pixels until an obstacle or the grid bottom is reached."
    
    elements:
      - object: azure_pixels
        color: 8 (azure)
        role: source and extension_material
        location: Primarily in the upper rows of the input, potentially extending downwards in the output.
      - object: obstacle_pixels
        color: any color except 0 (white) and 8 (azure)
        role: barrier
        location: Below the initial azure pixels in the input. In the examples, these are red (2) pixels.
      - object: background_pixels
        color: 0 (white)
        role: fillable_space
        location: Everywhere else.
    
    relationships:
      - type: spatial
        description: Obstacle pixels are located below the initial azure pixels.
      - type: interaction
        description: Azure lines extend downwards from the columns defined by the initial azure pixels.
      - type: boundary
        description: The downward extension of azure lines stops at the row immediately above an obstacle pixel or at the bottom row of the grid.
    
    transformation:
      - action: identify_source_region
        input: input grid
        output: the set of rows from the top down to the last row containing any azure pixel. Let the index of this last row be 'max_r'.
      - action: identify_source_columns
        input: input grid, source_region
        output: the set of column indices 'c' where at least one azure pixel exists between row 0 and 'max_r' (inclusive).
      - action: copy_grid
        input: input grid
        output: initial output grid (identical to input).
      - action: extend_lines
        input: initial output grid, source_columns, max_r, input grid (for checking obstacles)
        output: final output grid
        steps:
          - For each column 'c' in source_columns:
            - Iterate downwards row by row ('scan_r'), starting from 'max_r + 1'.
            - Check the color of the pixel at `input[scan_r][c]`.
            - If the pixel is white (0): Change the pixel at `output[scan_r][c]` to azure (8).
            - If the pixel is not white (0): Stop extending the line in this column 'c'.
            - If the bottom of the grid is reached: Stop extending the line in this column 'c'.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as an identical copy of the input grid.
    2.  Identify the lowermost row in the input grid that contains at least one azure (8) pixel. Let the index of this row be `max_r`. If no azure pixels exist in the input, the process is complete, and the copied grid is the final output.
    3.  Identify all columns that contain at least one azure (8) pixel at or above row `max_r`.
    4.  For each identified column:
        a.  Starting from the row immediately below `max_r` (row `max_r + 1`), scan downwards row by row towards the bottom of the grid.
        b.  For the current row being scanned, examine the pixel in the input grid at the current row and column.
        c.  If the input pixel at this position is white (0), change the corresponding pixel in the output grid to azure (8).
        d.  If the input pixel at this position is *not* white (0), stop scanning downwards for this column and proceed to the next identified column.
        e.  If the scan reaches the bottom row and the pixel is white, change it to azure in the output grid, then stop scanning for this column and proceed to the next identified column.
    5.  Return the final output grid.