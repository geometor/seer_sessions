**Perception**

1.  **Grid Structure**: Both input and output grids are 10x10.
2.  **Background**: The background color is consistently white (0).
3.  **Objects**: Each input grid contains a single contiguous object composed of a non-white color (gray (5) in train_1, orange (7) in train_2).
4.  **Transformation**: The object's shape and color are preserved in the output grid. The transformation involves moving (translating) the entire object within the grid.
5.  **Translation Details**:
    *   In train_1, the gray 'plus' shape moves 3 cells to the right.
    *   In train_2, the orange 'L' shape moves 3 cells down.
6.  **Rule Determination**: The direction of the translation appears to depend on the object's initial position relative to the grid boundaries. Specifically, it relates to the position of the object's top-leftmost pixel. If this pixel is closer to the top edge than the left edge, the object moves down. If it's closer to or equidistant from the left edge compared to the top edge, the object moves right. The magnitude of the shift is consistently 3 cells in both examples.

**Facts**


```yaml
task_type: object_transformation
grid_properties:
  size: 10x10 # Constant across examples
  background_color: 0 # white
objects:
  - type: contiguous_shape
    color: non-white (varies: 5/gray, 7/orange)
    count: 1 per grid
transformation:
  type: translation
  preserve_shape: true
  preserve_color: true
  properties:
    - magnitude: 3 cells
    - direction: conditional
      condition: position_of_top_left_pixel (min_r, min_c)
      rules:
        - if: min_r < min_c  # Closer to top edge
          action: shift_down (delta_row = +3, delta_col = 0)
        - if: min_c <= min_r # Closer to or equidistant from left edge
          action: shift_right (delta_row = 0, delta_col = +3)
```


**Natural Language Program**

1.  Identify the single contiguous object composed of non-white pixels in the input grid.
2.  Determine the coordinates (row `min_r`, column `min_c`) of the top-leftmost pixel belonging to this object.
3.  Compare `min_r` and `min_c`.
4.  If `min_r` is less than `min_c`, determine the translation vector as (3 rows down, 0 columns across).
5.  If `min_c` is less than or equal to `min_r`, determine the translation vector as (0 rows down, 3 columns right).
6.  Create a new output grid of the same dimensions as the input, initialized with the background color (white).
7.  For every pixel belonging to the identified object in the input grid, copy its color to the corresponding position in the output grid, shifted according to the determined translation vector.