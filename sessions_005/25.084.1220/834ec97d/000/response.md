Okay, let's analyze the task examples.

## Perception

1.  **Input Grid Structure:** Each input grid contains a single non-white pixel (the "source pixel") on a white background. The grids vary in size.
2.  **Output Grid Structure:** The output grid has the same dimensions as the input grid. It contains the original source pixel, but moved one position down. It also features a new pattern of yellow pixels.
3.  **Source Pixel Movement:** The single non-white pixel from the input grid is found one row lower in the output grid, while maintaining its original column.
4.  **Yellow Pattern Generation:** A pattern of yellow pixels appears in the output grid. This pattern extends from the top row (row 0) down to and including the *original* row of the source pixel.
5.  **Column Parity Rule:** The columns containing the yellow pixels depend on the column of the *original* source pixel. If the source pixel was in an even column (0, 2, 4,...), the yellow pixels appear in all even columns within the specified rows. If the source pixel was in an odd column (1, 3, 5,...), the yellow pixels appear in all odd columns within the specified rows.
6.  **Overlap:** The yellow pattern fills the designated cells. The moved source pixel is then placed, potentially overwriting a yellow cell if its new position `(original_row + 1, original_col)` happens to fall within the yellow pattern's area (although this doesn't occur in the examples as the source always moves *below* the yellow pattern's maximum row). The yellow pattern generation itself *does* overwrite the original position of the source pixel if it matches the row/column parity criteria.

## Facts


```yaml
task_description: Transform the grid based on the position of a single non-white source pixel.

elements:
  - object: grid
    description: A 2D array of pixels with values 0-9 representing colors. Contains a background and usually one distinct object.
    properties:
      - height: Integer (1-30)
      - width: Integer (1-30)
      - background_color: white (0)

  - object: source_pixel
    description: The single non-white pixel in the input grid.
    properties:
      - color: Integer (1-9), varies per example (magenta, red, maroon).
      - initial_location: Tuple (row_s, col_s)
      - column_parity: String ('even' or 'odd') derived from col_s.
      - final_location: Tuple (row_s + 1, col_s)

  - object: yellow_pattern
    description: A pattern of yellow pixels introduced in the output grid.
    properties:
      - color: yellow (4)
      - location: Cells (r, c) where 0 <= r <= row_s, and the parity of c matches the column_parity of the source_pixel.

actions:
  - action: identify_source_pixel
    input: input_grid
    output: source_pixel_properties (color, initial_location, column_parity)
    description: Find the coordinates and color of the unique non-white pixel. Determine the parity of its column.

  - action: generate_yellow_pattern
    input: grid_dimensions, source_pixel_initial_row (row_s), source_pixel_column_parity
    output: partial_output_grid (containing only the yellow pattern on a white background)
    description: Create a grid filled with yellow (4) at cells (r, c) where r is between 0 and row_s (inclusive) and the parity of column c matches the source_pixel_column_parity.

  - action: move_source_pixel
    input: source_pixel_color, source_pixel_initial_location (row_s, col_s)
    output: source_pixel_final_location (row_s + 1, col_s)
    description: Calculate the new position for the source pixel, one row below its original position.

  - action: construct_output_grid
    input: partial_output_grid (from generate_yellow_pattern), source_pixel_color, source_pixel_final_location
    output: final_output_grid
    description: Start with the grid containing the yellow pattern. Place the source_pixel_color at the source_pixel_final_location. Ensure the final grid has the correct dimensions. Handle cases where the final location might be outside the grid boundaries (though not observed in examples, typically implies the pixel is not placed).

relationships:
  - The yellow pattern's vertical extent (rows 0 to row_s) is determined by the source_pixel's initial row.
  - The yellow pattern's horizontal placement (columns included) is determined by the parity of the source_pixel's initial column.
  - The source_pixel's final location is directly derived from its initial location (shifted down by one row).
  - The final output combines the generated yellow pattern and the moved source pixel.
```


## Natural Language Program

1.  **Identify Source:** Scan the input grid to find the unique non-white pixel. Record its color (`source_color`), row (`row_s`), and column (`col_s`).
2.  **Determine Column Parity:** Check if `col_s` is even or odd.
3.  **Initialize Output:** Create a new grid with the same dimensions as the input grid, filled entirely with white pixels (0).
4.  **Generate Yellow Pattern:** Iterate through each cell `(r, c)` of the grid. If the row `r` is less than or equal to `row_s` AND the parity (even/odd) of the column `c` matches the parity of `col_s`, set the pixel at `(r, c)` in the output grid to yellow (4).
5.  **Place Moved Source Pixel:** Calculate the new row `new_row_s = row_s + 1`. If `new_row_s` is within the grid boundaries (i.e., `new_row_s < grid_height`), set the pixel at `(new_row_s, col_s)` in the output grid to `source_color`. This step overwrites any pixel previously placed at this location by the yellow pattern generation (though practically, the source pixel always moves below the generated pattern in the examples).
6.  **Return Output:** The modified grid is the final output.