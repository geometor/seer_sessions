
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 3 3 0
0 3 0 0 0 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 0 0 0 3 0
0 3 0 0 0 0 0 4 0 0 0 0 3 0
0 3 0 0 0 0 0 0 0 0 0 0 3 0
0 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 3 3 0
0 3 0 0 0 0 0 4 0 0 0 0 3 0
0 3 0 0 0 0 0 4 0 0 0 0 3 0
0 3 0 0 0 0 0 4 0 0 0 0 3 0
0 3 0 0 0 0 0 4 0 0 0 0 3 0
0 3 0 0 0 0 0 4 0 0 0 0 3 0
0 3 0 0 0 0 0 4 0 0 0 0 3 0
0 3 0 0 0 0 0 4 0 0 0 0 3 0
0 3 0 0 0 0 0 4 0 0 0 0 3 0
0 3 4 4 4 4 4 4 4 4 4 4 3 0
0 3 0 0 0 0 0 4 0 0 0 0 3 0
0 3 3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 1 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 1 0
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 1 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 1 0
0 1 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 1 0
0 1 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 1 0
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, I will analyze the provided examples to understand the transformation rule.

**Perception of Task Elements:**

The input and output grids are of the same dimensions in both examples.
Each input grid features:
1.  An outer border of white pixels (0).
2.  An inner rectangular frame made of a single color (green=3 in train_1, blue=1 in train_2).
3.  An area inside the frame, mostly filled with white pixels (0).
4.  A single, uniquely colored pixel located within the inner white area (yellow=4 in train_1, magenta=6 in train_2). This seems to be the 'seed' or 'source' pixel.

The output grid retains the outer border and the inner frame exactly as they were in the input.
The transformation happens within the area bounded by the inner frame.
The single 'seed' pixel from the input appears to "project" its color horizontally and vertically within the inner area.
Specifically, all the white pixels (0) along the same row and same column as the seed pixel, but only *within* the boundaries set by the inner frame, are changed to the color of the seed pixel. The original seed pixel retains its color, and the frame pixels remain unchanged.

**YAML Facts:**


```yaml
task_description: Draw horizontal and vertical lines from a seed pixel within a framed area.
elements:
  - object: Background
    attributes:
      color: white (0)
      location: Outermost border pixels.
      persists: Yes, unchanged in output.
  - object: Frame
    attributes:
      color: Varies (e.g., green, blue)
      shape: Rectangle
      location: Forms an inner border inside the background.
      pixels: Contiguous pixels of the frame color.
      persists: Yes, unchanged in output.
  - object: Inner Area
    attributes:
      location: Bounded by the Frame.
      initial_color: Mostly white (0).
      transformation: Some white pixels change color.
  - object: Seed Pixel
    attributes:
      color: Varies (e.g., yellow, magenta), different from Frame and Background.
      location: A single pixel within the Inner Area.
      role: Source of the transformation color and location.
      persists: Yes, unchanged in output.
relationships:
  - type: containment
    object1: Seed Pixel
    relation: is inside
    object2: Inner Area
  - type: containment
    object1: Inner Area
    relation: is bounded by
    object2: Frame
  - type: boundary
    object1: Frame
    relation: separates
    object2: Inner Area
    object3: Background
actions:
  - action: identify
    target: Frame, Seed Pixel, Inner Area
  - action: project_color
    source: Seed Pixel
    direction: Horizontal and Vertical
    target: White pixels within the Inner Area
    constraint: Projection stops at the Frame boundary.
    effect: Changes target white pixels to the Seed Pixel's color.
```


**Natural Language Program:**

1.  Identify the grid boundaries.
2.  Identify the rectangular inner frame by finding the contiguous block of non-white pixels forming a border inside the grid. Note the frame's color and the coordinates defining the inner area it encloses.
3.  Scan the inner area (defined in step 2) to locate the single pixel whose color is neither white (0) nor the frame color. This is the 'seed' pixel. Note its color (`seed_color`) and its coordinates (`seed_row`, `seed_col`).
4.  Create a copy of the input grid to serve as the output grid.
5.  Iterate through all rows (`r`) within the inner area's row boundaries. For the pixel at (`r`, `seed_col`), if its color in the *input* grid is white (0), change its color in the *output* grid to `seed_color`.
6.  Iterate through all columns (`c`) within the inner area's column boundaries. For the pixel at (`seed_row`, `c`), if its color in the *input* grid is white (0), change its color in the *output* grid to `seed_color`.
7.  Return the modified output grid.
