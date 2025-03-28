*   **Perception:** The input grids contain a single horizontal line composed mostly of blue pixels, but with one or more non-blue pixels embedded within it. The rest of the grid is white. The output grids are identical to the input grids, except that vertical columns are drawn extending upwards from the non-blue pixels found in the horizontal line.

*   **YAML Facts:**
    
```yaml
    facts:
      - element: grid
        description: A 2D array of pixels with colors represented by integers 0-9.
      - element: background
        property: color
        value: white (0)
        description: The predominant color filling most of the grid space.
      - element: base_line
        description: A single horizontal contiguous line of non-white pixels found in the input grid.
        property: composition
        value: Mostly blue (1) pixels, containing one or more "trigger" pixels of other colors (e.g., azure (8), red (2)).
        location: Varies vertically but is unique within each input.
      - element: trigger_pixel
        description: A pixel within the base_line that is not blue (1).
        property: color
        value: Varies (azure (8) or red (2) in examples).
        location: Specific column index within the base_line.
      - element: output_column
        description: A vertical column appearing in the output grid directly above a trigger_pixel.
        property: height
        value: Dependent on the color of the trigger_pixel (3 for azure (8), 4 for red (2)).
        property: composition
        value: The top pixel matches the trigger_pixel's color. The pixels below it, down to the row above the base_line, are blue (1).
        relationship: Positioned in the same column as the corresponding trigger_pixel.
        action: Created or drawn onto the output grid.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify the unique horizontal row (the "base line") that contains non-white pixels.
    3.  Iterate through each pixel in the base line.
    4.  For each pixel that is *not* blue (1) and *not* white (0) (a "trigger pixel"):
        a.  Note its color (C) and column index (X).
        b.  Determine the required height (H) for the new column based on the color C: if C is azure (8), H is 3; if C is red (2), H is 4.
        c.  Place the color C in the output grid at column X and row `(base_line_row - H + 1)`.
        d.  Fill the pixels in the output grid at column X, from row `(base_line_row - H + 2)` up to `(base_line_row - 1)`, with the color blue (1).