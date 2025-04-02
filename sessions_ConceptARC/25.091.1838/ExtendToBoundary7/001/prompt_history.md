
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

Okay, analyzing the provided examples.

**Perception of Elements:**

*   **Input Grids:** The input grids contain a background of white pixels (0), a single straight line of gray pixels (5) (either horizontal or vertical), and one or more isolated colored pixels (non-white, non-gray).
*   **Output Grids:** The output grids retain the white background and the gray line from the input. The key change is that the isolated colored pixels from the input have been extended into lines.
*   **Transformation:** The colored pixels in the input act as starting points. Lines of the same color are drawn from these starting points towards the gray line.
    *   If the gray line is vertical, horizontal lines are drawn from the colored pixels towards the gray line, stopping one pixel away from it.
    *   If the gray line is horizontal, vertical lines are drawn from the colored pixels towards the gray line, stopping one pixel away from it.
    *   Pixels to the left of a vertical gray line draw lines to the right. Pixels to the right draw lines to the left.
    *   Pixels above a horizontal gray line draw lines downwards. Pixels below draw lines upwards.
*   **Objects:** The primary objects are the gray line (barrier) and the colored source pixels.
*   **Relationships:** The core relationship is the position of the source pixels relative to the gray barrier, which determines the direction and extent of the drawn lines.

**Facts:**


```yaml
task_description: Draw lines from colored pixels towards a central gray barrier line.
grid_properties:
  - background_color: 0 (white)
objects:
  - type: barrier_line
    color: 5 (gray)
    shape: straight line (either horizontal or vertical)
    role: Acts as a boundary for drawing lines.
  - type: source_pixel
    color: Any color except 0 (white) and 5 (gray).
    shape: single pixel
    role: Starting point for drawing lines.
relationships:
  - type: relative_position
    object1: source_pixel
    object2: barrier_line
    description: The position of a source pixel relative to the barrier line (above/below or left/right) determines the drawing direction.
actions:
  - type: find_barrier
    description: Locate the gray (5) line and determine its orientation (horizontal/vertical) and index (row/column).
  - type: find_sources
    description: Locate all pixels that are not white (0) or gray (5).
  - type: draw_line
    actor: source_pixel
    target: position adjacent to barrier_line
    properties:
      - color: Same as the source_pixel.
      - direction: Perpendicular to the barrier_line, moving from the source_pixel towards the barrier_line.
      - extent: From the source_pixel up to, but not including, the barrier_line.
output_grid:
  - composition: Input grid modified by the 'draw_line' actions. The barrier_line and background remain unchanged except where lines are drawn.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the single, continuous line of gray pixels (color 5). Determine if this line is horizontal or vertical, and note its row or column index (let's call it the "barrier index").
3.  Find all pixels in the input grid whose color is neither white (0) nor gray (5). These are the "source pixels".
4.  For each source pixel found:
    a.  Get its color (let's call it "source color") and its position (row, col).
    b.  If the gray barrier line is horizontal (at row `barrier_index`):
        i.  If the source pixel's row is less than `barrier_index` (it's above the barrier), fill all pixels in the same column (`col`) from `row` down to `barrier_index - 1` with the `source_color`.
        ii. If the source pixel's row is greater than `barrier_index` (it's below the barrier), fill all pixels in the same column (`col`) from `barrier_index + 1` up to `row` with the `source_color`.
    c.  If the gray barrier line is vertical (at column `barrier_index`):
        i.  If the source pixel's column is less than `barrier_index` (it's left of the barrier), fill all pixels in the same row (`row`) from `col` right to `barrier_index - 1` with the `source_color`.
        ii. If the source pixel's column is greater than `barrier_index` (it's right of the barrier), fill all pixels in the same row (`row`) from `barrier_index + 1` left to `col` with the `source_color`.
5.  Return the modified output grid.
