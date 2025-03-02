# e48d4e1a • 011 • example_2 • investigate_dreamer

---
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input and output grids are both 10x10.
*   The input grid has a cross-like shape formed by yellow (4) pixels. There's a single green(5) pixel in the top right corner, which is not relevant to the output.
*   The output grid has a vertical line of yellow (4) pixels on the leftmost column and a horizontal line of yellow (4) pixels at row 7.
* The cross shape is modified.

**YAML Block (Facts):**



```yaml
objects:
  - id: shape_1
    type: cross
    color: yellow
    initial_position:
      top_left: [0,3]
      bottom_right: [9,3]
      horizontal_top_left: [3,0]
      horizontal_bottom_right: [3,9]
    final_position:
      vertical_top_left: [0,0]
      vertical_bottom_right: [9,0]
      horizontal_top_left: [6,0]
      horizontal_bottom_right: [6,9]
  - id: pixel_5
    type: single_pixel
    color: green
    initial_position: [0,9]
    final_position: None

actions:
  - type: transformation
    object_id: shape_1
    description: >
      The vertical bar of the cross moves to the leftmost column,
      the horizontal bar moves to the row that is original horizontal bar index + 3

relationships:
  - type: part_of
    object_id: shape_1

```



**Natural Language Program:**

1.  Identify the cross shape formed by yellow (4) pixels in the input grid.
2.  Identify the vertical bar of the yellow cross.
3.  Move this vertical bar to the first column(index 0) of the output grid.
4.  Identify the horizontal bar of the yellow cross in input grid.
5.  Move this horizontal bar to the row = original horizontal bar index + 3.
6. Ignore any other pixels.

