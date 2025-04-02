
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 4 4 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 3 0 0
0 0 0 0 0 0
0 0 0 0 0 0
5 5 5 5 5 5
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
3 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 3 0 0
0 0 0 3 0 0
0 0 0 3 0 0
5 5 5 5 5 5
3 0 0 0 0 0
3 0 0 0 0 0
3 0 0 0 0 0
3 0 0 0 0 0
3 0 0 0 0 0
3 0 0 0 0 0
3 0 0 0 0 0
3 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception**

1.  **Core Elements**: The inputs contain a background (white, 0), one or more 'source' pixels of a distinct color (yellow, 4 in train_1; green, 3 in train_2), and a 'barrier' object made of gray pixels (5).
2.  **Barrier Structure**: In `train_1`, the barrier is a vertical gray line. In `train_2`, the barrier is a horizontal gray line.
3.  **Transformation**: The source pixels are extended or 'painted' towards the gray barrier. The extension stops just before hitting the barrier.
4.  **Extension Direction**:
    *   If the barrier is a vertical line, the extension happens horizontally (left or right) along the row of the source pixel.
    *   If the barrier is a horizontal line, the extension happens vertically (up or down) along the column of the source pixel.
5.  **Color Preservation**: The extended pixels take the color of the original source pixel. The barrier and background pixels remain unchanged.
6.  **Source Pixel Location**: The direction of extension depends on the source pixel's position relative to the barrier (e.g., left of a vertical barrier extends right, above a horizontal barrier extends down).

**YAML Facts**


```yaml
observations:
  - element: Grids
    description: Input and output are 2D grids of pixels with colors 0-9.
    properties:
      - background_color: white (0)
  - element: Barrier Object
    description: A contiguous object made of gray pixels (5).
    properties:
      - color: gray (5)
      - shape: Appears as a straight line (vertical or horizontal) in the examples.
      - role: Acts as a boundary for extension.
  - element: Source Pixels
    description: Isolated pixels with colors other than white (0) or gray (5).
    properties:
      - color: Variable (yellow/4 in train_1, green/3 in train_2)
      - count: Can be multiple per input grid.
      - role: Origin points for the extension action.
  - element: Transformation Action
    description: Extending source pixels towards the barrier object.
    properties:
      - direction: Determined by the orientation of the barrier and the relative position of the source pixel.
          - If barrier is vertical, extension is horizontal (towards the barrier).
          - If barrier is horizontal, extension is vertical (towards the barrier).
      - color: The extension uses the color of the source pixel.
      - stopping_condition: The extension stops one pixel away from the barrier.
  - element: Invariance
    description: Elements not part of the extension process remain unchanged.
    properties:
      - background pixels (white)
      - barrier pixels (gray)
relationships:
  - type: Spatial
    description: The position of a source pixel relative to the barrier determines the direction of extension (left/right or up/down).
  - type: Functional
    description: The orientation of the barrier (vertical/horizontal) determines the axis of extension (horizontal/vertical).
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the location and orientation (predominantly horizontal or vertical line) of the gray barrier object (color 5).
3.  Find all source pixels in the input grid (pixels that are not white (0) and not gray (5)).
4.  For each source pixel found:
    a.  Determine its color and position (row, column).
    b.  Based on the barrier's orientation:
        i.  **If the barrier is vertical** (at column `barrier_col`):
            *   If the source pixel's column is less than `barrier_col`, extend the source pixel's color horizontally to the right, filling cells in the same row from `source_col + 1` up to, but not including, `barrier_col`.
            *   If the source pixel's column is greater than `barrier_col`, extend the source pixel's color horizontally to the left, filling cells in the same row from `barrier_col + 1` up to `source_col - 1`.
        ii. **If the barrier is horizontal** (at row `barrier_row`):
            *   If the source pixel's row is less than `barrier_row`, extend the source pixel's color vertically downwards, filling cells in the same column from `source_row + 1` up to, but not including, `barrier_row`.
            *   If the source pixel's row is greater than `barrier_row`, extend the source pixel's color vertically upwards, filling cells in the same column from `barrier_row + 1` up to `source_row - 1`.
    c.  Update the output grid with these newly colored pixels.
5.  Return the final output grid.
