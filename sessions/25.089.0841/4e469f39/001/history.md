
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 0 5 0 0 0 0
0 0 5 0 0 5 0 0 0 0
0 0 5 0 0 5 0 0 0 0
0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 0 0 0 0 0
0 0 5 5 2 5 0 0 0 0
0 0 5 2 2 5 0 0 0 0
0 0 5 2 2 5 0 0 0 0
0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 5 5 0 0 0
0 0 0 5 0 0 5 0 0 0
0 0 0 5 0 0 5 0 0 0
0 0 0 5 0 0 5 0 0 0
0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2
0 0 0 5 2 5 5 0 0 0
0 0 0 5 2 2 5 0 0 0
0 0 0 5 2 2 5 0 0 0
0 0 0 5 2 2 5 0 0 0
0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 5 5 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 5 0
0 0 0 0 0 5 0 0 5 0
0 0 0 0 0 5 5 5 5 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2
0 5 2 5 5 0 0 0 0 0
0 5 2 2 5 0 0 0 0 0
0 5 2 2 5 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0
2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 5 5 2 5 0
0 0 0 0 0 5 2 2 5 0
0 0 0 0 0 5 5 5 5 0
```

*   **Perception**: The input grids contain shapes made of gray pixels (5) on a white background (0). These gray shapes often form containers or boundaries around areas of white pixels. The output grids modify the input by filling these enclosed white areas with red pixels (2). Additionally, a horizontal red line is drawn two rows above the topmost part of each filled red area. The extent and direction (starting from the left edge or starting from the filled area's left edge) of this horizontal line depend on whether the right side of the original enclosed white area is bounded by gray pixels.

*   **YAML Facts**:
    
```yaml
    task_description: Fill enclosed white regions with red and draw a horizontal red line above each filled region.
    
    elements:
      - element: background
        color: white (0)
      - element: container
        color: gray (5)
        role: forms boundaries defining enclosed regions
      - element: fill_color
        color: red (2)
        role: fills enclosed white regions in the output
      - element: line_color
        color: red (2)
        role: forms horizontal lines above filled regions in the output

    transformations:
      - action: identify_regions
        input_color: white (0)
        condition: region must be contiguous and fully enclosed by gray (5) pixels (no path from the region to the grid edge only through white pixels)
        resulting_objects: list of enclosed white regions

      - action: fill_regions
        target_regions: output of identify_regions
        fill_color: red (2)
        output_grid_modification: pixels within identified regions are changed from white to red

      - action: draw_lines
        trigger: for each region filled in the previous step
        properties:
          - line_row: Determined by `min_r - 2`, where `min_r` is the minimum row index of the filled region. Skip if `min_r - 2 < 0`.
          - line_extent: Determined by checking for gray pixels adjacent to the right boundary of the original white region.
            - condition_check: Are there any gray (5) pixels at column `max_c + 1` between rows `min_r` and `max_r` (inclusive) of the original white region? (`right_closed`)
            - if `right_closed` is false: line extends from column `min_c` to the right edge of the grid (`width - 1`).
            - if `right_closed` is true: line extends from the left edge of the grid (column 0) to column `max_c`.
          - line_color: red (2)
          - overwrite_rule: Only change white (0) pixels to red (2) in the target row; do not overwrite gray (5) pixels.
        output_grid_modification: red pixels are added in the calculated row and columns.

    relationships:
      - relationship: enclosure
        from: gray (5) pixels
        to: white (0) pixel regions
        description: Gray pixels surround and define the boundaries of the white regions to be filled.
      - relationship: spatial_offset
        from: filled red region
        to: horizontal red line
        description: The line appears exactly two rows above the highest point (`min_r`) of the filled region.
      - relationship: adjacency_check
        from: original white region boundaries
        to: adjacent gray (5) pixels
        description: The presence or absence of gray pixels immediately to the right of the enclosed white region determines the horizontal extent of the associated red line.
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all distinct contiguous regions of white pixels in the input grid that are completely enclosed by gray pixels. A white region is considered enclosed if a flood fill starting within it cannot reach the grid boundary without crossing a gray pixel.
    3.  For each identified enclosed white region:
        a.  Record its bounding box: the minimum row (`min_r`), maximum row (`max_r`), minimum column (`min_c`), and maximum column (`max_c`).
        b.  Fill all white pixels belonging to this region with red (2) in the output grid.
    4.  After filling all enclosed regions, iterate through the recorded bounding boxes of the *original* white regions:
        a.  Calculate the target row for the horizontal line: `target_r = min_r - 2`.
        b.  If `target_r` is less than 0, do not draw a line for this region and proceed to the next region.
        c.  Check if the right side of the original white region was adjacent to any gray pixels: Determine if there were any gray (5) pixels in the input grid at column `max_c + 1` within the row range [`min_r`, `max_r`]. Let this be `right_is_closed`. Handle the case where `max_c + 1` is outside the grid width (in which case `right_is_closed` is false).
        d.  If `right_is_closed` is false:
            i.  Iterate through the columns `c` from `min_c` to the grid width minus 1.
            ii. For each `c`, if the pixel at `(target_r, c)` in the *input* grid is white (0), change the corresponding pixel `(target_r, c)` in the *output* grid to red (2).
        e.  If `right_is_closed` is true:
            i.  Iterate through the columns `c` from 0 to `max_c`.
            ii. For each `c`, if the pixel at `(target_r, c)` in the *input* grid is white (0), change the corresponding pixel `(target_r, c)` in the *output* grid to red (2).
    5.  Return the final output grid.
