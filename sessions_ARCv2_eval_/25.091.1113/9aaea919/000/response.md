*   **Perception of task elements:**
    *   The input and output grids are the same size (30x30).
    *   Each grid has a dominant background color (Orange=7 in train\_1, Blue=1 in train\_2, Magenta=6 in train\_3).
    *   The input grids contain multiple distinct objects, primarily 5-pixel plus-shapes (+) and 5-pixel horizontal lines (-).
    *   The transformation involves selective removal of some objects and color changes of others, while leaving the rest unchanged.
    *   Specifically, horizontal line objects of certain colors (Red=2, Green=3) are removed (replaced by the background color).
    *   Plus-shaped objects of certain colors (Maroon=9, Magenta=6, Green=3) are changed to Gray (5).
    *   Other plus-shaped objects retain their original colors.

*   **YAML facts:**
    
```yaml
    background_color:
      description: The dominant color filling most of the grid.
      input_train_1: 7 # Orange
      output_train_1: 7 # Orange
      input_train_2: 1 # Blue
      output_train_2: 1 # Blue
      input_train_3: 6 # Magenta
      output_train_3: 6 # Magenta
      transformation: Remains unchanged.
    objects:
      description: Contiguous blocks of non-background colors.
      types:
        - shape: plus # 5 pixels in a '+' configuration
        - shape: horizontal_line # 5 pixels in a '-' configuration
      actions:
        - condition:
            shape: horizontal_line
            color: [2, 3] # Red, Green
          effect: remove # Replace with background color
        - condition:
            shape: plus
            color: [9, 6, 3] # Maroon, Magenta, Green
          effect: change_color # Replace color with Gray (5)
        - condition:
            shape: plus
            color: [0, 1, 2, 4, 7, 8] # White, Blue, Red, Yellow, Orange, Azure
          effect: keep # No change
    grid_size:
      description: Dimensions of the input and output grids.
      value: 30x30
      transformation: Remains unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify the background color of the input grid (the most frequent color).
    2.  Create an output grid initialized with the same background color and dimensions as the input grid.
    3.  Find all distinct objects (contiguous groups of pixels with the same non-background color) in the input grid.
    4.  For each identified object:
        a.  Determine the shape of the object.
        b.  Determine the color of the object.
        c.  If the object is a 5-pixel horizontal line and its color is Red (2) or Green (3), do nothing (it remains background color in the output).
        d.  If the object is a 5-pixel plus-shape and its color is Maroon (9), Magenta (6), or Green (3), copy the object's shape to the corresponding position in the output grid, but change its color to Gray (5).
        e.  If the object is a 5-pixel plus-shape and its color is *not* Maroon (9), Magenta (6), or Green (3), copy the object (shape and original color) to the corresponding position in the output grid.
        f.  Ignore any other object shapes or colors not explicitly mentioned above (though none appear in the examples).
    5.  Return the final output grid.