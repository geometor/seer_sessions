
## train_1

**input:**
```
0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 7 0 7 0 0
0 0 0 7 7 7 0 7 0 0
0 0 0 7 0 0 0 7 0 0
0 0 0 7 0 7 7 7 0 0
0 0 0 7 0 7 0 0 0 0
0 0 0 7 0 7 0 0 0 0
0 0 0 7 9 7 0 0 0 0
0 0 0 7 0 7 0 0 0 0
0 0 0 7 0 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 7 8 7 0 0
0 0 0 0 0 7 8 7 0 0
0 0 0 7 7 7 8 7 0 0
0 0 0 7 8 8 8 7 0 0
0 0 0 7 8 7 7 7 0 0
0 0 0 7 8 7 0 0 0 0
0 0 0 7 8 7 0 0 0 0
0 0 0 7 8 7 0 0 0 0
0 0 0 7 8 7 0 0 0 0
0 0 0 7 8 7 0 0 0 0
```


## train_2

**input:**
```
7 0 7 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0
7 0 7 7 7 7 0 0 0 0
7 0 0 0 0 7 0 0 0 0
7 7 7 7 0 7 0 0 0 0
0 0 0 7 0 7 7 7 7 0
0 0 0 7 9 0 0 0 7 0
0 0 0 7 7 7 7 0 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 7 0 7 0
```


**output:**
```
7 8 7 0 0 0 0 0 0 0
7 8 7 0 0 0 0 0 0 0
7 8 7 7 7 7 0 0 0 0
7 8 8 8 8 7 0 0 0 0
7 7 7 7 8 7 0 0 0 0
0 0 0 7 8 7 7 7 7 0
0 0 0 7 9 0 0 0 7 0
0 0 0 7 7 7 7 0 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 7 0 7 0
```


## train_3

**input:**
```
0 0 7 0 7 0 0 0 0 0
0 0 7 0 7 0 0 0 0 0
0 0 7 0 7 7 7 0 0 0
0 0 7 0 0 0 7 0 0 0
0 0 7 7 7 9 7 0 0 0
0 0 0 0 7 0 7 0 0 0
0 0 0 0 7 0 7 7 7 0
0 0 0 0 7 0 0 0 7 0
0 0 0 0 7 7 7 0 7 0
0 0 0 0 0 0 7 0 7 0
```


**output:**
```
0 0 7 8 7 0 0 0 0 0
0 0 7 8 7 0 0 0 0 0
0 0 7 8 7 7 7 0 0 0
0 0 7 8 8 8 7 0 0 0
0 0 7 7 7 8 7 0 0 0
0 0 0 0 7 8 7 0 0 0
0 0 0 0 7 8 7 7 7 0
0 0 0 0 7 8 8 8 7 0
0 0 0 0 7 7 7 8 7 0
0 0 0 0 0 0 7 8 7 0
```


## train_4

**input:**
```
0 0 0 7 0 7 0 0 0 0
0 0 0 7 0 7 0 0 0 0
0 0 0 7 0 7 7 7 0 0
0 0 0 7 0 0 0 7 0 0
0 0 0 7 7 7 0 7 0 0
0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 7 0 7 7 7
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 7 7 7 7
```


**output:**
```
0 0 0 7 8 7 0 0 0 0
0 0 0 7 8 7 0 0 0 0
0 0 0 7 8 7 7 7 0 0
0 0 0 7 8 8 8 7 0 0
0 0 0 7 7 7 8 7 0 0
0 0 0 0 0 7 8 7 0 0
0 0 0 0 0 7 8 7 0 0
0 0 0 0 0 7 8 7 7 7
0 0 0 0 0 7 8 8 8 8
0 0 0 0 0 7 7 7 7 7
```

*   **Perception:**
    *   The input and output grids are primarily composed of white (0) background pixels and orange (7) pixels forming shapes or structures.
    *   Some input grids contain a single maroon (9) pixel, typically located adjacent to or within the orange structures.
    *   The transformation involves changing certain pixels in the input grid to azure (8) in the output grid. All other pixels retain their original color, unless they meet the specific conditions for changing to azure.
    *   The change to azure (8) occurs in areas horizontally bounded by orange (7) pixels within the same row.
    *   White (0) pixels are changed to azure (8) if there is an orange (7) pixel somewhere to their left and somewhere to their right in the same row.
    *   Maroon (9) pixels have a stricter condition: they are changed to azure (8) only if their immediate horizontal neighbors (left and right) are both orange (7).

*   **Facts:**
    
```yaml
    input_grid:
      description: A 2D grid of pixels with integer values 0-9 representing colors.
      elements:
        - color: 0 (white) - Background.
        - color: 7 (orange) - Forms structural boundaries.
        - color: 9 (maroon) - Appears occasionally, sometimes affected by the transformation.
      properties:
        - size: Variable height and width (up to 30x30).
    output_grid:
      description: A 2D grid derived from the input grid by applying a transformation rule.
      elements:
        - color: 0 (white) - Unchanged background pixels.
        - color: 7 (orange) - Unchanged structural pixels.
        - color: 9 (maroon) - Unchanged maroon pixels unless specific conditions met.
        - color: 8 (azure) - Pixels changed from white or maroon based on rules.
      properties:
        - size: Same height and width as the input grid.
    transformation:
      action: Conditional pixel color change (filling).
      target_pixels: Pixels with color white (0) or maroon (9) in the input.
      output_color: azure (8).
      conditions:
        - for_white_pixels:
            description: Change white (0) to azure (8).
            trigger: The pixel must be horizontally bounded by orange (7) pixels within the same row.
            details: There must be at least one orange pixel to the left (any distance) and at least one orange pixel to the right (any distance) in the same row.
        - for_maroon_pixels:
            description: Change maroon (9) to azure (8).
            trigger: The pixel must be immediately horizontally adjacent to orange (7) pixels on both sides.
            details: The pixel directly to the left (column c-1) AND the pixel directly to the right (column c+1) must both be orange (7).
      relationships:
        - horizontal_adjacency: Critical for the maroon pixel transformation condition.
        - horizontal_bounding: Critical for the white pixel transformation condition. The bounding pixels (orange) can be at any horizontal distance within the row.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the basis for the output grid.
    2.  Iterate through each row `r` of the grid.
    3.  For each row `r`, find the column indices of all orange (7) pixels. Let these be `orange_cols`.
    4.  Iterate through each column `c` in the current row `r`.
    5.  Get the color of the input pixel at `(r, c)`.
    6.  **If the input pixel color is white (0):**
        a.  Check if there exists an orange column index `c_left` in `orange_cols` such that `c_left < c`.
        b.  Check if there exists an orange column index `c_right` in `orange_cols` such that `c_right > c`.
        c.  If both checks (a and b) are true, change the color of the pixel at `(r, c)` in the output grid to azure (8).
    7.  **If the input pixel color is maroon (9):**
        a.  Check if the pixel to the immediate left, `(r, c-1)`, exists and its color in the input grid is orange (7).
        b.  Check if the pixel to the immediate right, `(r, c+1)`, exists and its color in the input grid is orange (7).
        c.  If both checks (a and b) are true, change the color of the pixel at `(r, c)` in the output grid to azure (8).
    8.  If neither of the above conditions (steps 6 or 7) caused a change, the pixel at `(r, c)` in the output grid retains its original color from the input grid.
    9.  After iterating through all pixels, the modified grid is the final output.
