
## train_1

**input:**
```
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0
0 0 2 0 3 0 0 2 0 0 0 0
0 0 2 0 3 0 0 2 0 0 0 0
3 3 2 3 3 3 3 2 3 3 3 3
0 0 2 0 3 0 0 2 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
3 3 2 2 2 2 2 2 3 3 3 3
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0
0 0 1 0 0 8 0 0 1 0 0 0
0 0 1 0 0 8 0 0 1 0 0 0
8 8 1 8 8 8 8 8 1 8 8 8
0 0 1 0 0 8 0 0 1 0 0 0
0 0 1 0 0 8 0 0 1 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
8 8 1 1 1 1 1 1 1 8 8 8
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 3 0 4 0 3 0 0 0
4 4 4 4 3 4 4 4 3 4 4 4
0 0 0 0 3 0 4 0 3 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
4 4 4 4 3 3 3 3 3 4 4 4
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
```

*   **Perception:**
    *   Each input grid contains a large central shape composed of a single color (red, blue, or green). Let's call this the "main shape". The background is white (0).
    *   Another color (green, azure, or yellow respectively) appears as pixels both inside the boundary of the main shape and outside the boundary. Let's call this the "active color".
    *   The active color pixels outside the main shape form simple linear patterns, either extending vertically within the columns spanned by the main shape, or horizontally within the rows spanned by the main shape.
    *   In the output grid, the main shape remains unchanged in color and position.
    *   The active color pixels that were *inside* the main shape in the input are removed (changed to white) in the output.
    *   The active color pixels that were *outside* the main shape in the input are moved to new locations in the output. Their original locations become white.
    *   The movement depends on the alignment relative to the main shape's bounding box:
        *   Active pixels in columns spanned by the main shape (but rows outside it) move 3 columns to the right.
        *   Active pixels in rows spanned by the main shape (but columns outside it) move vertically to align with the top edge (minimum row) of the main shape.

*   **YAML Facts:**
    
```yaml
    task_context:
      grid_properties:
        - size: 12x12 (consistent across examples)
        - background_color: white (0)
      main_components:
        - object: main_shape
          description: A large contiguous shape of a single color (non-white, non-active).
          properties:
            - color: Varies (red, blue, green in examples)
            - location: Central area of the grid
            - stability: Unchanged between input and output
            - role: Acts as a spatial boundary or mask.
        - object: active_pixels
          description: Pixels of a single color appearing both inside and outside the main_shape.
          properties:
            - color: Varies (green, azure, yellow in examples) but consistent within a pair.
            - location: Dispersed, some inside main_shape, some outside.
            - configuration_outside: Forms vertical or horizontal line segments relative to the main_shape's bounding box.
    transformation:
      actions:
        - action: identify_main_shape_and_color
          input: input_grid
          output: main_shape_object, main_shape_color
        - action: identify_active_color
          input: input_grid, main_shape_object
          condition: Find color present both inside and outside main_shape bounds.
          output: active_color_value
        - action: identify_main_shape_bounding_box
          input: main_shape_object
          output: min_row, max_row, min_col, max_col
        - action: process_pixels
          input: input_grid, main_shape_color, active_color_value, bounding_box
          output: output_grid
          sub_actions:
            - step: Initialize output_grid as a copy of input_grid.
            - step: Iterate through each pixel (r, c) of the input_grid.
            - step: If input_grid[r, c] == active_color_value:
                - condition: Pixel (r, c) is inside the main_shape (or its bounding box).
                  effect: Set output_grid[r, c] = white (0).
                - condition: Pixel (r, c) is outside the main_shape bounding box.
                  effect:
                    - Set output_grid[r, c] = white (0). # Remove from original position
                    - sub_condition: Pixel is vertically aligned (min_col <= c <= max_col).
                      target_location: (r, c + 3)
                    - sub_condition: Pixel is horizontally aligned (min_row <= r <= max_row).
                      target_location: (min_row, c)
                    - effect: Set output_grid[target_location] = active_color_value. # Place at new position
            - step: If input_grid[r, c] != active_color_value (i.e., main_shape color or background):
                - effect: Keep the pixel as is (output_grid[r, c] = input_grid[r, c]). # Already handled by copy

    ```


*   **Natural Language Program:**
    1.  Identify the main solid shape in the input grid (the largest contiguous object of a single color, excluding the background color 0/white). Note its color.
    2.  Identify the "active color" - this is the color that appears in pixels both *inside* the area covered by the main shape and *outside* it.
    3.  Determine the bounding box of the main shape (minimum row, maximum row, minimum column, maximum column).
    4.  Create the output grid, initially identical to the input grid.
    5.  Iterate through each pixel of the input grid at position (row `r`, column `c`).
    6.  If the pixel's color is the active color:
        a.  Check if the pixel's position (r, c) is within the bounding box of the main shape (`min_row <= r <= max_row` AND `min_col <= c <= max_col`).
        b.  If it is inside the bounding box, change the color of the pixel at (r, c) in the *output* grid to white (0).
        c.  If it is outside the bounding box:
            i.  Change the color of the pixel at (r, c) in the *output* grid to white (0) (erase from original position).
            ii. Determine the target position:
                *   If the pixel's column `c` is within the main shape's column range (`min_col <= c <= max_col`), the target position is (`r`, `c + 3`).
                *   If the pixel's row `r` is within the main shape's row range (`min_row <= r <= max_row`), the target position is (`min_row`, `c`).
            iii. Change the color of the pixel at the calculated target position in the *output* grid to the active color.
    7.  Pixels that are part of the main shape or the background (not the active color) remain unchanged from the input grid (this is implicitly handled by initializing the output grid as a copy and only modifying active color pixels).
    8.  Return the modified output grid.
