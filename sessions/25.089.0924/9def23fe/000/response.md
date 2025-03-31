*   **Perception:**
    *   The input grids contain a background of white pixels (0).
    *   There is one primary, contiguous object of a single color (red=2 in all examples). This object is generally rectangular but can be complex.
    *   There are also several scattered single pixels of another color (green=3, azure=8, or yellow=4). These act as markers or secondary objects.
    *   The output grid retains the original dimensions.
    *   The transformation involves expanding the area covered by the primary color (red=2).
    *   The expansion happens along the rows and columns that originally contained any part of the primary red object.
    *   Specifically, any white pixel (0) in the input grid is changed to the primary color (red=2) in the output grid *if* its row contained a red pixel *or* its column contained a red pixel in the input.
    *   The original red pixels remain red.
    *   The scattered marker pixels (green, azure, yellow) retain their original color and position in the output, potentially overwriting the expanded red area where they coincide.

*   **Facts:**
    
```yaml
    background_color: white (0)
    objects:
      - type: primary_shape
        color: red (2) # Consistent across examples
        description: A contiguous block of pixels defining the main area of interest.
      - type: markers
        color: variable (green=3, azure=8, yellow=4) # Varies per example
        description: Single, scattered pixels distinct from the primary shape and background.
        quantity: multiple
    actions:
      - identify_primary_color_pixels: Find all coordinates of the primary shape (red=2).
      - identify_affected_rows: Collect the unique row indices containing any primary color pixel.
      - identify_affected_columns: Collect the unique column indices containing any primary color pixel.
      - generate_output_grid: Create a new grid based on the input.
      - fill_rows: For each affected row, change all white (0) pixels in that row to the primary color (red=2).
      - fill_columns: For each affected column, change all remaining white (0) pixels in that column to the primary color (red=2).
      - preserve_originals: Ensure that pixels that were not white in the input retain their original color in the output (overwriting any red fill if necessary). This includes the original primary shape pixels and the marker pixels.
    relationships:
      - The primary shape determines which rows and columns are affected.
      - The transformation primarily affects the white background pixels.
      - Marker pixels are unaffected by the transformation itself but persist in the final output.
      - The filling action uses the color of the primary shape.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify the primary color, which is the color appearing in a contiguous block (red=2 in the examples).
    3.  Find all row indices that contain at least one pixel of the primary color in the input grid. Store these as the "affected rows".
    4.  Find all column indices that contain at least one pixel of the primary color in the input grid. Store these as the "affected columns".
    5.  Iterate through each cell `(r, c)` of the input grid.
    6.  If the row index `r` is in the set of "affected rows" AND the input cell `(r, c)` is white (0), change the corresponding output cell `(r, c)` to the primary color (red=2).
    7.  Iterate through each cell `(r, c)` of the grid again (or use the intermediate grid from step 6).
    8.  If the column index `c` is in the set of "affected columns" AND the cell `(r, c)` is currently white (0) (meaning it wasn't filled by the row operation), change the output cell `(r, c)` to the primary color (red=2).
    9.  Ensure all non-white pixels from the original input grid retain their original color in the final output grid (this is implicitly handled by only modifying white pixels in steps 6 & 8 if starting with a copy, but explicitly stated for clarity, especially regarding the marker pixels).