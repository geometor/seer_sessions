
## train_1

**input:**
```
0 6 6 6 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 6 6 6 0 0 6 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 6 6 6 0 6 6 6 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 6 6 6 0 0 0 6 0 0 0 0 6 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 0 0 6 6 6 0 0 6 6 6 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The task operates on single-row grids containing primarily white (0) pixels and some magenta (6) pixels.
    *   The core pattern involves sequences of three consecutive magenta pixels (`6 6 6`) and isolated single magenta pixels (`0 6 0`).
    *   The transformation replaces isolated magenta pixels with the three-pixel sequence.
    *   Existing three-pixel sequences in the input are preserved in the output.

*   **YAML Facts:**
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # Effectively 1D as inputs are single rows
    colors_present:
      - white (0)
      - magenta (6)
    objects:
      - type: sequence
        color: magenta (6)
        value: [6, 6, 6]
        behavior: preserved if present in input
      - type: isolated_pixel
        color: magenta (6)
        context: surrounded by white (0) pixels (pattern [0, 6, 0])
        behavior: transformed
    transformation:
      action: replacement
      target: isolated_pixel (magenta 6)
      replacement_pattern: sequence [6, 6, 6]
      placement_rule: The replacement sequence [6, 6, 6] overwrites the original [0, 6, 0] pattern centered on the original isolated pixel's position.
    background_color: white (0)
    grid_size_change: none
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input row to serve as the output row.
    2.  Iterate through the input row, examining each pixel from the second position up to the second-to-last position. Let the current index be `i`.
    3.  Check if the pattern `[white, magenta, white]` (i.e., `[0, 6, 0]`) exists starting at index `i-1` in the *input* row.
    4.  If this pattern is found, modify the *output* row by setting the pixels at indices `i-1`, `i`, and `i+1` to magenta (6).
    5.  After checking all relevant positions, return the modified output row.
