
## train_1

**input:**
```
0 0 0 3 3 0 3 3 3 0 0 0 3 0 0 3 0 0
```


**output:**
```
0 0 0 4 4 0 8 8 8 0 0 0 6 0 0 6 0 0
```


## train_2

**input:**
```
0 0 3 3 0 3 0 0 3 3 3 0 0 0 3 3 0 0
```


**output:**
```
0 0 4 4 0 6 0 0 8 8 8 0 0 0 4 4 0 0
```


## train_3

**input:**
```
0 0 3 3 3 0 0 0 3 3 0 0 0 3 0 3 0 0
```


**output:**
```
0 0 8 8 8 0 0 0 4 4 0 0 0 6 0 6 0 0
```

*   **Perception of Task Elements:**
    *   The input and output grids are one-dimensional arrays (or single rows).
    *   The input grids contain only white (0) and green (3) pixels.
    *   The output grids contain white (0) pixels and pixels of other colors (yellow=4, magenta=6, azure=8).
    *   The white pixels in the input remain white and in the same position in the output.
    *   The green pixels in the input are replaced by other colors in the output.
    *   Contiguous groups (or "blobs") of green pixels in the input are replaced by a single, uniform color in the output.
    *   The replacement color depends on the size (length) of the contiguous green group in the input.
        *   A green group of size 1 is replaced by magenta (6).
        *   A green group of size 2 is replaced by yellow (4).
        *   A green group of size 3 is replaced by azure (8).

*   **YAML Facts:**
    
```yaml
    task_type: color_transformation
    grid_dimensionality: 1D # or treated as 1xN 2D
    input_colors:
      - white (0)
      - green (3)
    output_colors:
      - white (0)
      - yellow (4)
      - magenta (6)
      - azure (8)
    objects:
      - type: contiguous_group
        color: green (3)
        properties:
          - size (number of pixels)
      - type: background
        color: white (0)
    actions:
      - name: identify_groups
        input: input_grid
        target_color: green (3)
        output: list of green groups (position, size)
      - name: map_color_by_size
        input: green_group
        conditions:
          - if size == 1: output_color = magenta (6)
          - if size == 2: output_color = yellow (4)
          - if size == 3: output_color = azure (8)
      - name: update_grid
        input: input_grid, identified_groups, mapped_colors
        output: output_grid
        logic: Replace pixels of each green group with its corresponding mapped color. Keep white pixels unchanged.
    relationships:
      - The output color of a group depends solely on the size of that group in the input.
      - The positions of non-white pixels are preserved from input to output.
      - White pixels remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid identical to the input grid.
    2.  Iterate through the input grid to identify contiguous horizontal groups of green (3) pixels. Record the starting position and size (length) of each group.
    3.  For each identified green group:
        a.  Determine the size of the group.
        b.  Select a replacement color based on the size:
            *   If size is 1, the replacement color is magenta (6).
            *   If size is 2, the replacement color is yellow (4).
            *   If size is 3, the replacement color is azure (8).
        c.  Update the corresponding segment in the output grid by replacing the original green pixels with the selected replacement color.
    4.  Return the modified output grid. White (0) pixels remain unaffected throughout the process.
