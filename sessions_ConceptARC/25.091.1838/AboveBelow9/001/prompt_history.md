
## train_1

**input:**
```
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0
0 0 3 0 0 3 3 0 0 0 0 0
0 0 3 0 0 3 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 7 7 7 7 7 7 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7 0 0 0 0 0
```


**output:**
```
0 0 0 0 7 7 7 7 7 7 0 0 0 0 0
0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the task based on the provided examples.

**Perception**

1.  **Grid Structure:** Both input grids contain a single, solid horizontal line of yellow (4) pixels that spans the entire width.
2.  **Objects:** Besides the yellow line and the white (0) background, there are other colored objects (green - 3 in the first example, orange - 7 in the second). These objects appear both above and below the yellow line.
3.  **Transformation:** The core transformation seems to be related to the position of these other colored objects relative to the yellow horizontal line.
4.  **Selective Removal:** In the output grids, all the colored objects (green or orange) that were located *below* the yellow line in the input have been removed and replaced with the white (0) background color.
5.  **Preservation:** The yellow line itself and all colored objects located *above* the yellow line remain unchanged in the output.

The task appears to involve using the horizontal yellow line as a dividing boundary and clearing everything below it, except for the background itself.

**Facts**


```yaml
elements:
  - object: background
    color: white (0)
    role: canvas
  - object: horizontal_line
    color: yellow (4)
    properties:
      - spans full width
      - solid (no breaks)
      - exactly one instance per grid
    role: separator/boundary
  - object: other_pixels
    color: [green (3), orange (7)] # Any color other than background or line color
    properties:
      - can form contiguous shapes or be individual pixels
      - located above or below the horizontal_line
    role: content_to_be_filtered
relationships:
  - type: spatial
    description: other_pixels are either 'above' or 'below' the horizontal_line based on their row index compared to the line's row index.
actions:
  - action: identify
    target: horizontal_line
    purpose: find the row index of the separator.
  - action: iterate
    target: grid pixels
    condition: row index > horizontal_line row index
  - action: replace
    target: other_pixels below horizontal_line
    result: replaced with background color (white - 0)
  - action: preserve
    target:
      - horizontal_line
      - other_pixels above horizontal_line
      - background pixels
    result: remain unchanged
```


**Natural Language Program**

1.  Identify the single horizontal line composed entirely of yellow (4) pixels that spans the full width of the input grid. Determine the row index of this line.
2.  Create a copy of the input grid to serve as the output grid.
3.  Iterate through each pixel in the output grid located in rows *below* the identified yellow line's row.
4.  For each pixel in these lower rows, if its color is *not* the background color (white - 0), change its color to the background color (white - 0).
5.  Leave all pixels in rows *at or above* the yellow line (including the yellow line itself) unchanged from the input grid.
6.  Return the modified grid as the output.
