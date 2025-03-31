*   **Perception:** The input and output grids have the same dimensions. The grids contain pixels of three colors: white (0), blue (1), and red (2). The positions of the blue pixels (1) in the input seem crucial. In the output grid, the pixels located in the same rows or columns as the input blue pixels are changed to blue (1). All other pixels retain their original color from the input grid.

*   **Facts:**
    
```yaml
    grid_properties:
      - dimensions_match: Input and output grids have the same height and width.
      - colors_present: white (0), blue (1), red (2).
    objects:
      - type: pixel
        properties:
          - color: Integer value 0-9 (specifically 0, 1, 2 observed).
          - location: Defined by row and column index.
      - type: row
        properties:
          - index: Integer identifying the row.
          - contains_blue_pixel: Boolean, true if any pixel in the row has color 1 in the input.
      - type: column
        properties:
          - index: Integer identifying the column.
          - contains_blue_pixel: Boolean, true if any pixel in the column has color 1 in the input.
    relationships:
      - A pixel belongs to one row and one column.
      - The presence of a blue pixel (1) in a row or column in the input grid influences the color of all pixels in that corresponding row or column in the output grid.
    actions:
      - identify: Locate all pixels with color blue (1) in the input grid.
      - determine_affected_regions: Find all unique row indices and column indices that contain at least one blue pixel.
      - transform: Create the output grid by:
          - For each pixel location (row, col):
            - If the row index is among the identified affected rows OR the column index is among the identified affected columns:
              - Set the output pixel color to blue (1).
            - Else:
              - Set the output pixel color to the same color as the input pixel at that location.

    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify the coordinates (row and column indices) of all blue pixels (color 1) in the input grid.
    3.  Collect all unique row indices from these coordinates.
    4.  Collect all unique column indices from these coordinates.
    5.  Iterate through each pixel position (row `r`, column `c`) of the grid.
    6.  If the row index `r` is in the collection of unique row indices identified in step 3, change the color of the pixel at (`r`, `c`) in the output grid to blue (1).
    7.  If the column index `c` is in the collection of unique column indices identified in step 4, change the color of the pixel at (`r`, `c`) in the output grid to blue (1).
    8.  Pixels whose row and column indices are not identified in steps 3 and 4 retain their original color from the input grid (this is handled by the initialization in step 1 and the conditional changes in steps 6 & 7).