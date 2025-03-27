
## train_1

**input:**
```
9 6 5 7 7 7 7
8 7 1 7 7 7 7
0 8 9 7 7 7 7
7 7 7 7 7 7 7
7 7 7 1 8 4 7
7 7 7 4 7 6 7
7 7 7 6 2 4 7
```


**output:**
```
5 8 9 7 7 7 7
8 7 6 7 7 7 7
9 1 0 7 7 7 7
7 7 7 7 7 7 7
7 7 7 4 4 4 7
7 7 7 2 7 8 7
7 7 7 1 6 6 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7
7 7 7 7 7 7 7
7 7 5 2 8 7 7
7 7 1 7 9 7 7
7 7 4 3 0 7 7
7 7 7 7 7 7 7
7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7
7 7 7 7 7 7 7
7 7 8 1 0 7 7
7 7 3 7 2 7 7
7 7 5 9 4 7 7
7 7 7 7 7 7 7
7 7 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7
7 7 7 6 5 5 7
7 7 7 5 7 6 7
7 7 7 1 5 1 7
8 8 8 7 7 7 7
9 7 9 7 7 7 7
0 0 0 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7
7 7 7 5 5 1 7
7 7 7 5 7 5 7
7 7 7 6 6 1 7
8 9 0 7 7 7 7
0 7 8 7 7 7 7
8 9 0 7 7 7 7
```

Okay, let's break down this task.

## Perception

1.  **Grid Size:** The input and output grids are consistently the same size (7x7 in the examples).
2.  **Background Color:** The color orange (7) appears to be the background color, filling most of the grid and remaining unchanged in the output, except potentially within specific active regions.
3.  **Active Regions:** There are distinct clusters or components formed by non-orange pixels. In the examples, these components seem to fit within 3x3 bounding boxes.
    *   Example 1 has two such regions (top-left, bottom-right).
    *   Example 2 has one central region.
    *   Example 3 has two regions (top-right, bottom-left).
4.  **Transformation:** The changes between input and output occur exclusively within these 3x3 regions associated with the non-orange components.
5.  **Operation:** By comparing the input and output values within these 3x3 regions, a consistent pattern emerges: the 8 pixels on the perimeter of the 3x3 region appear to rotate counter-clockwise by one step, while the central pixel of the 3x3 region remains fixed.

    *   **Example 1 (Top-Left):**
        Input `[[9, 6, 5], [8, 7, 1], [0, 8, 9]]` becomes Output `[[5, 8, 9], [8, 7, 6], [9, 1, 0]]`.
        Corner `5` moves to `(0,0)`, corner `9` moves to `(2,0)`, corner `0` moves to `(2,2)`, corner `9` moves to `(0,2)`.
        Edge `6` moves to `(1,2)`, edge `1` moves to `(2,1)`, edge `8` moves to `(1,0)`, edge `8` moves to `(0,1)`.
        Center `7` stays at `(1,1)`. This confirms the counter-clockwise rotation of the perimeter around the center.
    *   This same rotation pattern holds true for all other identified 3x3 regions in the examples.

6.  **Identification of Regions:** The key seems to be identifying the correct 3x3 regions. They correspond precisely to the 3x3 bounding boxes of the connected components formed by non-orange pixels. Even if a pixel within that 3x3 bounding box is orange (like the central pixel in several examples), it participates in the transformation (or in the center's case, remains fixed).

## Facts


```yaml
task_context:
  grid_properties:
    - size_preservation: Input and output grids have the same dimensions.
    - background_color: Orange (7) acts as a static background.
  object_identification:
    - criteria: Connected components of non-orange pixels (using 8-way adjacency).
    - target_object_property: Components whose bounding box dimensions are exactly 3x3.
transformation:
  locality: Changes occur only within the 3x3 bounding boxes of the identified target objects.
  rule:
    - type: Rotation (within the 3x3 bounding box)
    - direction: Counter-clockwise
    - elements: The 8 perimeter pixels of the 3x3 box.
    - invariant: The central pixel of the 3x3 box remains unchanged.
  application: Apply this rotation independently to each identified 3x3 target region.
  default_behavior: Pixels outside the identified 3x3 target regions remain unchanged.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the background color as orange (7).
3.  Find all connected components of pixels that are *not* the background color, using 8-way adjacency (pixels are connected if they touch horizontally, vertically, or diagonally).
4.  For each distinct component found:
    a. Calculate its bounding box (the smallest rectangle containing all pixels of the component).
    b. Check if the height and width of the bounding box are both exactly 3.
    c. If the bounding box is 3x3:
        i.  Let (R, C) be the top-left coordinates of this 3x3 bounding box in the grid.
        ii. Store the values of the 8 perimeter pixels of this 3x3 subgrid from the *input* grid:
            - Top-Left: `input[R][C]`
            - Top-Center: `input[R][C+1]`
            - Top-Right: `input[R][C+2]`
            - Middle-Left: `input[R+1][C]`
            - Middle-Right: `input[R+1][C+2]`
            - Bottom-Left: `input[R+2][C]`
            - Bottom-Center: `input[R+2][C+1]`
            - Bottom-Right: `input[R+2][C+2]`
        iii. Update the corresponding perimeter cells in the *output* grid by rotating the stored values one step counter-clockwise:
            - `output[R][C]` = Top-Right value
            - `output[R][C+1]` = Middle-Left value
            - `output[R][C+2]` = Bottom-Right value
            - `output[R+1][C]` = Bottom-Center value
            - `output[R+1][C+2]` = Top-Center value
            - `output[R+2][C]` = Top-Left value
            - `output[R+2][C+1]` = Middle-Right value
            - `output[R+2][C+2]` = Bottom-Left value
        iv. The central cell `output[R+1][C+1]` remains unchanged (it keeps the value from the initial copy of the input grid).
5.  Return the modified output grid.
