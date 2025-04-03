
## train_1

**input:**
```
0 0 5 5 5 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 9 9 9 0 0 0 8 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 9 9 9 0 0 8 8 8 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 3 3 3 0 0 0 2 0 0 0 0 7 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 0 0 2 2 2 0 0 7 7 7 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The input grids contain horizontal lines of length 3 and single dots (1x1 pixels) of various non-white colors, all located on the top row. The background is white (0).

The transformation rule appears to operate on the single dots. Each dot is replaced by a horizontal line of length 3, using the same color as the original dot. The center of the new line coincides with the column of the original dot. Existing horizontal lines of length 3 remain unchanged in the output.

**Facts:**


```yaml
task_context:
  - grid_dimensions: All examples use a 1xN grid (single row).
  - background_color: white (0).
  - elements:
      - type: object
        subtype: horizontal_line
        properties:
          - color: non-white (gray, maroon, green)
          - size: 1x3
          - location: top row
      - type: object
        subtype: dot
        properties:
          - color: non-white (red, azure, maroon, orange, blue)
          - size: 1x1
          - location: top row
transformation:
  - action: identify
    target: single non-white dots (1x1 pixels)
    condition: surrounded by white pixels horizontally (or grid boundary)
  - action: replace
    target: identified single dots
    result:
      - type: horizontal_line
      - properties:
          - color: same as the original dot
          - size: 1x3
          - location: centered horizontally at the original dot's column position
  - action: preserve
    target: existing horizontal lines (1x3 non-white pixels)
    result: no change
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each pixel in the input grid's row.
3.  If a pixel is non-white (not 0) and is a single dot (i.e., its horizontal neighbors within the grid boundaries are white), then:
    a.  Identify the color of the dot.
    b.  Identify the column index of the dot.
    c.  In the output grid, change the pixel at the column index `c` and its horizontal neighbors (column `c-1` and `c+1`, if within grid bounds) to the color of the original dot.
4.  Leave all other pixels (background white pixels and pixels belonging to existing horizontal lines of length 3) unchanged.
5.  Return the modified output grid.
