
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 8 6 8 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 8 6 8 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 6 0 8 0 6 0 0 0 0 0 0
0 0 6 8 6 0 0 0 0 0 0 0
0 8 8 6 8 8 0 0 0 0 0 0
0 0 6 8 6 0 0 0 0 0 0 0
0 6 0 8 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 8 0 6 0
0 0 0 0 0 0 0 6 8 6 0 0
0 0 0 0 0 0 8 8 6 8 8 0
0 0 0 0 0 0 0 6 8 6 0 0
0 0 0 0 0 0 6 0 8 0 6 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 7 2 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 2 7 0 0
0 0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
2 0 7 0 2 0 0 0 0 0 0 0
0 2 7 2 0 0 0 0 0 0 0 0
7 7 2 7 7 0 0 0 0 0 0 0
0 2 7 2 0 0 0 0 0 0 0 0
2 0 7 0 2 0 2 0 7 0 2 0
0 0 0 0 0 0 0 2 7 2 0 0
0 0 0 0 0 0 7 7 2 7 7 0
0 0 0 0 0 0 0 2 7 2 0 0
0 0 0 0 0 0 2 0 7 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the task based on the provided examples.

**Perception**

1.  **Input Structure:** The input grids contain one or more distinct shapes set against a white background (color 0). In both examples, these shapes are identical "plus" or "cross" patterns.
2.  **Object Composition:** Each cross shape consists of a central pixel of one color (magenta 6 in train_1, red 2 in train_2) and four adjacent pixels (up, down, left, right) of another color (azure 8 in train_1, orange 7 in train_2).
3.  **Output Structure:** The output grids retain the original cross shapes from the input. Additionally, new pixels are added around each cross shape.
4.  **Transformation Pattern:** The new pixels appear at specific locations relative to the center of each cross. Observing their positions, they consistently match the eight possible "knight's moves" in chess (two steps in one cardinal direction and one step perpendicularly) starting from the central pixel of the cross.
5.  **Color Rule:** The color of the newly added pixels is identical to the color of the *central* pixel of the corresponding cross shape (magenta 6 in train_1, red 2 in train_2).
6.  **Multiple Objects:** The transformation is applied independently to each identified cross shape in the input.

**Facts**


```yaml
task_type: pattern_completion
input_elements:
  - type: background
    color: white
  - type: object
    shape: cross (3x3, center + 4 adjacent)
    properties:
      - center_pixel:
          color: C1 (e.g., magenta, red)
          location: (row, col)
      - arm_pixels:
          color: C2 (e.g., azure, orange)
          location: adjacent to center
output_elements:
  - type: background
    color: white
  - type: object (original cross)
    shape: cross
    properties: (same as input)
  - type: added_pixels
    count: 8 per cross object
    color: C1 (same as center_pixel of corresponding cross)
    placement: knight's move positions relative to the center_pixel of the cross
relationships:
  - The transformation identifies specific 'cross' objects in the input.
  - For each cross object, the color of its central pixel (C1) determines the color of the pixels to be added.
  - The location of the central pixel determines the anchor point for placing the added pixels.
  - Added pixels are placed at locations defined by a fixed geometric offset (knight's move) from the anchor point.
actions:
  - Identify cross objects based on shape and color pattern.
  - For each identified cross:
    - Get the center pixel's color (C1) and location (row, col).
    - Calculate the 8 knight's move coordinates relative to (row, col).
    - Place pixels of color C1 at these calculated coordinates in the output grid, ensuring they are within bounds.
  - Copy the original input grid content to the output grid. (The new pixels are added without removing original content).

```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each pixel of the input grid to find potential centers of cross shapes. A potential center is a non-white pixel.
3.  For each potential center pixel at `(row, col)` with color `C1`:
    a.  Check its four cardinal neighbors (up, down, left, right).
    b.  Verify if all four neighbors exist, are within the grid boundaries, are non-white, and share the *same* color `C2`, where `C2` is different from `C1`.
    c.  Verify that the diagonal neighbors of the center pixel are white (color 0). This confirms the specific 3x3 cross shape without filled corners.
4.  If a pixel at `(row, col)` with color `C1` is confirmed as the center of a cross shape:
    a.  Define the eight knight's move offsets: `(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)`.
    b.  For each offset `(dr, dc)`:
        i.  Calculate the target coordinates: `(new_row, new_col) = (row + dr, col + dc)`.
        ii. Check if `(new_row, new_col)` is within the grid boundaries.
        iii. If it is within bounds, set the pixel at `(new_row, new_col)` in the *output* grid to color `C1`.
5.  Return the modified output grid.
