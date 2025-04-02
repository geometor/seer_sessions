## Perception

1.  **Grid Structure:** The input and output are grids containing pixels of white (0), red (2), and yellow (4). White serves as the background color.
2.  **Input Composition:** Each input grid contains exactly one yellow pixel and multiple red pixels scattered across the grid.
3.  **Output Composition:** The output grid contains *either* only the original yellow pixel *or* all the original red pixels, with the remaining pixels being white (background). The pixel(s) that are kept retain their original positions.
4.  **Core Transformation:** The task involves deciding whether to preserve the yellow pixel or the set of red pixels based on the spatial relationship between the yellow pixel and the red pixels.
5.  **Identifying the Condition:** The decision hinges on whether any red pixels share the same row or column as the single yellow pixel.
    *   If the yellow pixel is "isolated" (no red pixels in its row or column), the yellow pixel is kept, and all red pixels are removed. (Seen in train_1)
    *   If the yellow pixel shares a row or column with one or more red pixels, a secondary condition applies based on the *relative direction* of these sharing red pixels.
6.  **Secondary Condition (Directionality):**
    *   If *all* red pixels sharing a row or column with the yellow pixel are located strictly to the *east* (same row, greater column index) of the yellow pixel, then only the yellow pixel is kept. (Seen in train_3)
    *   If *any* red pixel sharing a row or column with the yellow pixel is located North, South, or West of it, or if there are sharing red pixels in multiple directions (e.g., one East, one West), then all original red pixels are kept, and the yellow pixel is removed. (Seen in train_2 and train_4)

## YAML Facts


```yaml
task_description: Preserve either the single yellow pixel or all red pixels based on their spatial relationship.

components:
  - item: Grid
    properties:
      - type: 2D array of integers (0-9)
      - colors: white (0), red (2), yellow (4)
      - background_color: white (0)
  - item: Yellow Pixel
    properties:
      - color: yellow (4)
      - count: exactly 1 per input grid
      - location: (row, col) coordinates
  - item: Red Pixels
    properties:
      - color: red (2)
      - count: variable (one or more) per input grid
      - location: set of (row, col) coordinates

relationships_and_conditions:
  - relationship: Sharing Row/Column
    definition: A red pixel shares a row/column with the yellow pixel if its row index or column index matches the yellow pixel's.
    variable: sharing_red_pixels (set of red pixels satisfying this)
  - condition: Isolation Check
    check: Is the set 'sharing_red_pixels' empty?
    outcome_if_true: Keep Yellow Pixel Only
    outcome_if_false: Proceed to Directionality Check
  - condition: Directionality Check (applies only if 'sharing_red_pixels' is not empty)
    check: Are ALL pixels in 'sharing_red_pixels' located strictly East of the yellow pixel? (pixel.row == yellow.row AND pixel.col > yellow.col)
    outcome_if_true: Keep Yellow Pixel Only
    outcome_if_false: Keep All Red Pixels Only

actions:
  - name: Keep Yellow Pixel Only
    effect: Output grid contains only the yellow pixel at its original location; all other cells are background color.
  - name: Keep All Red Pixels Only
    effect: Output grid contains all original red pixels at their original locations; the position of the original yellow pixel becomes background color, as do all other non-red cells.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid, but set all pixels to the background color (white, 0).
2.  Identify the coordinates (row `y_row`, column `y_col`) of the single yellow (4) pixel in the input grid.
3.  Identify the coordinates of all red (2) pixels in the input grid, storing them as a list or set `red_pixel_locations`.
4.  Create an empty list called `sharing_red_pixels`.
5.  Iterate through each red pixel location (`r_row`, `r_col`) in `red_pixel_locations`:
    *   If `r_row` equals `y_row` (same row) OR `r_col` equals `y_col` (same column), add the location (`r_row`, `r_col`) to the `sharing_red_pixels` list.
6.  Check if the `sharing_red_pixels` list is empty.
    *   **If `sharing_red_pixels` is empty:** Set the pixel at (`y_row`, `y_col`) in the output grid to yellow (4).
    *   **If `sharing_red_pixels` is not empty:**
        *   Set a flag `all_east` to `true`.
        *   Iterate through each sharing red pixel location (`sr_row`, `sr_col`) in `sharing_red_pixels`:
            *   If it's NOT the case that (`sr_row == y_row` AND `sr_col > y_col`), set `all_east` to `false` and stop checking this inner loop.
        *   Check the value of the `all_east` flag:
            *   **If `all_east` is `true`:** Set the pixel at (`y_row`, `y_col`) in the output grid to yellow (4).
            *   **If `all_east` is `false`:** Iterate through all original red pixel locations (`r_row`, `r_col`) in `red_pixel_locations` and set the corresponding pixel in the output grid to red (2).
7.  Return the final output grid.