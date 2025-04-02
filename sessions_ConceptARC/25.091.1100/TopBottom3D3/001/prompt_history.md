
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 1 2 2 2 1 1 0
0 0 2 2 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0
0 3 4 4 4 4 3 0
0 3 4 4 4 4 3 0
0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 0
0 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 6 0 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
7 7 7 6 7 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

*   **Perception of the Elements:**
    *   Each input grid contains a background of white pixels (0).
    *   There are two distinct non-white colored objects in each input grid.
    *   One object appears to be an "inner" shape (cross, rectangle, line).
    *   The second object acts as a "frame" or border around parts of the inner shape. The frame color is different from the inner shape color.
    *   In the output grid, the inner shape's pixels are replaced by the color of the frame object.
    *   The frame object itself remains unchanged in the output.
    *   The background pixels remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_description: Identify two distinct non-background colored objects. One object (frame) partially encloses the other (inner). Replace the pixels of the inner object with the color of the frame object.
    
    elements:
      - object: background
        color_property: white (0)
        role: static background
      - object: inner_shape
        color_property: varies (red, yellow, magenta in examples)
        topology: contiguous block of a single color, does not touch the grid edge directly in examples, enclosed by frame_shape and background.
        role: target for color replacement
      - object: frame_shape
        color_property: varies (blue, green, orange in examples), distinct from inner_shape color.
        topology: contiguous block of a single color, partially surrounds inner_shape, touches background (0).
        role: source color for replacement, remains unchanged in output.
    
    relationships:
      - type: spatial
        description: frame_shape partially encloses or borders inner_shape.
      - type: spatial
        description: frame_shape touches the background (0).
      - type: spatial
        description: inner_shape is surrounded by frame_shape and/or background (0), does not directly touch the grid boundary in examples (or touches less than frame_shape).
    
    actions:
      - action: identify_colors
        inputs: input_grid
        outputs: background_color (0), color1, color2
      - action: identify_frame_color
        inputs: input_grid, color1, color2
        outputs: frame_color
        logic: The color that has pixels adjacent to the background color (0) is the frame_color. (Alternative logic: Find bounding box of non-background colors; the color present at the edge of the bounding box is the frame_color).
      - action: identify_inner_color
        inputs: color1, color2, frame_color
        outputs: inner_color
        logic: The non-background color that is not the frame_color.
      - action: replace_color
        inputs: input_grid, inner_color, frame_color
        outputs: output_grid
        logic: Create a new grid where pixels matching inner_color in the input are changed to frame_color. All other pixels retain their original color.
    
    derived_properties:
      bounding_box: The minimum rectangle enclosing all non-background pixels. The frame_color pixels typically lie on the boundary of this box, while inner_color pixels are inside.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct colors present in the input grid besides the background color (white, 0). There will be exactly two such colors: `color_A` and `color_B`.
    2.  Determine which of these two colors, `color_A` or `color_B`, forms the "frame". The frame color is the one whose pixels are adjacent (horizontally or vertically) to background (white, 0) pixels. Assign this color to `frame_color`.
    3.  The other non-background color is the "inner" color. Assign this color to `inner_color`.
    4.  Create the output grid based on the input grid:
        *   For each pixel in the input grid:
            *   If the pixel's color is `inner_color`, set the corresponding output pixel's color to `frame_color`.
            *   Otherwise, keep the pixel's original color in the output grid.
