
## train_1

**input:**
```
0 2 2
0 0 2
0 0 0
```


**output:**
```
0 0 0
0 2 2
0 0 2
```


## train_2

**input:**
```
0 0 0
1 1 1
0 0 0
```


**output:**
```
0 0 0
0 0 0
1 1 1
```


## train_3

**input:**
```
0 1 0
1 1 0
0 0 0
```


**output:**
```
0 0 0
0 1 0
1 1 0
```


## train_4

**input:**
```
1 1 1
0 0 0
0 0 0
```


**output:**
```
0 0 0
1 1 1
0 0 0
```

*   **Perception:**
    *   Each input grid contains a single connected shape composed of non-white pixels (either red or blue in the examples) against a white background.
    *   The output grid is the same size as the input grid.
    *   The non-white shape from the input appears in the output, but shifted downwards by one row.
    *   The original positions occupied by the shape in the input become white in the output, unless they are occupied by the shifted shape.
    *   The relative positions of the pixels within the shape remain unchanged.
    *   The transformation appears to be a simple vertical translation downwards by one unit.

*   **Facts:**
    
```yaml
    task_type: transformation
    grid_properties:
      - size_input: 3x3 (all examples)
      - size_output: 3x3 (all examples)
      - background_color: white (0)
    objects:
      - name: shape
        pixels: contiguous block of non-white pixels (colors 1-blue, 2-red observed)
        count_per_grid: 1
    actions:
      - name: shift_down
        target: shape
        details: move vertically downwards by 1 row position
        constraints: original horizontal position is maintained
    relationships:
      - input_shape_pixels: map directly to output_shape_pixels after transformation
      - output_background: all pixels not occupied by the shifted shape are white (0)
    ```


*   **Natural Language Program:**
    1.  Identify all non-white pixels in the input grid. These pixels constitute the 'shape'.
    2.  Create a new output grid of the same dimensions as the input grid, initially filled with the background color (white, 0).
    3.  For each non-white pixel found at position `(row, column)` in the input grid with color `C`:
        a.  Calculate the new position `(row + 1, column)`.
        b.  If the new position is within the bounds of the grid dimensions, set the pixel at this new position in the output grid to color `C`.
    4.  The resulting grid is the output.
