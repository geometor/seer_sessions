
## train_1

**input:**
```
4 4 4 2 4 4 4
4 4 4 2 4 1 4
4 4 4 2 4 4 4
2 2 2 2 2 2 2
4 4 4 2 4 4 4
4 4 4 2 4 4 4
4 4 4 2 4 4 4
```


**output:**
```
4 4 4
4 1 4
4 4 4
```


## train_2

**input:**
```
8 8 3 8 8
8 8 3 8 8
3 3 3 3 3
8 8 3 8 8
4 8 3 8 8
```


**output:**
```
8 8
4 8
```


## train_3

**input:**
```
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 8 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
1 1 1 1 1 1 1 1 1 1 1
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
```


**output:**
```
3 3 3 3 3
3 3 3 3 3
3 8 3 3 3
3 3 3 3 3
3 3 3 3 3
```

Okay, let's break down this task.

**Perception:**

1.  **Input Grid Structure:** Each input grid features a prominent "cross" shape composed of a single horizontal line and a single vertical line, both spanning the full width and height of the grid, respectively. These lines always intersect near the center of the grid and are made of the same color.
2.  **Background Color:** The areas separated by the cross are filled with a consistent background color.
3.  **Unique Pixel:** Within one of the four quadrants defined by the cross, there exists a single pixel of a unique color, different from both the cross color and the background color.
4.  **Output Grid:** The output grid is always a rectangular subgrid extracted from the input grid.
5.  **Transformation Logic:** The key observation is that the output grid corresponds exactly to the quadrant of the input grid (as defined by the cross) that contains the unique pixel. The size and content of the output are determined by the boundaries of that specific quadrant.

**Facts:**


```yaml
elements:
  - role: input_grid
    description: A 2D grid of pixels with height H and width W.
  - role: cross
    description: An object within the input grid composed of a single horizontal line spanning width W and a single vertical line spanning height H.
    properties:
      - color: A single color C_cross, consistent for both lines.
      - location: The lines intersect at a central point (r_cross, c_cross).
      - function: Divides the grid into four quadrants (excluding the cross lines themselves).
  - role: background
    description: The pixels filling the quadrants, not part of the cross or the unique pixel.
    properties:
      - color: A single color C_bg, distinct from C_cross.
  - role: unique_pixel
    description: A single pixel within the input grid.
    properties:
      - color: A single color C_unique, distinct from C_cross and C_bg.
      - count: Exactly one pixel of this color exists in the grid.
      - location: Resides within one of the four quadrants defined by the cross at coordinates (r_unique, c_unique).
  - role: output_grid
    description: A 2D grid of pixels, representing a subgrid of the input_grid.
    properties:
      - content: Matches the pixels of the input_grid quadrant containing the unique_pixel.
      - size: Determined by the dimensions of the quadrant containing the unique_pixel.

relationships:
  - type: identifies
    subject: cross
    object: quadrants
    details: The horizontal line at r_cross and vertical line at c_cross define the boundaries between the top-left, top-right, bottom-left, and bottom-right quadrants.
  - type: determines
    subject: unique_pixel
    object: output_grid
    details: The location (quadrant) of the unique_pixel dictates which quadrant subgrid from the input becomes the output_grid.

actions:
  - step: 1
    action: Identify_Cross
    inputs: input_grid
    outputs: r_cross, c_cross, C_cross
    description: Find the row index (r_cross) of the full horizontal line and the column index (c_cross) of the full vertical line, and their color (C_cross).
  - step: 2
    action: Identify_Unique_Pixel
    inputs: input_grid, C_cross
    outputs: r_unique, c_unique, C_unique
    description: Find the coordinates (r_unique, c_unique) and color (C_unique) of the pixel whose color appears exactly once and is not C_cross.
  - step: 3
    action: Determine_Quadrant
    inputs: r_cross, c_cross, r_unique, c_unique
    outputs: quadrant_boundaries
    description: Compare (r_unique, c_unique) with (r_cross, c_cross) to determine which quadrant the unique pixel is in (top-left, top-right, bottom-left, bottom-right) and calculate the row/column boundaries of that quadrant.
      - Top-Left: [0, r_cross), [0, c_cross)
      - Top-Right: [0, r_cross), [c_cross + 1, W)
      - Bottom-Left: [r_cross + 1, H), [0, c_cross)
      - Bottom-Right: [r_cross + 1, H), [c_cross + 1, W)
  - step: 4
    action: Extract_Subgrid
    inputs: input_grid, quadrant_boundaries
    outputs: output_grid
    description: Extract the subgrid from the input_grid defined by the calculated quadrant_boundaries.
```


**Natural Language Program:**

1.  Examine the input grid to find the single horizontal line and the single vertical line that span the grid's width and height, respectively. Record the row index (`r_cross`) of the horizontal line and the column index (`c_cross`) of the vertical line. These lines form a cross.
2.  Identify the pixel in the input grid whose color is unique (appears only once). Record its row index (`r_unique`) and column index (`c_unique`).
3.  Compare the unique pixel's coordinates (`r_unique`, `c_unique`) with the cross's intersection coordinates (`r_cross`, `c_cross`) to determine which quadrant it falls into:
    *   If `r_unique < r_cross` and `c_unique < c_cross`, it's the Top-Left quadrant.
    *   If `r_unique < r_cross` and `c_unique > c_cross`, it's the Top-Right quadrant.
    *   If `r_unique > r_cross` and `c_unique < c_cross`, it's the Bottom-Left quadrant.
    *   If `r_unique > r_cross` and `c_unique > c_cross`, it's the Bottom-Right quadrant.
4.  Define the boundaries of the selected quadrant based on the input grid's dimensions (Height `H`, Width `W`) and the cross intersection (`r_cross`, `c_cross`):
    *   Top-Left: Rows 0 to `r_cross - 1`, Columns 0 to `c_cross - 1`.
    *   Top-Right: Rows 0 to `r_cross - 1`, Columns `c_cross + 1` to `W - 1`.
    *   Bottom-Left: Rows `r_cross + 1` to `H - 1`, Columns 0 to `c_cross - 1`.
    *   Bottom-Right: Rows `r_cross + 1` to `H - 1`, Columns `c_cross + 1` to `W - 1`.
5.  Extract the subgrid from the input grid corresponding to these calculated row and column boundaries. This subgrid is the final output.
