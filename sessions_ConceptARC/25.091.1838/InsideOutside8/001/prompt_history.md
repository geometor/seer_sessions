
## train_1

**input:**
```
0 0 0 0 0 3 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 3 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 3
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 3 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 4 4 4 4 4 4 4 4 0
3 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
6 0 0 0 0 0 0 0 0 0 6
0 6 0 0 8 0 0 0 0 6 0
0 0 6 0 0 8 0 0 6 0 0
0 0 0 6 0 0 0 6 0 0 0
0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 8 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

## Perception of Elements

1.  **Grid Structure:** Both input and output are 2D grids of pixels with different colors. The grid dimensions remain constant between input and output for each example.
2.  **Colors:** Each example uses three colors: white (0) as the background, one color forming a prominent shape or boundary (yellow/4 in train_1, magenta/6 in train_2), and another color representing points or small objects (green/3 in train_1, azure/8 in train_2).
3.  **Boundary Shape:** In both examples, one color (yellow or magenta) forms a structure that seems to enclose or delineate a region within the grid. In train_1, it's a clear 'U' shape. In train_2, it's a more scattered but still somewhat containing shape.
4.  **Target Points:** The other color (green or azure) appears as scattered individual pixels or very small clusters.
5.  **Transformation:** The core transformation involves selectively keeping some of the 'target points' based on their relationship to the 'boundary shape'. Specifically, target points that appear to be *inside* the region defined by the boundary shape are retained in the output, while target points *outside* this region are removed (turned to white). The boundary shape itself is also removed in the output, replaced by the background color (white).
6.  **Defining 'Inside':** The concept of 'inside' seems related to connectivity. Points are 'inside' if they are in an area that is separated from the grid's outer border by the boundary shape. A flood fill starting from the outside (grid edges) and stopping at the boundary color would likely fail to reach the 'inside' points.

## YAML Facts


```yaml
task_description: Keep only the target-colored pixels that are located inside the region defined by the boundary-colored shape. Replace everything else, including the boundary shape itself, with the background color.

elements:
  - object: Grid
    properties:
      - type: 2D array
      - pixels: contain color values (0-9)
      - dimensions: consistent between input and output

  - object: Background
    properties:
      - color: white (0)
      - role: fills most of the output grid and areas outside the boundary in the input

  - object: Boundary Shape
    properties:
      - color: distinct non-background color (e.g., yellow/4, magenta/6)
      - shape: forms a connected or semi-connected structure
      - role: defines an 'inside' and 'outside' region within the grid
      - persistence: removed in the output

  - object: Target Points
    properties:
      - color: distinct non-background color, different from boundary color (e.g., green/3, azure/8)
      - shape: typically individual pixels or small clusters
      - location: scattered across the grid
      - role: points to be selectively kept or removed
      - persistence: kept only if located 'inside' the boundary region, otherwise removed

relationships:
  - type: containment
    description: Target points are classified as either 'inside' or 'outside' the region defined by the Boundary Shape.
  - type: transformation_rule
    description: The output grid retains only the 'inside' Target Points at their original locations, set against the Background color. The Boundary Shape is removed.

determination_of_inside:
  - method: Flood Fill Inversion
    steps:
      - Identify Boundary Color pixels.
      - Perform a flood fill starting from all Background pixels on the grid's border.
      - The fill propagates to adjacent Background pixels but cannot cross Boundary Color pixels.
      - Mark all pixels reached by the flood fill as 'outside'.
      - Any non-Boundary, non-Background pixel *not* marked as 'outside' is considered 'inside'.
```


## Natural Language Program

1.  Create an output grid with the same dimensions as the input grid, initially filled entirely with the background color (white, 0).
2.  Identify the 'boundary color' (the color forming the main enclosing shape, e.g., yellow in train_1, magenta in train_2) and the 'target color(s)' (the color(s) of the scattered points, e.g., green in train_1, azure in train_2).
3.  Determine the 'outside' region of the input grid:
    a.  Create a boolean grid (or marker set) of the same size as the input, initialized to `false`.
    b.  Initialize a queue with the coordinates of all background-colored (white, 0) pixels located on the outermost border (row 0, last row, column 0, last column) of the input grid. Mark these initial coordinates as `true` in the boolean grid.
    c.  While the queue is not empty:
        i.  Dequeue a coordinate `(r, c)`.
        ii. For each neighbor `(nr, nc)` (adjacent horizontally or vertically) of `(r, c)`:
            - If `(nr, nc)` is within the grid bounds, is *not* the 'boundary color' in the input grid, and is marked `false` in the boolean grid:
                - Mark `(nr, nc)` as `true` in the boolean grid.
                - Enqueue `(nr, nc)`.
    d.  The pixels marked `true` in the boolean grid now represent the 'outside' region reachable from the border without crossing the boundary shape.
4.  Iterate through each pixel `(r, c)` of the input grid:
    a.  If the color of the input pixel `input[r][c]` is a 'target color' AND the corresponding location `(r, c)` is marked `false` in the boolean grid (meaning it's *not* 'outside', therefore it's 'inside'):
        i.  Set the corresponding pixel in the output grid `output[r][c]` to the 'target color' found in `input[r][c]`.
5.  Return the completed output grid.
