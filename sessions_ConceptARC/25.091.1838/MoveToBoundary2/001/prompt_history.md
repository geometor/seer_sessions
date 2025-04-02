
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 7 0
0 7 0 0 0 7 0 0 7 0
0 7 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 7 0
0 7 0 0 0 7 0 0 7 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
```

*   **Perception:**
    The task involves applying a gravity-like effect to all non-white pixels within the grid. In all provided examples, the only non-white pixels are orange (color 7). These orange pixels "fall" downwards within their respective columns until they either reach the bottom edge of the grid or land on top of another orange pixel in the same column. The white pixels (color 0) remain unchanged and act as empty space through which the orange pixels can fall. The relative horizontal positions of the orange pixels within their columns are maintained.

*   **Facts:**
    
```yaml
    task_type: gravity_simulation
    components:
      - role: background
        element: pixels
        color_value: 0
        color_name: white
        behavior: static
      - role: falling_object
        element: pixels
        color_value: 7
        color_name: orange
        behavior: move_down
    actions:
      - type: apply_gravity
        target: falling_object
        direction: down
        constraints:
          - stop_condition: grid_bottom_edge
          - stop_condition: encountering_another_falling_object_pixel_below
    grid_properties:
      - size: constant_between_input_output
      - coordinate_system: row_major (y, x)
    invariance:
      - background_pixels_remain_unchanged
      - horizontal_position_of_falling_pixels_within_columns_is_preserved
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through the columns of the grid from left to right (index `c`).
    3.  Within each column, iterate through the rows from bottom to top (index `r` from `height - 1` down to `0`).
    4.  If the pixel at `(r, c)` in the output grid is orange (7):
        a.  Look downwards from the current row `r` (starting at `r + 1`) within the same column `c` to find the first available white (0) pixel position before hitting the grid bottom or another orange pixel. Let this lowest available white pixel row be `target_r`.
        b.  If a lower white pixel position `target_r` is found (meaning `target_r > r` and the cell at `(target_r, c)` is white), move the orange pixel:
            i.  Set the pixel at `(target_r, c)` in the output grid to orange (7).
            ii. Set the original pixel position `(r, c)` in the output grid to white (0).
    5.  Repeat step 3 and 4 until no more orange pixels can be moved downwards in any column. Alternatively, processing columns from bottom-to-top ensures pixels settle correctly in one pass. A simpler iterative approach: Repeatedly scan the grid and move any orange pixel down one step if the cell below it is white, until a full scan results in no movements.
    6.  Return the modified output grid.
