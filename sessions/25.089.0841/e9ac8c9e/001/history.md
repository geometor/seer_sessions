
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 4 0 0
0 0 0 5 5 5 5 0 0 0
0 0 0 5 5 5 5 0 0 0
0 0 0 5 5 5 5 0 0 0
0 0 0 5 5 5 5 0 0 0
0 0 8 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 4 4 0 0 0
0 0 0 3 3 4 4 0 0 0
0 0 0 8 8 6 6 0 0 0
0 0 0 8 8 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 2 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
0 7 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 2 0 0 0 0 0 0
0 0 7 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
8 0 0 0 0 0 0 9 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
0 5 5 5 5 5 5 0 0 0
7 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 8 8 8 9 9 9 0 0 0
0 8 8 8 9 9 9 0 0 0
0 8 8 8 9 9 9 0 0 0
0 7 7 7 6 6 6 0 0 0
0 7 7 7 6 6 6 0 0 0
0 7 7 7 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input grids contain a prominent rectangular block of gray pixels (color 5).
    *   Surrounding this gray rectangle, but not necessarily adjacent, are four distinct non-gray, non-white pixels, which act as color markers. These markers tend to be located towards the general corners relative to the gray rectangle.
    *   The rest of the input grid is typically filled with the background color (white, 0).
    *   The output grid retains the same dimensions as the input grid.
    *   The transformation replaces the gray rectangle area in the output grid.
    *   The area corresponding to the input gray rectangle is divided into four equal quadrants in the output grid.
    *   Each quadrant is filled with the color of one of the four marker pixels from the input. The mapping is consistent: the top-left marker colors the top-left quadrant, the top-right marker colors the top-right quadrant, the bottom-left marker colors the bottom-left quadrant, and the bottom-right marker colors the bottom-right quadrant.
    *   The marker pixels themselves and the original gray pixels are removed (replaced by background or the quadrant fill color) in the output.

*   **YAML Facts:**
    
```yaml
    task_description: Fill a central gray rectangle based on four corner color markers.

    elements:
      - object: background
        color: white (0)
        role: Fills most of the grid area.

      - object: target_rectangle
        color: gray (5)
        shape: rectangle
        role: Defines the area to be filled in the output.
        properties:
          - is contiguous
          - dimensions are always even in examples (height H, width W)

      - object: corner_markers
        color: any non-white (0), non-gray (5) color
        count: 4
        role: Determine the fill colors for the output quadrants.
        location: Located relatively near the four corners of the grid, outside the target_rectangle.
        identification:
          - C_TL: Non-background, non-gray pixel with the minimum row index, then minimum column index.
          - C_TR: Non-background, non-gray pixel with the minimum row index, then maximum column index.
          - C_BL: Non-background, non-gray pixel with the maximum row index, then minimum column index.
          - C_BR: Non-background, non-gray pixel with the maximum row index, then maximum column index.

    transformation:
      - action: identify_target_rectangle
        input: input_grid
        output: coordinates (row_start, col_start, height H, width W) of the gray rectangle.

      - action: identify_corner_markers
        input: input_grid, target_rectangle (to exclude gray)
        output: Four colors (C_TL, C_TR, C_BL, C_BR) based on their relative corner positions.

      - action: create_output_grid
        input: input_grid dimensions
        output: A new grid of the same size, filled with background color (white, 0).

      - action: fill_quadrants
        input: output_grid, target_rectangle coordinates, corner marker colors (C_TL, C_TR, C_BL, C_BR)
        process:
          - Divide the target_rectangle area within the output grid into four equal quadrants of size (H/2) x (W/2).
          - Fill the top-left quadrant with C_TL.
          - Fill the top-right quadrant with C_TR.
          - Fill the bottom-left quadrant with C_BL.
          - Fill the bottom-right quadrant with C_BR.
        output: Modified output_grid.

    relationships:
      - The position of each corner_marker relative to the overall grid determines which quadrant of the target_rectangle it colors.
      - The size of the target_rectangle determines the size and location of the filled area in the output.
      - The dimensions (H, W) of the target_rectangle determine the size of each filled quadrant (H/2, W/2).
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
    2.  Identify the contiguous rectangular block of gray pixels (color 5) in the input grid. Determine its top-left corner coordinates (row\_start, col\_start) and its dimensions (height H, width W).
    3.  Identify the four corner marker pixels in the input grid. These are the non-background (non-0), non-gray (non-5) pixels located as follows:
        *   Top-Left Marker (C\_TL): The marker pixel with the minimum row index. If there's a tie, the one with the minimum column index among those.
        *   Top-Right Marker (C\_TR): The marker pixel with the minimum row index. If there's a tie, the one with the maximum column index among those.
        *   Bottom-Left Marker (C\_BL): The marker pixel with the maximum row index. If there's a tie, the one with the minimum column index among those.
        *   Bottom-Right Marker (C\_BR): The marker pixel with the maximum row index. If there's a tie, the one with the maximum column index among those.
    4.  Divide the area in the output grid corresponding to the input gray rectangle (from `row_start` to `row_start + H - 1` and `col_start` to `col_start + W - 1`) into four equal quadrants, each of size (H/2) by (W/2).
    5.  Fill the pixels in the top-left quadrant (rows `row_start` to `row_start + H/2 - 1`, columns `col_start` to `col_start + W/2 - 1`) with the color of the Top-Left Marker (C\_TL).
    6.  Fill the pixels in the top-right quadrant (rows `row_start` to `row_start + H/2 - 1`, columns `col_start + W/2` to `col_start + W - 1`) with the color of the Top-Right Marker (C\_TR).
    7.  Fill the pixels in the bottom-left quadrant (rows `row_start + H/2` to `row_start + H - 1`, columns `col_start` to `col_start + W/2 - 1`) with the color of the Bottom-Left Marker (C\_BL).
    8.  Fill the pixels in the bottom-right quadrant (rows `row_start + H/2` to `row_start + H - 1`, columns `col_start + W/2` to `col_start + W - 1`) with the color of the Bottom-Right Marker (C\_BR).
    9.  Return the modified output grid.
