
## train_1

**input:**
```
2 0
0 0
```


**output:**
```
2 2 0 0
2 2 0 0
0 0 1 0
0 0 0 1
```


## train_2

**input:**
```
0 0 0 5 0
0 5 0 0 0
0 0 0 0 0
0 5 0 0 0
0 0 0 0 0
```


**output:**
```
1 0 0 0 0 0 5 5 0 0
0 1 0 0 0 0 5 5 0 0
0 0 5 5 0 0 0 0 1 0
0 0 5 5 0 0 0 0 0 1
1 0 0 0 1 0 0 0 0 0
0 1 0 0 0 1 0 0 0 0
0 0 5 5 0 0 1 0 0 0
0 0 5 5 0 0 0 1 0 0
0 0 0 0 1 0 0 0 1 0
0 0 0 0 0 1 0 0 0 1
```


## train_3

**input:**
```
0 0 0 0 0 3
0 0 0 0 0 0
0 3 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0 3 3
1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0
```

*   **Perception:**
    *   The task involves transforming an input grid into an output grid.
    *   The output grid dimensions are consistently double the input grid dimensions (both height and width are multiplied by 2).
    *   Each pixel in the input grid maps to a 2x2 block of pixels in the output grid.
    *   The transformation rule depends on the color of the input pixel.
    *   Non-white pixels (colors 2, 3, 5 in the examples) in the input are expanded into a solid 2x2 block of the same color in the corresponding output location.
    *   White pixels (color 0) in the input are transformed into a specific 2x2 pattern in the output: mostly white (0), but with blue (1) pixels on the anti-diagonal (top-right and bottom-left cells of the 2x2 block).

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    transformation: scaling_and_pattern_replacement
    grid_properties:
      - input_grid:
          type: 2D_array
          cell_type: integer_color_code (0-9)
      - output_grid:
          type: 2D_array
          cell_type: integer_color_code (0-9)
          height: input_grid.height * 2
          width: input_grid.width * 2
    pixel_mapping:
      - rule: Each input pixel at (r, c) maps to a 2x2 block in the output grid starting at (r*2, c*2).
    transformation_rules:
      - condition: Input pixel color is non-white (not 0).
        action: Fill the corresponding output 2x2 block with the input pixel's color.
        target_pixels:
          - (r*2, c*2)
          - (r*2, c*2 + 1)
          - (r*2 + 1, c*2)
          - (r*2 + 1, c*2 + 1)
      - condition: Input pixel color is white (0).
        action: Fill the corresponding output 2x2 block with a pattern.
        pattern:
          - Set pixels at (r*2, c*2) and (r*2 + 1, c*2 + 1) to white (0).
          - Set pixels at (r*2, c*2 + 1) and (r*2 + 1, c*2) to blue (1). # Anti-diagonal
    ```


*   **Natural Language Program:**
    1.  Determine the dimensions (height `H`, width `W`) of the input grid.
    2.  Create a new output grid with dimensions (height `H*2`, width `W*2`), initially filled with a default color (e.g., white/0, although it will be overwritten).
    3.  Iterate through each pixel of the input grid, using its row index `r` (from 0 to `H-1`) and column index `c` (from 0 to `W-1`).
    4.  For each input pixel at `(r, c)`:
        a.  Identify the corresponding 2x2 block in the output grid, which starts at `(r*2, c*2)` and ends at `(r*2 + 1, c*2 + 1)`.
        b.  Check the color `C` of the input pixel at `(r, c)`.
        c.  If the color `C` is not white (0):
            i.  Set the color of all four pixels in the output 2x2 block (`(r*2, c*2)`, `(r*2, c*2 + 1)`, `(r*2 + 1, c*2)`, `(r*2 + 1, c*2 + 1)`) to `C`.
        d.  If the color `C` is white (0):
            i.  Set the color of the output pixels at `(r*2, c*2)` and `(r*2 + 1, c*2 + 1)` to white (0).
            ii. Set the color of the output pixels at `(r*2, c*2 + 1)` and `(r*2 + 1, c*2)` to blue (1).
    5.  Return the completed output grid.
